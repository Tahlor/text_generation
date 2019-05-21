import csv
import sys
import os
import re

csv.field_size_limit(sys.maxsize)

""" Process large corpus of text, clean out symbols
Used for e.g. creating font images.
"""

input_path = r"./text/documents_utf8_filtered_20pageviews.csv"
output_path = r"./text/raw_text.txt"

remove_parens = re.compile(r"[\(\[].*?[\)\]]")
double_spaces = re.compile(r"  ")
comma = re.compile(r" ,")
periods = re.compile(r" \.")
remove_symbols = re.compile(r'[^ a-zA-Z0-9_,.;:?%\'\"]+')

# num_lines = sum(1 for line in open(input_path))
# print(num_lines)
# 463819

def clean(text):
    text = remove_parens.sub("", text)
    text = remove_symbols.sub("", text)
    text = double_spaces.sub(" ", text)
    text = comma.sub(",", text)
    text = periods.sub(".", text)
    return text

def process(input_path, output_path, max=10000):
    if max:
        output_path = output_path.replace(".txt", "_{}.txt".format(max))
    with open(output_path, "w") as output:
        with open(input_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for i, row in enumerate(csv_reader):
                text = clean(row[1])
                output.write(text)
                if max and i > max:
                    break
if __name__=='__main__':
    process(input_path, output_path, max=10000)
    process(input_path, output_path, max=0)