#!/bin/python3
import math

def entropy_check(string):
    "Calculates the Shannon entropy of a UTF-8 encoded string"

    # decode the string as UTF-8
    unicode_string = string.decode('utf-8')

    # get probability of chars in string
    prob = [float(unicode_string.count(c)) / len(unicode_string) for c in dict.fromkeys(list(unicode_string)) ]

    # calculate the entropy
    entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])

    return entropy

filename = input("Write down the path of the file to analyze >")

option = input("What do you want to do? Analyze file [file] or line per line [line]>").upper()


if option == "FILE":
    with open(filename, 'rb') as f:
        content = f.read()
        print("Test2", entropy_check(content))


elif option == "LINE":
    with open(filename, 'rb') as f:
        content = f.readlines()

        for line in content:
            entropy = entropy_check(line)
            if entropy > 3.75:
                print(line[:-1])
                print("This line has High Entropy", entropy)
