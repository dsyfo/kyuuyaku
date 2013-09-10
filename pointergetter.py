# -*- coding: utf-8 -*-
from utils import str2byte, byte2str, known_ranges
from collections import defaultdict
ALL_START = 0x8141
KANJI_START = 0x889f
KANJI_END = 0x9872

rom = open("kyuuyaku_megami_tensei_clean.sfc", "rb")
# 0x28000
POINTER_TABLES = [0x80000,
                  0x88000,
                  0x90000,
                  0x98000,
                  0x158000]

messages = {}
kanji = set([])
unknown = defaultdict(int)

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
        message = []
        ONE_01 = 0
        while True:
            if offset and not (pointer + offset) % 0x8000:
                break

            if offset and pointer + offset in pointers:
                break

            rom.seek(table + pointer + offset)
            byte = ord(rom.read(1))

            assert type(byte) is int
            message.append(byte)
            if byte == 0x01:
                if ONE_01 == 1:
                    break
                elif ONE_01 == 0:
                    ONE_01 += 1
            elif ONE_01:
                ONE_01 = 0

            offset += 1

        messages[table + pointer] = message


def is_a_char(value):
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
    elif ALL_START < value < KANJI_END:
        if value not in byte2str:
            return value
        else:
            return byte2str[value]
    else:
        return False


f = open("output.txt", "w")
for address, message in sorted(messages.items()):
    f.write("0x%x\n--------\n" % address)
    skip_next = False
    formatted = ""
    for n, _ in enumerate(message):
        if skip_next:
            skip_next = False
            continue

        me = message[n:n+2]
        mechar = is_a_char(message[n:n+2])
        if mechar:
            lnext = message[n+1:n+3]
            mnext = message[n+2:n+4]
            rnext = message[n+3:n+5]
            if is_a_char(lnext) != False and is_a_char(rnext) != False:
                if is_a_char(mnext) == False:
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
                formatted += mechar
            skip_next = True
        else:
            if formatted and formatted[-1] not in [' ', '\n']:
                formatted += " "
            formatted += "0x%x " % me[0]

    f.write(formatted.replace(" \n", "\n").strip())
    f.write("\n\n--------\n")

for char, count in sorted(unknown.items(), key=lambda (x,y): y, reverse=True):
    f.write(("%x" % char).zfill(4) + " %d\n" % count)
f.write('\n')
for char, count in sorted(sorted(unknown.items(), key=lambda (x,y): y, reverse=True)[:10]):
    f.write(("%x" % char).zfill(4) + " %d\n" % count)
