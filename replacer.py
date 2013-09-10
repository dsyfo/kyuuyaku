from utils import str2byte, found_kanji

seek = 0x15aa5b
portrait = 0x07040000
newline = 0x0f
button = 0x0103
new_win = 0x0102

found_kanji.sort(reverse=True)
f = open("kyuuyaku_megami_tensei.sfc", "r+b")


def pop_found_kanji():
    global found_kanji
    if found_kanji:
        return found_kanji.pop()
    else:
        return 0x8260


def write_it(val, size=2):
    global seek, f

    to_write = []
    while val > 0xff:
        to_write.append(val & 0xff)
        val = val >> 8
    to_write.append(val & 0xff)

    while len(to_write) < size:
        to_write.append(0x00)

    if len(to_write) != size:
        raise Exception("Size not good.")

    to_write.reverse()
    for byte in to_write:
        f.write(chr(byte))
    seek += len(to_write)


f.seek(seek)
value = 0x8700
#value = pop_found_kanji()
while True:
    write_it(button, 2)
    write_it(new_win, 2)
    if (seek % 0x8000) >= 0x7E00:
        break

    for i in range(5):
        row = "%x" % (value & 0xfff)
        for c in row.zfill(3):
            write_it(str2byte[c], 2)

        if seek < 0x15ae5b:
            for j in range(9):
                write_it(str2byte['Z'], 2)
        else:
            write_it(str2byte['z']+1, 2)
            for j in range(4):
                write_it(value, 2)
                value += 1
                #value = pop_found_kanji()
            write_it(str2byte['z']+1, 2)
            for j in range(4):
                write_it(value, 2)
                value += 1
                #value = pop_found_kanji()
        write_it(newline, 1)

write_it(0x0101, 2)
f.close()
print "%x" % value
