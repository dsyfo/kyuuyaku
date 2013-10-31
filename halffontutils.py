from tileset import convert_line, write_tiles
FONT = "AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz"
FONT_FILE = "kyuuyaku_half_font.ppm"
HEIGHT = 12
WIDTH = 6


def load_letters(filename):
    data = open(filename).readlines()[4].strip()
    data = convert_line(data)
    numtiles = len(data) / (HEIGHT*WIDTH)
    assert len(data) % HEIGHT == 0
    assert len(data) % WIDTH == 0
    data = [data[i:i+WIDTH] for i in range(0, len(data), WIDTH)]
    tiles = [data[i:] for i in range(0, len(data), numtiles)]
    tiles = zip(*tiles)
    font_dict = dict(zip(FONT, tiles))
    return font_dict


def pair_up(a, b, font_dict):
    f = lambda (x, y): x + y
    return map(f, zip(font_dict[a], font_dict[b]))


def make_pair_tiles(text, font_dict):
    pairs = set([])
    for line in text.split('\n'):
        if not line:
            continue
        if len(line) % 2:
            line += ' '
        for pair in [line[i:i+2] for i in range(0, len(line), 2)]:
            pairs.add(tuple(pair))

    pair_tiles = [pair_up(a, b, font_dict) for a, b in pairs]
    pair_tiles = dict(zip(pairs, pair_tiles))
    return pair_tiles


if __name__ == "__main__":
    font_dict = load_letters(FONT_FILE)
    pair_tiles = make_pair_tiles("HelloEveryoneHowAreYou", font_dict)
    tiles = [pair_tiles[key] for key in sorted(pair_tiles)]
    write_tiles(tiles)
