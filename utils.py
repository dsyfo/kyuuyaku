# -*- coding: utf-8 -*-
table = open("table.txt")

str2byte = {}
byte2str = {}
known_ranges = []

value = None
startvalue = None
for line in table:
    oldvalue = value
    if not startvalue:
        startvalue = value

    line = line.strip().split()
    if len(line) >= 2:
        value = int(line[-1], 16)
        char = line[0]
    elif len(line) == 1:
        value = value + 1
        char = line[0]

    if oldvalue and value not in [oldvalue,  oldvalue + 1] and oldvalue >= startvalue:
        known_ranges.append((startvalue, oldvalue))
        startvalue = value

    assert value
    str2byte[char] = value
    byte2str[value] = char

known_ranges.append((startvalue, value))
str2byte[' '] = 0x8140
byte2str[0x8140] = ' '
known_ranges.append((0x8140, 0x8140))

found_kanji = [int(x.strip(), 16) for x in open("found_kanji.txt")]

if __name__ == "__main__":
    pass
