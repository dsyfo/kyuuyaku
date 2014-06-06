# -*- coding: utf-8 -*-
import manage
from kyuuyaku.models import *
from utils import get_messages

Message.objects.all().delete()
for pointer, message in sorted(get_messages().items()):
    Message(pointer=pointer, data=message).save()
