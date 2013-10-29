from sys import argv
from utils import int2ints, hexify
from shortutils import str2byte, byte2str
from dumpshort import get_messages

for char in str2byte.keys():
    if char.lower() not in str2byte:
        str2byte[char.lower()] = str2byte[char]
    if char.upper() not in str2byte:
        str2byte[char.upper()] = str2byte[char]

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
            print decoded, len(message)
            if decoded in translations:
                message = translations[decoded].upper()
                message = "".join(map(lambda c: chr(str2byte[c]), message))
                changed += 1
            else:
                for key in sorted(translations, key=lambda x: len(x), reverse=True):
                    if key in decoded:
                        index = decoded.find(key)
                        translation = translations[key]
                        length = len(key.decode('utf8'))
                        if len(translation) < length:
                            translation += ' ' * (length - len(translation))
                        translation = "".join(map(lambda c: chr(str2byte[c]), translation))
                        message = message[:index] + translation + message[index + len(translation):]
                        changed += 1
                        break
            message = "".join(message)
            decoded = "".join(map(lambda c: byte2str[ord(c)], message))
            print decoded, len(message)
            message += chr(0)
            outfile.write(message)
            namesaddress += len(message)

        tableaddress += 2

    print "%x %x" % (tableaddress, namesaddress)
    print "%s changed" % changed


if __name__ == "__main__":
    outfile = open(argv[1], 'r+b')
    translations = {}
    for line in open(argv[2]):
        while '  ' in line:
            line = line.replace('  ', ' ')
        line = line.strip().split(' ')
        if len(line) < 2:
            continue
        translations[line[0].strip()] = line[1].strip()

    address = int(argv[3], 16)
    rewrite_names(outfile, translations, address)
