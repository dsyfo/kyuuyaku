from sys import argv
from utils import int2ints
from shortutils import str2byte, byte2str
from dumpshort import get_messages


def rewrite_names(outfile, translations, tableaddress):
    messages = get_messages(outfile, tableaddress)
    outfile.seek(tableaddress)
    previously = {}
    namesaddress = len(messages)*2 + tableaddress
    print "%x %x" % (tableaddress, namesaddress)

    changed = 0
    for message in messages:
        message = "".join(map(chr, message))
        outfile.seek(tableaddress)
        if message in previously:
            outfile.write(previously[message])
        else:
            pointer = 0x8000 | (namesaddress & 0xffff)
            pointer = int2ints(pointer, 2)
            pointer = "".join(map(chr, pointer))
            previously[message] = pointer
            outfile.write(pointer)

            outfile.seek(namesaddress)
            decoded = "".join(map(lambda c: byte2str[ord(c)], message))
            if decoded in translations:
                message = translations[decoded].upper()
                message = "".join(map(lambda c: chr(str2byte[c]), message))
                changed += 1
            message = "".join(message)
            message += chr(0)
            outfile.write(message)
            namesaddress += len(message)

        tableaddress += 2

    print "%x %x" % (tableaddress, namesaddress)
    print "%s changed" % changed


if __name__ == "__main__":
    outfile = open(argv[1], 'r+b')
    translations = dict([l.strip().split(' ') for l in open(argv[2]).readlines()])
    address = int(argv[3], 16)
    rewrite_names(outfile, translations, address)
