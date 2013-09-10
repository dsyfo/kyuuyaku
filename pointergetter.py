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

f = open("output.txt", "w")
for address, message in sorted(messages.items()):
    f.write("0x%x\n" % address)
    formatted = ""
    last_char = None
    for m in message:
        if last_char:
            temp = (2**8 * last_char + m)
            if ALL_START < temp < KANJI_END and temp not in byte2str:
                unknown[temp] += 1

            if temp == 0x0103:
                formatted += "→"
                last_char = None
            elif temp == 0x0102:
                formatted += "\n\n"
                last_char = None
            elif any(map(lambda (x, y): x <= temp <= y, known_ranges)):
                k = byte2str[temp]
                formatted += k
                last_char = None
            else:
                if formatted and formatted[-1] not in " \n":
                    formatted += " "
                formatted += "0x" + ("%x" % last_char).zfill(2) + " "
                last_char = m
        elif m ==  0x0f:
            formatted += "\n"
            last_char = None
        else:
            last_char = m

    formatted = formatted.strip()
    f.write(formatted)
    f.write("\n\n")

for char, count in sorted(unknown.items(), key=lambda (x,y): y, reverse=True):
    f.write(("%x" % char).zfill(4) + " %d\n" % count)
f.write('\n')
for char, count in sorted(sorted(unknown.items(), key=lambda (x,y): y, reverse=True)[:10]):
    f.write(("%x" % char).zfill(4) + " %d\n" % count)
