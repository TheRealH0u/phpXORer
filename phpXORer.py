from functools import reduce
import argparse
import string
import re
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

def find_combinations(target_char, xor_char, depth, blacklist, current_combo=[]):
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

def xor_find_matching_character(target_char, xor_char):
    # Convert characters to ASCII values
    target_char_ascii = ord(target_char)
    xor_char_ascii = ord(xor_char)
    
    # Iterate through printable characters to find a match
    for printable_char in string.printable:
        xor_result = ord(printable_char) ^ xor_char_ascii
        
        if chr(xor_result) == target_char:
            return printable_char
    raise Exception("No matching printable character found for encoding")

def split_string(input_string):
    # Regular expression pattern to match contents inside parentheses
    pattern = r'\("(.*?)"\)'

    # Using re.findall to extract all matches
    matches = re.findall(pattern, input_string)

    # Initialize an empty list to store contents inside parentheses
    contents_list = []

    # Iterate through matches and store contents in the list
    for match in matches:
        contents_list.append(match)
    return contents_list

def XOR_encode(string_to_encode:str, blacklist: list, xor_chars:list, random:bool):
    for xor_char in xor_chars:
        try:
            if not random:
                print(f"# --- {xor_char} --- #")
            else:
                print(f"# --- Random --- #")
            output = []
            for char in string_to_encode:
                results = []
                depth = initial_depth
                while not results:
                    if random:
                        xor_char = random_char(blacklist)
                    results = find_combinations(char, xor_char, depth, blacklist)
                    depth += 1
                    if depth > max_depth:
                        raise Exception("To many depths")
                r = output_string(results[0])
                output.append("("+" ^ ".join(r)+f' ^ {output_string(xor_char)[0]})')

            print(f"(", end="")
            print(".".join(output) + ");")
            print("")
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
                    #encoded_char = xor_find_matching_character(char, xor_char)
                    while not results:
                        results = find_combinations(char, xor_char, depth, blacklist)
                        depth += 1
                        if depth > max_depth:
                            raise Exception("To many depths")
                    r = output_string(results[0])
                    print(f"{repr(char)} => "+" ^ ".join(r)+f' ^ {output_string(xor_char)[0]}')
                except Exception as e:
                    print(f"{ord(char)} = {char} => {e}")
                    continue
                except KeyboardInterrupt as e:
                    exit(0)
            print("")
        

def XOR_echo(string_to_encode:str, blacklist: list, xor_chars: list, random:bool):
    """
    Usage: python3 phpXORer.py -e 2 -t '("writeMsg")("")'
    This can be pasted directly and it will work
    Usage: python3 phpXORer.py -e 2 -t '("writeMsg")()'
    With this you have to add at the end () because empty brackets get deleted. 
    They have to have "" inside of them 
    """
    global initial_depth
    global max_depth
    string_to_encode_array = split_string(string_to_encode)

    for xor_char in xor_chars:
        try:
            if not random:
                print(f"# --- {xor_char} --- #")
            else:
                print(f"# --- Random --- #")
            output = ""
            output_array = []
            for string_to_encode in string_to_encode_array:
                output += "("
                for char in string_to_encode:
                    results = []
                    depth = initial_depth
                    #encoded_char = xor_find_matching_character(char, xor_char)
                    while not results:
                        if random:
                            xor_char = random_char(blacklist)
                        results = find_combinations(char, xor_char, depth, blacklist)
                        depth += 1
                        if depth > max_depth:
                            raise Exception("To many depths")
                    r = output_string(results[0])
                    output_array.append("("+" ^ ".join(r)+f' ^ {output_string(xor_char)[0]})')
                output += ".".join(output_array)
                output += ")"
            print(f"echo ", end="")
            print(output + ";")
            print("")
        except Exception as e:
            print(e)
            continue

def XOR_eval(string_to_encode:str, blacklist: list, xor_chars: list, random:bool):
    global initial_depth
    global max_depth
    for xor_char in xor_chars:
        try:
            if not random:
                print(f"# --- {xor_char} --- #")
            else:
                print(f"# --- Random --- #")
            output = []
            for char in string_to_encode:
                results = []
                depth = initial_depth
                while not results:
                    if random:
                        xor_char = random_char(blacklist)
                    results = find_combinations(char, xor_char, depth, blacklist)
                    depth += 1
                    if depth > max_depth:
                        raise Exception("To many depths")
                r = output_string(results[0])

                # print(r)
                # print(results[0])
                # input()
                output.append("("+" ^ ".join(r)+f' ^ {output_string(xor_char)[0]})')

            # Print the encoded output
            print(f"eval(", end="")
            print(".".join(output) + ");")
            print("")
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


parser.add_argument('-b', '--blacklist', type=str, help='Blacklist separated by commas')
parser.add_argument('-d', '--depth', type=int, help='Increase or decrease the depth of recursion')

# Parse the arguments
args = parser.parse_args()

# Blacklist array
if args.blacklist:
    parser.error("Add the blacklist inside the script (Blacklist array). Dont forget to escape the characters")
blacklist = [] # Add blacklist inside script ["\\", "\t", ","]


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
