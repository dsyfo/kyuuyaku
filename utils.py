# -*- coding: utf-8 -*-
from collections import defaultdict

ALL_START = 0x8141
KANJI_START = 0x889f
KANJI_END = 0x9872

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

# 0x28000
POINTER_TABLES = [0x80000,
                  0x88000,
                  0x90000,
                  0x98000,
                  0x158000]


def is_kanji(value):
    return KANJI_START <= ord(value) <= KANJI_END


def is_a_char(value):
    return ALL_START <= ord(value) <= KANJI_END


def get_messages():
    rom = open("kyuuyaku_megami_tensei_clean.sfc", "rb")
    messages = {}
    for table in POINTER_TABLES:
        assert not table % 0x8000
        offset = 0
        pointers = []
        while True:
            if offset in pointers or offset >= 0x8000:
                break

            rom.seek(table + offset)
            pointer = rom.read(2)
            pointer = (2**8 * ord(pointer[1]) + ord(pointer[0]))
            pointer = pointer % 0x8000
            pointers.append(pointer)

            offset += 2

        for pointer in pointers:
            offset = 0
            message = ""
            ONE_01 = 0
            while True:
                if offset and not (pointer + offset) % 0x8000:
                    break

                if offset and pointer + offset in pointers:
                    break

                rom.seek(table + pointer + offset)
                byte = ord(rom.read(1))

                assert type(byte) is int
                message = " ".join([message, "%x" % byte])
                if byte == 0x01:
                    if ONE_01 == 1:
                        break
                    elif ONE_01 == 0:
                        ONE_01 += 1
                elif ONE_01:
                    ONE_01 = 0

                offset += 1

            messages[table + pointer] = message.strip()

    return messages


def char_check(value, lookup=None):
    lookup = lookup or byte2str

    if value[0] == 0x0f:
        return ("\n", value[1:])

    if len(value) != 2:
        return False

    high, low = tuple(value)

    value = (2**8 * high + low)
    if value == 0x0103:
        return "→"
    elif value == 0x0102:
        return "\n\n"
    elif ALL_START <= value <= KANJI_END:
        if value not in lookup:
            return value
        else:
            return lookup[value]
    else:
        return False


def gen_formatted(message, lookup=None):
    if type(message) in [str, unicode]:
        message = map(lambda w: int(w, 16), message.strip().split())

    formatted = u""
    skip_next = False
    unknown = defaultdict(int)
    for n, _ in enumerate(message):
        if skip_next:
            skip_next = False
            continue

        me = message[n:n+2]
        mechar = char_check(message[n:n+2], lookup)
        if mechar:
            lnext = message[n+1:n+3]
            mnext = message[n+2:n+4]
            rnext = message[n+3:n+5]
            if (char_check(lnext, lookup) != False and
                    char_check(rnext, lookup) != False and
                    char_check(mnext, lookup) == False):
                continue
            if type(mechar) is tuple:
                formatted = formatted + mechar[0]
                continue
            elif type(mechar) is int:
                if formatted and formatted[-1] not in [' ', '\n']:
                    formatted += " "
                formatted += "0x%x 0x%x " % tuple(me)
                unknown[mechar] += 1
            else:
                if type(mechar) is str:
                    mechar = mechar.decode('utf-8')
                formatted += mechar
            skip_next = True
        else:
            if formatted and formatted[-1] not in [' ', '\n']:
                formatted += " "
            formatted += "0x%x " % me[0]
    return formatted.replace(" \n", "\n").strip(), unknown


if __name__ == "__main__":
    pass
