from sys import argv
from utils import ints2int, hexify


def get_messages(infile, tableaddress, charsize=1):
    pointers = []
    bank = tableaddress & 0xffff8000
    infile.seek(tableaddress)
    while True:
        if pointers and infile.tell() >= min(pointers):
            break
        pointer = ints2int(map(ord, infile.read(2))) & 0x7fff
        pointers.append(pointer + bank)

    messages = []
    for pointer in pointers:
        infile.seek(pointer)
        message = []
        while True:
            data = map(ord, infile.read(charsize))
            if data[0] == 0:
                break
            else:
                data = ints2int(data, bigend=False)
                message.append(data)
        messages.append(message)

    return messages


if __name__ == "__main__":
    infile = open(argv[1], 'rb')
    address = int(argv[2], 16)
    charsize = int(argv[3]) if len(argv) > 3 else 1
    messages = get_messages(infile, address, charsize=charsize)

    if charsize == 1:
        from shortutils import byte2str
    else:
        from utils import byte2str

    for m in messages:
        m = "".join(map(lambda c: byte2str[c] if c in byte2str else '*', m))
        print m
