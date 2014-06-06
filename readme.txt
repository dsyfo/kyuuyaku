Anyway, here’s an example command line for the dumper:
`python dumpshort.py kyuuyaku_megami_tensei_clean.sfc 0x158000 2`

This tells the script to start at address 0x158000 and use a character size of 2 bytes.

Characters either take up 1 byte or 2 bytes each. 2-byte characters are used for dialogue, and 1-byte characters are used for item/spell names, etc. The values of the characters are stored in `table.txt` and `shorttable.txt`, respectively. There’s also a file called `shortwritetable.txt` which I used because I wanted to use different characters for writing for some reason?

You can write tables for translating item names using the format in `equips.txt`, `spells.txt`, `demons.txt`, etc. There’s a file called `translate.sh` which contains lines like:

`python wumpshort.py kyuuyaku_megami_tensei.sfc equips.txt 88dac pad`

This tells the script to search the rom, starting at 0x88dac, for equipment names matching the japanese text in equips.txt, and substitute them for the english names. I believe “pad” is there because 0x88dac is probably the address of a shop, so it is necessary to pad the width of the substituted text to preserve the formatting in the dialogue box. I don’t think I wrote a companion script for dialogue, but this one might work, if not for the aforementioned control code issue.

If you want a complete dump of all the dialogue, there’s a script called `pointergetter.py`. Just run it and it will dump everything into a file called `output.txt`. It’s not perfect, I think it outputs a lot of garbage as well, but I never figured out what all of the control codes do, so I just dumped the raw hex for any unknown codes.

`tileget.py`, `tileset.py`, and `halffontutils.py` were all written to help with replacing the existing font with my half-width font. I don’t remember how far I got but I never saw that as being a huge obstacle.

`utils.py` contains miscellaneous utilities for use in the other modules. Things like, converting a 2-byte integer into two 1-byte integers, mapping from a hex code to a unicode character, etc

`replacer.py` isn’t useful, it just fills a dialogue box with incrementing values. I used it to see how the kanji were ordered in the game’s data, but now there is a full table in the repo. I have no idea what `doubledemoner.py` was supposed to do. The commit message reads, “added tool to distribute demon names across various sections of bank”, which is like, WHOA! That sounds cool! Did I really write that?

You can ignore any of the django stuff. That is super obsolete, and honestly, I don’t think it was ever necessary.

Anyway, the utility that does the heavy lifting in most situations is `utils.get_messages`, and it looks pretty short, so if you need to do some reverse engineering that’s a good place to look. You can see right away how it partitions the rom into 0x8000-length sections, which is the size of one bank.
