#!/usr/bin/env python
import jsbeautifier
import re
import base64
import numpy
import urllib.parse
import argparse
import math
import json
from colorama import init, Fore, Style

options = jsbeautifier.default_options()
options.editorconfig = True
options.end_with_newline = True
options.space_in_empty_paren = True
options.jslint_happy = True
options.space_after_anon_function = True
options.space_after_named_function = True
options.unindent_chained_methods = True
options.break_chained_methods = True
options.keep_array_indentation = True
options.unescape_strings = True
options.e4x = True
options.comma_first = True
options.indent_empty_lines = True

"""
    Calculates the Shannon entropy of a UTF-8 encoded string
"""
def entropy_check(string):
    # decode the string as UTF-8
    unicode_string = string.decode('utf-8')

    # get probability of chars in string
    prob = [float(unicode_string.count(c)) / len(unicode_string) for c in dict.fromkeys(list(unicode_string))]

    # calculate the entropy
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])

    return entropy


"""
    Gets the string we are going to analyse, line per line or the full string from the file
"""
def calculate_entropy(filename, option):
    option = option.upper()

    if option == "FILE":
        with open(filename, 'rb') as f:
            content = f.read()
            print(f"File entropy is {entropy_check(content)}, if higher than 3.75 is not human written")


    elif option == "LINE":
        with open(filename, 'rb') as f:
            content = f.readlines()

            for line in content:
                entropy = entropy_check(line)
                if entropy > 3.75:
                    line_str = line[:-1]
                    line_str = line_str.decode('utf-8')

                    print(f"Entropy {entropy}, code: {line_str}")


"""
    Cleans the javascript string beautifying it
"""
def beautify_string(data):
    data = jsbeautifier.beautify(data, options)

    return data


"""
    Cleans the javascript file beautifying it
"""
def beautify_file(filename):
    res = jsbeautifier.beautify_file(filename, options)

    return res


"""
    Parse hex numbers to char
"""
def parse_hex(data):
    def replace_hex(match):
        try:
            decoded = bytes.fromhex(match.group(1)).decode('utf-8')
        except UnicodeDecodeError:
            decoded = bytes.fromhex(match.group(1)).decode("iso-8859-1")
        return decoded

    pattern = r'\\x([0-9a-fA-F]{2})'

    data = re.sub(pattern, replace_hex, data)

    return data


def parse_unicode(data):
    def replace_unicode(match):
        return chr(int(match.group(1), 16))

    pattern = r'\\u([0-9a-fA-F]{4})'

    data = re.sub(pattern, replace_unicode, data)

    return data


"""
    Finds base64 between '' and "" and then deletes first and last character 
"""
def find_base64(data):
    base64_pattern = r'["\'](?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=|[A-Za-z0-9+/]{4})["\']'
    base64_strings = re.findall(base64_pattern, data)

    base64_strings_cleaned = []
    for match in base64_strings:
        match = match[1:-1]
        if len(match) >= 10:
            base64_strings_cleaned.append(match)
    return base64_strings_cleaned

"""
    Decodes base64 and saves it to json output file
"""
def decode_base64(encoded_data):
    decoded_strings = []
    for base64_string in encoded_data:
        decoded_bytes = base64.b64decode(base64_string)
        try:
            decoded_string = decoded_bytes.decode("'utf-8'")
        except UnicodeDecodeError:
            decoded_string = decoded_bytes.decode("iso-8859-1")

        decoded_dict = {'original': base64_string, 'decoded':decoded_string}
        decoded_strings.append(decoded_dict)
    return decoded_strings


"""
    Appending characrers between + like "A" + "B" 
"""
def append_strings_multi(data):
    # Regular expression pattern to match (number).toString( number )
    pattern = r'[\'\"]\s+\+\s+[\'\"]'

    # Find all matches of the pattern
    matches = re.finditer(pattern, data, re.MULTILINE)

    length = 0

    for match in matches:
        print(match.group(0))

        to_string = ""

        data = data[:match.start() - length] + to_string + data[match.end() - length:]

        length = length + len(match.group(0))

    return data

"""
    Replaces toString function parsing its contect to string integer equivalent
    after parsing the integer to the new base
"""
def replace_tostring(data):
    # Regular expression pattern to match (number).toString( number )
    pattern = r'\(\s*(\d+)\s*\)\s*\.toString\(\s*(\d+)\s*\)'

    # Find all matches of the pattern
    matches = re.finditer(pattern, data, re.MULTILINE)

    length = 0

    for match in matches:
        # Extract the two numbers from the matched groups
        first_number = int(match.group(1))
        second_number = int(match.group(2))

        to_string = numpy.base_repr(first_number, second_number)

        to_string = "\"" + to_string + "\""

        data = data[:match.start() - length] + to_string + data[match.end() - length:]

        length = length + len(match.group(0)) - 3

    return data

