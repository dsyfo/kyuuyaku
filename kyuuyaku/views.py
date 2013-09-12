from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from kyuuyaku.models import Char, CharBlockOCR, CharVote

from random import choice


def is_unicode_kanji(value):
    return 0x3400 <= ord(value) <= 0x9fa0


def voteblock(request):
    if request.method == 'POST':
        if 'values' in request.POST:
            values = request.POST['values'].strip()
        else:
            values = ""

        if len(values) == 4:
            cbc = request.session['cbc']
            chars = (Char.objects.filter(charblockchar__block=cbc.block,
                                         charblockchar__segment=cbc.segment)
                     .order_by('pk'))
            assert chars.count() <= 4
            ip = request.META.get('HTTP_X_FORWARDED_FOR')
            if ip:
                ip = ip.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            for char, value in zip(chars, request.POST['values']):
                if not is_unicode_kanji(value):
                    continue

                if not CharVote.objects.filter(ip=ip, char=char).exists():
                    CharVote(ip=ip, char=char, value=value).save()
                else:
                    cv = CharVote.objects.get(ip=ip, char=char)
                    cv.value = value
                    cv.save()

        return HttpResponseRedirect(".")

    char = Char.get_lowvote_char()
    cbc = choice(char.charblockchar_set.all())
    block = cbc.block
    try:
        cbocr = CharBlockOCR.objects.get(block=block, segment=cbc.segment)
    except CharBlockOCR.DoesNotExist:
        cbocr = None

    row = (cbc.segment / 2) + 1
    column = "right" if cbc.segment % 2 else "left"

    request.session['cbc'] = cbc
    data = RequestContext(request,
            {'block': block,
             'cbocr': cbocr,
             'row': row,
             'completed': Char.objects.exclude(value=None).count(),
             'total': Char.objects.count(),
             'column': column})

    return render_to_response('voteblock.html', data)
