from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from kyuuyaku.models import Char, CharBlockOCR, CharVote, Message, MessageVote

from random import choice


def is_unicode_kanji(value):
    return 0x3400 <= ord(value) <= 0x9fa0


def voteblock(request, num=None):
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

    if not num:
        char = Char.get_lowvote_char()
    else:
        try:
            num = int(num, 16)
            char = Char.objects.get(code=num)
        except (ValueError, Char.DoesNotExist):
            return HttpResponseRedirect("/vote/block")

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


def votemessage(request, num=None):
    if request.method == 'POST':
        if 'text' in request.POST:
            text = request.POST['text'].strip()
            ip = request.META.get('HTTP_X_FORWARDED_FOR')
            if ip:
                ip = ip.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            message = request.session['message']
            if not MessageVote.objects.filter(ip=ip, message=message):
                MessageVote(ip=ip, message=message, translation=text).save()
            else:
                mv = MessageVote.objects.get(ip=ip, message=message)
                mv.translation = text
                mv.save()

        return HttpResponseRedirect(".")

    if not num:
        message = Message.get_lowvote_message()
    else:
        try:
            num = int(num, 16)
            message = Message.objects.get(pointer=num)
        except (ValueError, Message.DoesNotExist):
            return HttpResponseRedirect("/vote/message")

    request.session['message'] = message
    formatted, unknowns = message.info
    data = RequestContext(request,
            {'formatted': formatted,
             'unknowns': sorted(["%x" % u for u in unknowns]),
             'pointer': "%x" % message.pointer,
             'translation': message.get_translation()})
    return render_to_response('votemessage.html', data)