"""
    If there is a char set, it replaces it with the last value ("A", "B", "C") is "C"
"""
def parse_char_set(data):
    pattern = r'\+\s*\((\s*"[a-zA-Z]"\s*,\s*)+\s*"([a-zA-Z])"\s*\)\s*\+'

    # Find all matches of the pattern
    matches = re.finditer(pattern, data, re.MULTILINE)

    length = 0

    for match in matches:
        to_string = "+ \"" + match.group(2) + "\" +"

        print(match.group(0))
        print(match.group(2))
        print(to_string)
        data = data[:match.start() - length] + to_string + data[match.end() - length:]

        length = length + len(match.group(0)) - 7

    pattern = r'\+\s*\((\s*"[a-zA-Z]"\s*,\s*)+\s*"([a-zA-Z])"\s*\)\s*'

    # Find all matches of the pattern
    matches = re.finditer(pattern, data, re.MULTILINE)

    length = 0

    for match in matches:
        to_string = "+ \"" + match.group(2) + "\" "

        print(match.group(0))
        print(match.group(2))
        print(to_string)
        data = data[:match.start() - length] + to_string + data[match.end() - length:]

        length = length + len(match.group(0)) - 6

    pattern = r'\s*\((\s*"[a-zA-Z]"\s*,\s*)+\s*"([a-zA-Z])"\s*\)\s*\+'

    # Find all matches of the pattern
    matches = re.finditer(pattern, data, re.MULTILINE)

    length = 0

    for match in matches:
        to_string = " \"" + match.group(2) + "\" +"

        print(match.group(0))
        print(match.group(2))
        print(to_string)
        data = data[:match.start() - length] + to_string + data[match.end() - length:]

        length = length + len(match.group(0)) - 6

    return data


"""
    Replaces toString function parsing its contect to string integer equivalent
    after parsing the hex to integer and then to the new base
"""
def replace_hex_tostring(data):
    # Regular expression pattern to match (number).toString( number )
    pattern = r'\(\s*(\d+)\s*\)\s*\.toString\(\s*(0x[\da-fA-F]+)\s*\)'

    # Find all matches of the pattern
    matches = re.finditer(pattern, data, re.MULTILINE)

    length = 0

    for match in matches:
        # Extract the two numbers from the matched groups
        first_number = int(match.group(1))
        second_number = match.group(2)

        second_number = int(second_number, 16)

        to_string = numpy.base_repr(first_number, second_number)

        to_string = "\"" + to_string + "\""

        data = data[:match.start() - length] + to_string + data[match.end() - length:]

        length = length + len(match.group(0)) - 3

    return data


"""
    Replaces parseInt function parsing the content char to a in integer value
"""
def parse_int(data):
    pattern = r'parseInt\("(\d+)"\)'

    # Find all matches of the pattern
    matches = re.finditer(pattern, data, re.MULTILINE)

    length = 0

    for match in matches:
        data = data[:match.start() - length] + match.group(1) + data[match.end() - length:]

        length = length + len(match.group(0)) - 1

    return data


def parse_unescape(data):
    pattern = r'unescape\([\'"]([^\'"]+)[\'"]\)'

    def replacement(match):
        unicode_escaped = urllib.parse.unquote(match.group(1))
        replaced_unicode_escaped = unicode_escaped.replace('%', '\\')
        decoded_string = bytes(replaced_unicode_escaped, 'utf-8').decode('unicode_escape')
        return "\'" + decoded_string + "\'"

    data = re.sub(pattern, replacement, data)
    return data


def parse_eval_list_numbers(data):
    def replace_with_chars(match):
        numbers = re.findall(r'\d+', match.group(1))
        chars = ''.join(chr(int(num)) for num in numbers)
        return "\'" + chars + "\'"

    pattern = r"'([^']*?\((?:\d+(?:\s*,\s*)?)+\))'"
    data = re.sub(pattern, replace_with_chars, data)

    return data


