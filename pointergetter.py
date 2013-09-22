# -*- coding: utf-8 -*-
from utils import get_messages, gen_formatted
from collections import defaultdict

kanji = set([])
unknown = defaultdict(int)

f = open("output.txt", "w")
for address, message in sorted(get_messages().items()):
    if len(message) < 3:
        continue

    message = [int(m, 16) for m in message.split()]

    formatted, unk = gen_formatted(message)
    if len(formatted) < 2:
        continue

    f.write("0x%x\n--------\n" % address)
    for key, value in unk.items():
        if value:
            unknown[key] += value
    f.write(formatted.encode('utf-8'))
    f.write("\n\n--------\n")

for char, count in sorted(unknown.items(), key=lambda (x,y): y, reverse=True):
    f.write(("%x" % char).zfill(4) + " %d\n" % count)
f.write('\n')
for char, count in sorted(sorted(unknown.items(), key=lambda (x,y): y, reverse=True)[:10]):
    f.write(("%x" % char).zfill(4) + " %d\n" % count)
