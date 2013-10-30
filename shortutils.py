# -*- coding: utf-8 -*-
def get_dicts(table):
    value, startvalue = None, None
    a, b = {}, {}
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
        a[char] = value
        b[value] = char
    a[' '] = 1
    b[1] = ' '
    return a, b

table = open("shorttable.txt")
str2byte, byte2str = get_dicts(table)
table = open("shortwritetable.txt")
write2byte, write2str = get_dicts(table)
