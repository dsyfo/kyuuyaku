# -*- coding: utf-8 -*-
table = open("shorttable.txt")
str2byte = {}
byte2str = {}

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
        startvalue = value

    assert value
    str2byte[char] = value
    byte2str[value] = char

str2byte[' '] = 1
byte2str[1] = ' '
