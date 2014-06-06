import manage
from kyuuyaku.models import *
from os import system

KANJI_LIST = "specialkanji/found_kanji.txt"
KANJI_PER_IMAGE = 40
SEG_PER_IMAGE = 10
KANJI_PER_SEG = 4

Char.objects.all().delete()
CharBlock.objects.all().delete()
CharBlockChar.objects.all().delete()
CharBlockOCR.objects.all().delete()

klist = [int(i.strip(), 16) for i in open(KANJI_LIST)]
counter = 0


def reorg_ocr(output):
    a, b, ret = output[:5], output[5:], []
    for x, y in zip(a, b):
        ret += [x, y]
    return ret


while klist:
    charblock = CharBlock(image="kanji%s.png" % str(counter).zfill(3))
    charblock.save()
    kblock, klist = klist[:KANJI_PER_IMAGE], klist[KANJI_PER_IMAGE:]
    for n, k in enumerate(kblock):
        char = Char(code=k)
        char.save()
        segment, location = (n / KANJI_PER_SEG), (n % KANJI_PER_SEG)
        CharBlockChar(block=charblock, char=char,
                      segment=segment, location=location).save()

    system("tesseract specialkanji/kanji%s.png output -l jpn"
           % str(counter).zfill(3))
    output = [line.strip() for line in open("output.txt") if line.strip()]
    output = reorg_ocr(output[-1*SEG_PER_IMAGE:])
    for n, line in enumerate(output):
        CharBlockOCR(block=charblock, segment=n, text=line).save()

    counter += 1
