from sys import argv
from utils import int2ints, hexify
from dumpshort import get_messages

def rewrite_names(outfile, translations, tableaddress, pad=' ',
                  previously=None, coders=None, free=None):
    if coders:
        byte2str, str2byte, charsize = coders
    else:
        from shortutils import byte2str, str2byte
        charsize = 1

    messages = get_messages(outfile, tableaddress, charsize=charsize)
    outfile.seek(tableaddress)
    previously = previously or {}
    namesaddress = len(messages)*2 + tableaddress
    print "%x %x" % (tableaddress, namesaddress)

    changed = 0
    for message in messages:
        message = "".join(map(chr, message))
        outfile.seek(tableaddress)
        if message in previously:
            outfile.write(previously[message])
        else:
            decoded = "".join(map(lambda c: byte2str[ord(c)], message))
            print decoded, len(message)
            if decoded in translations and pad is None:
                message = translations[decoded].upper()
                message = [c.encode('utf8') for c in message.decode('utf8')]
                message = "".join(map(lambda c: chr(str2byte[c]), message))
                changed += 1
            elif pad is not None:
                for key in sorted(translations, key=lambda x: len(x), reverse=True):
                    if key in decoded:
                        index = decoded.find(key)
                        translation = translations[key]
                        length = len(key.decode('utf8'))
                        if len(translation) < length:
                            translation += pad * (length - len(translation))
                        translation = [c.encode('utf8') for c in translation.decode('utf8')]
                        translation = "".join(map(lambda c: chr(str2byte[c]), translation))
                        message = message[:index] + translation + message[index + len(translation):]
                        changed += 1
                        break

            message = "".join(message)
            decoded = "".join(map(lambda c: byte2str[ord(c)], message))
            print decoded, len(message)
            message += chr(0)

            if free is not None:
                namesaddress = None
                for start, end in list(free):
                    if end - start > len(message):
                        namesaddress = start
                        free.remove((start, end))
                        free = [(start + len(message), end)] + free
                        break


            pointer = 0x8000 | (namesaddress & 0xffff)
            pointer = int2ints(pointer, 2)
            pointer = "".join(map(chr, pointer))
            previously[message] = pointer
            outfile.write(pointer)

            outfile.seek(namesaddress)
            outfile.write(message)
            namesaddress += len(message)

        tableaddress += 2

    print "%x %x" % (tableaddress, namesaddress)
    print "%s changed" % changed
    return free, previously


if __name__ == "__main__":
    from shortutils import byte2str, str2byte
    for char in str2byte.keys():
        if char.lower() not in str2byte:
            str2byte[char.lower()] = str2byte[char]
        if char.upper() not in str2byte:
            str2byte[char.upper()] = str2byte[char]

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
    rewrite_names(outfile, translations, address, coders=(byte2str, str2byte, 1))
