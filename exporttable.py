import manage
from kyuuyaku.models import *

for char in Char.objects.exclude(value=None).order_by("code"):
    print char.value.encode('utf-8'), "%x" % char.code
