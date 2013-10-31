ADDRESSES = [0x1e8000, 0x1f0000, 0x1f8000]
bank_size = 0x8000
tile_size = 0x18  # bytes
tiles_per_bank = (bank_size / tile_size) + 1
width = 12
height = width
columns = 37
numrows = 37 * len(ADDRESSES)
offset = 0
filename = "kyuuyaku_megami_tensei.sfc"
imgname = "tile.ppm"

# NOTE: This program has been hard-coded to work with GIMP's PPM files


def convert_line(line):
    converted = []
    while line:
        if line[:3] == "".join([chr(0xff)]*3):
            converted.append(1)
        else:
            converted.append(0)
        line = line[3:]
    return converted


def write_tiles(tiles, addresses=None):
    if not addresses:
        addresses = ADDRESSES

    f = open(filename, 'r+b')
    for address in addresses:
        f.seek(address)
        # assert len(tiles) >= tiles_per_bank
        for tile in tiles[:tiles_per_bank]:
            assert len(tile) == height
            for rowbyte in tile:
                assert len(rowbyte) == width
                value = 0
                for bit in rowbyte:
                    value = value << 1
                    value |= bit
                value = value << 4
                print value
                f.write(chr(value >> 8))
                f.write(chr(value & 0xff))
        tiles = tiles[columns * columns:]

    f.close()


def get_tiles():
    f = open(imgname)
    f = f.readlines()[-1]
    img = []
    while f:
        img.append(f[:width*columns*3])
        f = f[width*columns*3:]
    rows = []
    while img:
        assert len(img) >= height
        rows.append(img[:height])
        img = img[height:]
    tiles = []
    for row in rows:
        for i, line in enumerate(row):
            row[i] = convert_line(line)
        while row[0]:
            tile = []
            for i, line in enumerate(row):
                tile.append(line[:width])
                row[i] = row[i][width:]
            tiles.append(tile)
    return tiles


if __name__ == "__main__":
    tiles = get_tiles()
    write_tiles(tiles)
