addresses = [0x1e8000, 0x1f0000, 0x1f8000]
bank_size = 0x8000
tile_size = 0x18  #bytes
tiles_per_bank = (bank_size / tile_size)
width = 12
height = width
columns = 37
rows = 37 * len(addresses)
offset = 0
filename = "kyuuyaku_megami_tensei_clean.sfc"

if __name__ == "__main__":
    f = open(filename, 'rb')
    print "P3 {0} {1} 1".format(width * columns, height * rows)
    for address in addresses:
        f.seek(address + offset)
        total_tiles = 0
        while total_tiles < tiles_per_bank:
            outrows = ["" for _ in range(height)]
            for x in range(columns):
                for j in range(height):
                    try:
                        a, b = tuple(map(ord, f.read(2)))
                    except ValueError:
                        a, b = 0xff, 0xff
                    data = (a << 8) | b
                    # just throw away extra bits, I guess
                    for i in range(width):
                        if data & 0x8000 or total_tiles >= tiles_per_bank:
                            outrows[j] += "1 1 1 "
                        else:
                            outrows[j] += "0 0 0 "
                        data = data << 1
                total_tiles += 1
            for row in outrows:
                print row.strip()
