#!/usr/bin/env python

import jsbeautifier, re, base64

options = jsbeautifier.default_options()
options.editorconfig = True
options.end_with_newline = True
options.space_in_paren = True
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




def beautify_string(filename):
    with open(filename, 'r') as f:
        content = f.read()

        res = jsbeautifier.beautify(content, options)

        return res

def beautify_file(filename):
    res = jsbeautifier.beautify_file(filename, options)

    return res


def replace_hex(match):
    return bytes.fromhex(match).decode('utf-8')
def parse_hex(data):

    print("Hex")
    pattern = r'\\x([0-9a-fA-F]{2})'

    data = re.sub(pattern, replace_hex, data)

    return data

def replace_unicode(match):
    return chr(int(match.group(1), 16))

def parse_unicode(data):

    print("Unicode")
    pattern = r'\\u([0-9a-fA-F]{4})'

    data = re.sub(pattern, replace_unicode, data)

    return data

def find_base64(data):
    base64_pattern = r"'([A-Za-z0-9+/=]+)'"
    base64_strings = re.findall(base64_pattern, data)
    return base64_strings


def decode_base64(encoded_data):
    decoded_strings = []
    for base64_string in encoded_data:
        decoded_bytes = base64.b64decode(base64_string)
        decoded_string = decoded_bytes.decode('utf-8')
        decoded_strings.append(decoded_string)
    return decoded_strings



if __name__ == "__main__":
    print("""                                                   
              ,,                                                ,               
              /@ @@ /    *@@(      (@         @#        @@%     #@@%            
              *@. #@(    *@  (@&   (@#@#   %@#@#           @@   /@  .@@.        
              *@@@       *@ (@@    (@   @@@   @#    ,@@    @@   /@(@@.          
              /@         /@@*      #@         @&  @@,   &@@     /@    .         
              (@         (@ ,@@%   @@         @@   @@*          #@              
              %@         %@    ,   @@        .@@     %@@.       &@              
                                                                                
                            Freyja Desobfuscating Tool                                                                               
    """)

    #file_path = "../samples/ejercicio6.js"
    file_path = "../samples/do_not_run.js"
    #file_path = "../samples/2b0c9059feece8475c71fbbde6cf4963132c274cf7ddebafbf2b0a59523c532e.js"
    #file_path = "../samples/b122473d00566758d09c695d191b368e0c815c65e8acc0f00da7a88e45cc8a9e.js"
    #file_path = "../samples/javascript-malware-collection/2017/20170507/20170507_0d258992733e8a397617eae0cbb08acc.js"
    #file_path = "../samples/javascript-malware-collection/2017/20170501/20170501_018edd4b581516682574e305c835c5c9.js"

    #print(beautify_string(file_path))

    data_beautified = beautify_file(file_path)

    #print("Beautifulling\n", data_beautified)

    base64_data = find_base64(data_beautified)

    #print(base64_data)

    data_beautified = parse_hex(data_beautified)
    data_beautified = parse_unicode(data_beautified)

    print(data_beautified)