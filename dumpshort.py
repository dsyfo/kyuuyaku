from sys import argv
from utils import ints2int, hexify
from shortutils import byte2str


def get_messages(infile, tableaddress):
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
            data = ord(infile.read(1))
            if data == 0:
                break
            else:
                message.append(data)
        messages.append(message)

    return messages


if __name__ == "__main__":
    infile = open(argv[1], 'rb')
    address = int(argv[2], 16)
    messages = get_messages(infile, address)
    for m in messages:
        m = "".join(map(lambda c: byte2str[c] if c in byte2str else '*', m))
        print m
