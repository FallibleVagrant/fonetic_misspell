#!/usr/bin/env python3

from english_to_ipa.eng_to_ipa import transcribe as ipa
#Use this import instead if you installed English-to-IPA.
#import eng_to_ipa as ipa

import random
import argparse
import sys

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="filename",
                    help="Input FILE to misspell", metavar="FILE")
parser.add_argument("-d", "--dict", dest="dictionary",
                    help="The dictionary that tells the program what to misspell IPA characters into", metavar="DICT")
parser.add_argument("-v", "--verbose",
                    action="store_true", dest="verbose", default=False,
                    help="Prints the input and IPA to stdout as well.")

args = parser.parse_args()

default_dict = {
    'ŋ': ['ng', 'n\''],
    'ʃ': ['sh'],
    'i': ['i', 'ee'],
    'θ': ['th', 'f', 'ff'],
    'ʤ': ['dge', 'ge'],
    'æ': ['ae', 'a'],
    'ˈæ': ['a'],
    'ˈi': ['e', 'i', 'ee'],
    'ʧ': ['ch'],
    'ˈh': ['\'', 'h'],
    'ɛ': ['e', 'eh'],
    'ð': ['d'],
    'j': ['ya', 'yu', '', 'y'],
    'z': ['z', 'ss', 's'],
    's': ['z', 'ss', 's'],
    'f': ['ph', 'f'],
    'ə': ['ah', 'a'],
    'ʌ': ['u', 'oo', 'a'],
    'k': ['k', 'c'],
    'u': ['u', 'oo'],
    'ɪ': ['i', 'e'],
    'l': ['l', 'll'],
    'ɑ': ['u', 'o', '', '\''],
    'ʊ': ['ou', 'o', 'au'],
    'ɔ': ['o', 'ou', 'oh'],
    'aɪ': ['ai', 'ay'],
    'ai': ['ai', 'ay'],
    'eɪ': ['ay', 'ei']
}

swap_dict = {}

if args.dictionary is None:
    swap_dict = default_dict
else:
    #Build the dictionary from the supplied file.
    with open(args.dictionary, 'r') as dict_file:
        for line in dict_file:
            words = line.split()
            for i, word in enumerate(words):
                if word == "NULL":
                    words[i] = ""
            if len(words) > 0:
                swap_dict[words[0]] = words[1:]
            else:
                print("Format error in provided dictionary, using in-built default dictionary instead.", file=sys.stderr)
                swap_dict = default_dict
                break

#Sorted so we get diphthongs first -- this makes us process "ei" first if we encounter an "e".
swap_list = sorted(list(swap_dict), key=len, reverse=True)

if args.filename is None:
    input_file = sys.stdin
else:
    input_file = open(args.filename, 'r')

for line in input_file:
    if line == "\n":
        continue
    ipa_line = ipa.convert(line)
    if args.verbose:
        line = line.replace("\n", "")
        print(f"Original line: {line}")
        print()
        print(f"IPA: {ipa_line}")
        print()
    output = []

    i = 0
    while i < len(ipa_line):
        c = ipa_line[i]
        swapped = False

        for key in swap_list:
            #Check if we have an exact match at index i.
            index = ipa_line.find(key, i, i + len(key))

            if not index == -1:
                possible_swaps = swap_dict[key]
                swap_index = random.randrange(len(possible_swaps))
                output += [possible_swaps[swap_index]]
                swapped = True
                i += len(key) - 1
                break

        #If we didn't swap, use the original character.
        if not swapped:
            output += [c]

        i += 1
   
    #Joing output, and get rid of any remaining stress marks.
    print("".join(output).replace("ˈ", "").replace("ˌ", ""))
    if args.verbose:
        print()

if input_file is not sys.stdin:
    input_file.close()
