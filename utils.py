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

# 0x28000
POINTER_TABLES = [0x80000,
                  0x88000,
                  0x90000,
                  0x98000,
                  0x158000]


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


if __name__ == "__main__":
    pass
