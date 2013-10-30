from sys import argv
from wumpshort import rewrite_names

if __name__ == "__main__":
    from shortutils import byte2str, write2byte
    for char in write2byte.keys():
        if char.lower() not in write2byte:
            write2byte[char.lower()] = write2byte[char]
        if char.upper() not in write2byte:
            write2byte[char.upper()] = write2byte[char]

    outfile = open(argv[1], 'r+b')
    translations = {}
    for line in open(argv[2]):
        while '  ' in line:
            line = line.replace('  ', ' ')
        line = line.strip().split(' ')
        if len(line) < 2:
            continue
        translations[line[0].strip()] = line[1].strip()

    freefile = open(argv[3])
    f = lambda x: int(x, 16)
    free = [tuple(map(f, line.strip().split())) for line in freefile.readlines()]

    order = [0x8d5a8, 0x8cdfd]
    #order = [0x8cdfd, 0x8d5a8]
    #8cff7 8d5a7
    #8d6c6 8d9e4
    #8d9e5
    previously=None
    for address in order:
        free, previously = rewrite_names(outfile, translations, address, previously=previously,
                                         coders=(byte2str, write2byte, 1), free=free, pad=None)
