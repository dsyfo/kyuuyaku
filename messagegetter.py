# -*- coding: utf-8 -*-
import manage
from kyuuyaku.models import *

rom = open("kyuuyaku_megami_tensei_clean.sfc", "rb")
# 0x28000
POINTER_TABLES = [0x80000,
                  0x88000,
                  0x90000,
                  0x98000,
                  0x158000]

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

Message.objects.all().delete()
for pointer, message in sorted(messages.items()):
    Message(pointer=pointer, data=message).save()
