import manage
from kyuuyaku.models import *
from utils import get_messages, byte2str

for address, message in get_messages().items():
    if not Message.objects.filter(data=message) | Message.objects.filter(pointer=address):
        Message(pointer=address, data=message).save()

for code, value in byte2str.items():
    chars = Char.objects.filter(code=code)
    if chars.exists():
        char = chars[0]
    else:
        char = Char(code=code)
        char.save()
    if not CharVote.objects.filter(ip=0,char=char,value=value):
        CharVote(ip=0, char=char, value=value).save()
