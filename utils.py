# -*- coding: utf-8 -*-
from collections import defaultdict

ALL_START = 0x8140
KANJI_START = 0x889f
KANJI_END = 0x9872
MIN_UNICODE_KANJI = u"\u4e00"
MAX_UNICODE_KANJI = u"\u9faf"

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

found_kanji = [int(x.strip(), 16) for x in open("all_kanji.txt")]

# 0x28000
POINTER_TABLES = [0x80000,
                  0x88000,
                  0x90000,
                  0x98000,
                  0x158000]


def is_kanji(value):
    return KANJI_START <= ord(value) <= KANJI_END


def is_unicode_kanji(char):
    if MIN_UNICODE_KANJI <= char <= MAX_UNICODE_KANJI:
        return True
    else:
        return False


def is_a_char(value):
    return ALL_START <= ord(value) <= KANJI_END


def get_messages():
    rom = open("kyuuyaku_megami_tensei_clean.sfc", "rb")
    messages = {}
    for table in POINTER_TABLES:
        rom.seek(table)
        assert not table % 0x8000
        pointer = 0
        message = ""
        CONSEC_01 = 0
        while True:
            offset = rom.tell() - table
            if offset and offset >= 0x8000:
                break

            byte = ord(rom.read(1))

            if byte != 0x01:
                if CONSEC_01 >= 2:
                    if pointer > 0x8000:
                        pointer = pointer & 0x7fff
                    if pointer > 0:
                        messages[table + pointer] = message.strip()
                    message = ""
                    pointer = offset
            message = " ".join([message, "%x" % byte])

            if byte == 0x01:
                CONSEC_01 += 1
            else:
                CONSEC_01 = 0

    return messages


def char_check(value, lookup=None):
    lookup = lookup or byte2str

    if len(value) < 1:
        return False

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
    formatted = formatted.replace(" \n", "\n").split("\n")
    formatted = [line for line in formatted if any(0x3040 <= ord(c) <= 0x30ff for c in line)]
    return "\n".join(formatted).strip(), unknown


def ints2int(data, bigend=True):
    data = list(data)
    if bigend:
        data.reverse()
    value = 0
    for d in data:
        value = (value << 8) | d
    return value


def int2ints(value, size, bigend=True):
    data = []
    for i in range(size):
        data.append(value & 0xff)
        value = value >> 8
    if not bigend:
        data.reverse()
    return data


def hexify(data, pad=None):
    if pad:
        h = lambda n: ("{0:0>%s}" % pad).format("%x" % n)
    else:
        h = lambda n: "%x" % n

    try:
        if type(data) in (list, tuple):
            return map(h, data)
        else:
            return h(data)
    except TypeError:
        return None


if __name__ == "__main__":
    pass
