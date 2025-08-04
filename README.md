# phpXORer
This script was made... well because I can. I found it amazing how you can use a different approach to run code in PHP.  
The script is not perfect it was made very quickly. Its not efficient nor is it pleasable to read.  

## Usage

### Text to XOR (-t string)
```shell
python3 phpXORer.py -t 'echo "test";'
python3 phpXORer.py -t 'echo "test";' -d 6
```
This will print out 4 lines because by default the script uses 4 chars to XOR on.  
`["@", "[", "\\", "^"]`

### Execution method (-e int)
```shell
python3 phpXORer.py -e 1 -t 'echo "test";'
python3 phpXORer.py -e 1 -t 'echo "test";' -d 6
python3 phpXORer.py -e 2 -t 'testing()'
python3 phpXORer.py -e 2 -t 'testing(test())'
```
This will again print out 4 lines but it will either use eval or echo as form of exploitation.

```python
e_choices = {
    1: 'eval',
    2: 'echo'
}
```

### Blacklist (-b)
Black list has to be added inside of the script because using `\t`, `\n` and other inside the console is a bit tricky.  
To edit just search inside the script `Blacklist array`  

### Character to XOR with (-c "a")
```shell
python3 phpXORer.py -e 1 -t 'echo "test";' -c "a"
python3 phpXORer.py -e 1 -t 'echo "test";' -c "a" -d 6
```
This will use the character to XOR with. It will not use the 4 mentioned above but it will use the one specified

### Random XOR (-r)
```shell
python3 phpXORer.py -e 1 -t 'echo "test";' -r
python3 phpXORer.py -e 1 -t 'echo "test";' -r -d 6
```
This will use random characters to XOR the text.

### All (-a)
```shell
python3 phpXORer.py -a
python3 phpXORer.py -a -d 6
```
You have to **have blacklist edited** to use this method. It will find all possibilities to XOR to get all printable characters.  
> It cannot be used with `-t` and `-e`  

### Depth (-d x > 5)
```shell
python3 phpXORer.py -e 1 -t 'echo "test";' -r -d 6
```
So for finding what characters can be XORed together I used simple recursion. The problem is python can only go so deep so I added a depth limit which is maximum of 5. You can overwrite this depth by using the -d flag.