def deobfuscate_data(file_path, file_out, level):
    data_beautified = beautify_file(file_path)

    if level == 0:
        print("Level. 0 All options")

        data_beautified = parse_hex(data_beautified)

        data_beautified = parse_unicode(data_beautified)

        data_beautified = replace_tostring(data_beautified)

        data_beautified = replace_hex_tostring(data_beautified)

        data_beautified = parse_eval_list_numbers(data_beautified)

        data_beautified = parse_unescape(data_beautified)

        data_beautified = parse_int(data_beautified)

        data_beautified = parse_char_set(data_beautified)

        data_beautified = append_strings_multi(data_beautified)

        data_beautified = beautify_string(data_beautified)

    elif level == 1:
        print("Level. 1 Just Beautify the File")

    elif level == 2:
        print("Level. 2 Parse Hex numbers to String")

        data_beautified = parse_hex(data_beautified)

        data_beautified = beautify_string(data_beautified)
    elif level == 3:
        print("Level. 3 Parse Unicode characters")

        data_beautified = parse_unicode(data_beautified)

        data_beautified = beautify_string(data_beautified)

    elif level == 4:
        print("Level. 4 Deobfuscate toString with numbers")

        data_beautified = replace_tostring(data_beautified)

        data_beautified = beautify_string(data_beautified)

    elif level == 5:
        print("Level. 5 Deobfuscate toString with Hex numbers")

        data_beautified = replace_hex_tostring(data_beautified)

        data_beautified = beautify_string(data_beautified)

    elif level == 6:
        print("Level. 6 Deobfuscate Eval with a list of numbers ")

        data_beautified = parse_eval_list_numbers(data_beautified)

        data_beautified = replace_hex_tostring(data_beautified)

    elif level == 7:
        print("Level. 7 Deobfuscate unescape function inside chars ")

        data_beautified = parse_unescape(data_beautified)

        data_beautified = replace_hex_tostring(data_beautified)

    elif level == 8:
        print("Level. 8 Deobfuscate char sets ")

        data_beautified = parse_char_set(data_beautified)

        data_beautified = replace_hex_tostring(data_beautified)


    elif level == 9:
        print("Level. 9 Deobfuscate parseInt function ")

        data_beautified = parse_int(data_beautified)

        data_beautified = replace_hex_tostring(data_beautified)


    elif level == 10:
        print("Level. 10 Append Chars")

        data_beautified = append_strings_multi(data_beautified)

        data_beautified = replace_hex_tostring(data_beautified)

    with open(file_out, "w") as f:
        f.write(data_beautified)

if __name__ == "__main__":

    init(autoreset=True)  # Initialize Colorama and autoreset colors

    print(Fore.LIGHTMAGENTA_EX + """                                               
              ,,                                                ,               
              /@ @@ /    *@@(      (@         @#        @@%     #@@%            
              *@. #@(    *@  (@&   (@#@#   %@#@#           @@   /@  .@@.        
              *@@@       *@ (@@    (@   @@@   @#    ,@@    @@   /@(@@.          
              /@         /@@*      #@         @&  @@,   &@@     /@    .         
              (@         (@ ,@@%   @@         @@   @@*          #@              
              %@         %@    ,   @@        .@@     %@@.       &@              
    """)

    print(Fore.LIGHTBLUE_EX + """    
               ⚔️🛡️⚒️🗡️🛶🏹🔱 Freyja Desobfuscating Tool ⚔️🛡️⚒️🗡️🛶🏹🔱                                                                               
    """)

    parser = argparse.ArgumentParser(usage = Fore.LIGHTCYAN_EX + " [-h] -f FILEIN [-o FILEOUT] [-l LEVEL] [-b] [-e {LINE,FILE,line,file}]")

    parser.add_argument('-f', '--filein', required=True, help= 'Input file name')
    parser.add_argument('-o', '--fileout', help='Output file name')
    parser.add_argument('-l', '--level', type=int, help='Level 0: All options.'
                                                        'Level 1: Just Beautify the File.'
                                                        'Level 2: Parse Hex numbers to String.'
                                                        'Level 3: Parse Unicode characters.'
                                                        'Level 4: Deobfuscate toString with numbers.'
                                                        'Level 5: Deobfuscate toString with Hex numbers.'
                                                        'Level 6: Deobfuscate Eval with a list of numbers.'
                                                        'Level 7: Deobfuscate unescape function inside chars.'
                                                        'Level 8: Deobfuscate char sets.'
                                                        'Level 9: Deobfuscate parseInt function.'
                                                        'Level 10: Append Chars.')

    parser.add_argument('-b', action='store_true', help='Extract Base64 strings')
    parser.add_argument('-e', choices=['LINE', 'FILE', 'line', 'file'], help='Shannon Entropy. Specify either "line" or "file"')

    args = parser.parse_args()
    if not any(vars(args).values()):
        parser.print_help()
        exit(-1)

    if args.filein:
        print(f"Input file: {args.filein}")
        file_path = args.filein

    if args.fileout:
        file_out = args.fileout
    else:
        if args.b:
            file_out = "out.json"
        else:
            file_out = "out.js"

    print(f"Output file: {file_out}")

    if args.b:
        data_beautified = beautify_file(file_path)
        base64_found = decode_base64(find_base64(data_beautified))
        with open(file_out, "w") as json_file:
            json.dump(base64_found, json_file)


    elif args.e:
        print(f"We all checking entropy {args.e}")
        calculate_entropy(file_path, args.e)

    elif args.level is not None:
        level = args.level
        deobfuscate_data(file_path, file_out, level)
    else:
        print(f"We will obfuscate with all techniques")
        deobfuscate_data(file_path, file_out, 0)
