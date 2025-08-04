from functools import reduce
import argparse
import string
import json
import random

initial_depth = 1
max_depth = 5

def random_char(blacklist):
    printable_chars = string.printable.strip()  # Get all printable characters
    while True:
        random_char = random.choice(printable_chars)
        if random_char not in blacklist:
            return random_char

def find_combinations(target_char, xor_char, depth, blacklist, current_combo=None):
    if current_combo is None:
        current_combo = []
    target_value = ord(target_char)
    xor_value = ord(xor_char)
    printable_chars = ''.join([c for c in string.printable if c != '\u000b'])
    
    # If we've reached the desired depth, check if the current combination is valid
    if depth == 0:
        combined_value = reduce(lambda x, y: x ^ y, map(ord, current_combo), xor_value)
        if combined_value == target_value:
            return [current_combo]
        return []

    results = []

    for char in printable_chars:
        if char in blacklist:
            continue
        new_combo = current_combo + [char]
        found_combos = find_combinations(target_char, xor_char, depth - 1, blacklist, new_combo)
        if found_combos:
            results.extend(found_combos)
            break  # Stop if we find any valid combinations at this depth

    return results

def output_string(inps):
    result = []
    for inp in inps:
        # Use json.dumps to escape special characters
        escaped_inp = json.dumps(inp)
        # Append " at the beginning and end
        result.append(escaped_inp)
    return result

def parse_nested_call(expression):
    """
    Parses a nested PHP expression into a tree:
    Examples:
    'var_dump' -> ['var_dump']
    'var_dump()' -> ['var_dump', []]
    'var_dump(get_cwd())' -> ['var_dump', ['get_cwd', []]]
    """
    expression = expression.strip()
    if not expression:
        return []

    # Check if there's a '(' in expression
    if '(' not in expression:
        # No parentheses = single function name
        return [expression]

    # Find function name (before first '(')
    func_name_end = expression.index('(')
    func_name = expression[:func_name_end].strip()

    # Extract inner content between matching parentheses
    i = func_name_end
    depth = 0
    start_inner = None
    for idx in range(i, len(expression)):
        if expression[idx] == '(':
            if depth == 0:
                start_inner = idx + 1
            depth += 1
        elif expression[idx] == ')':
            depth -= 1
            if depth == 0:
                end_inner = idx
                break
    else:
        raise Exception("Unbalanced parentheses")

    inner_expr = expression[start_inner:end_inner].strip()

    if inner_expr == '':
        # empty args
        return [func_name, []]

    # For now, we assume only single argument (could extend to multiple comma-separated later)
    # Parse inner expression recursively
    inner_parsed = parse_nested_call(inner_expr)

    return [func_name, inner_parsed]

def encode_function_tree(tree, xor_char, blacklist):
    # If tree is just a function name string, XOR encode and wrap in ()
    if isinstance(tree, str):
        output = []
        for char in tree:
            results = []
            depth = initial_depth
            while not results:
                results = find_combinations(char, xor_char, depth, blacklist)
                depth += 1
                if depth > max_depth:
                    raise Exception("Too many depths")
            r = output_string(results[0])
            output.append("(" + " ^ ".join(r) + f" ^ {output_string(xor_char)[0]})")
        return "(" + ".".join(output) + ")"

    # If tree is a list, first element is function name (string), second element is arguments (list or empty)
    if isinstance(tree, list):
        func_name = tree[0]
        encoded_func = encode_function_tree(func_name, xor_char, blacklist)

        # If no args or empty args (empty list)
        if len(tree) == 2 and tree[1] == []:
            return f"{encoded_func}()"
        elif len(tree) == 1:
            return f"{encoded_func}"

        # Otherwise, recursively encode argument(s)
        encoded_arg = encode_function_tree(tree[1], xor_char, blacklist)
        return f"{encoded_func}({encoded_arg})"

    raise Exception("Invalid tree structure")

def xor_encode_string(string_to_encode, xor_char, blacklist, random=False):
    output = []
    for char in string_to_encode:
        depth = initial_depth
        results = []
        current_xor = xor_char
        while not results:
            if random:
                current_xor = random_char(blacklist)
            results = find_combinations(char, current_xor, depth, blacklist)
            depth += 1
            if depth > max_depth:
                raise Exception("Too many depths")
        r = output_string(results[0])
        output.append("(" + " ^ ".join(r) + f" ^ {output_string(current_xor)[0]})")
    return ".".join(output)


def XOR_encode(string_to_encode:str, blacklist: list, xor_chars:list, random:bool):
    for xor_char in xor_chars:
        try:
            label = xor_char if not random else "Random"
            print(f"# --- {label} --- #")
            encoded = xor_encode_string(string_to_encode, xor_char, blacklist, random)
            print(f"({encoded});\n")
        except Exception as e:
            print(e)
            continue

def XOR_all(blacklist: list, xor_chars: list, random:bool):
    if len(blacklist) == 0:
        parser.error("-b is empty")
    else:
        for xor_char in xor_chars:
            print(f"# --- {xor_char} --- #")
            for char in string.printable:
                try:
                    results = []
                    depth = initial_depth
                    while not results:
                        results = find_combinations(char, xor_char, depth, blacklist)
                        depth += 1
                        if depth > max_depth:
                            raise Exception("Too many depths")
                    r = output_string(results[0])
                    print(f"{repr(char)} => "+" ^ ".join(r)+f' ^ {output_string(xor_char)[0]}')
                except Exception as e:
                    print(f"{ord(char)} = {char} => {e}")
                    continue
                except KeyboardInterrupt as e:
                    exit(0)
            print("")
        

def XOR_echo(string_to_encode: str, blacklist: list, xor_chars: list, random: bool):
    tree = parse_nested_call(string_to_encode)
    for xor_char in xor_chars:
        try:
            print(f"# --- XOR echo: {xor_char} --- #")
            encoded = encode_function_tree(tree, xor_char, blacklist)
            print(f"{encoded}\n")
        except Exception as e:
            print(e)
            continue

def XOR_eval(string_to_encode:str, blacklist: list, xor_chars: list, random:bool):
    for xor_char in xor_chars:
        try:
            label = xor_char if not random else "Random"
            print(f"# --- XOR eval: {label} --- #")
            encoded = xor_encode_string(string_to_encode, xor_char, blacklist, random)
            print(encoded)
        except Exception as e:
            print(e)
            continue

# Define the mapping for -e values
e_choices = {
    1: 'eval',
    2: 'echo'
}

# Create the parser
parser = argparse.ArgumentParser(description='PHP XORer')

# Optional arguments -e (numerical) and -t (text option)
group_et = parser.add_argument_group('optional arguments')
group_et.add_argument('-e', '--numerical', type=int, choices=e_choices, help='Numerical option (1 for eval, 2 for echo)')
group_et.add_argument('-t', '--text', type=str, help='Text option')

# Exclusive option -a (cannot be used with -e or -t)
group_a = parser.add_mutually_exclusive_group()
group_a.add_argument('-a', '--all', action='store_true', help='Print out all characters that are XORed with a char (-c) or @, [, \\, ^')

# Exclusive options for -c and -r
xor_group = parser.add_mutually_exclusive_group()
xor_group.add_argument('-c', '--char', type=str, help='One character to XOR with')
xor_group.add_argument('-r', '--random', action='store_true', help='Use random XOR characters')


# parser.add_argument('-b', '--blacklist', type=str, help='Blacklist separated by commas')
parser.add_argument('-d', '--depth', type=int, help='Increase or decrease the depth of recursion')

# Parse the arguments
if __name__ == "__main__":
    args = parser.parse_args()

    # Blacklist array
    # if args.blacklist:
    #     parser.error("Add the blacklist inside the script (Blacklist array). Dont forget to escape the characters")
    blacklist = ["@", "[", "]", "{", "}", "\\", "/", ",", "=", "*", "+", "-", ";", "?", "!", "\n", "\r", "\t", "\f", "%", "$", "'", "<", ">", "\""]
    blacklist += list(string.ascii_letters)

    if args.depth:
        max_depth = int(args.depth)

    xor_chars = None
    if not args.char:
        if not args.random:
            xor_chars = ["@", "[", "\\", "^"]
        else:
            xor_chars = ["1"]
    else:
        xor_chars = list(args.char)

    if args.all:
        if args.numerical or args.text:
            parser.error("-a cannot be used with -e or -t")
        XOR_all(blacklist, xor_chars, args.random)
    elif args.numerical or args.text:
        if not args.text:
            parser.error("-t should not be empty")
        if args.numerical == 1:
            XOR_eval(args.text, blacklist, xor_chars, args.random)
        elif args.numerical == 2:
            XOR_echo(args.text, blacklist, xor_chars, args.random)
        else:
            XOR_encode(args.text, blacklist, xor_chars, args.random)
