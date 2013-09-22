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

        Char.generate_lookup()
        return HttpResponseRedirect("/kyuuyaku/block/vote/")

    if not num:
        char = Char.get_lowvote_char()
    else:
        try:
            num = int(num, 16)
            char = Char.objects.get(code=num)
        except (ValueError, Char.DoesNotExist):
            return HttpResponseRedirect("/kyuuyaku/block/vote/")

    try:
        cbc = choice(char.charblockchar_set.all())
    except IndexError:
        return HttpResponseRedirect("/kyuuyaku/block/vote/")

    block = cbc.block
    try:
        cbocr = CharBlockOCR.objects.get(block=block, segment=cbc.segment)
    except CharBlockOCR.DoesNotExist:
        cbocr = None

    row = (cbc.segment / 2) + 1
    column = "right" if cbc.segment % 2 else "left"

    request.session['cbc'] = cbc
    data = RequestContext(request,
            {'kblock': block,
             'cbocr': cbocr,
             'row': row,
             'completed': Char.objects.exclude(value=None).count(),
             'total': Char.objects.count(),
             'column': column})

    return render_to_response('voteblock.html', data)


def votemessage(request, num=None):
    if request.method == 'POST':
        if 'text' in request.POST and request.POST['text'].strip():
            text = request.POST['text'].strip()[:5000]
            ip = request.META.get('HTTP_X_FORWARDED_FOR')
            if ip:
                ip = ip.split(',')[0]
            else:
                ip = request.META.get('REMOTE_ADDR')

            message = request.session['message']
            MessageVote(ip=ip, message=message, comment=text).save()

        Char.generate_lookup()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'), '.')

    if not num:
        message = Message.get_lowvote_message()
        return HttpResponseRedirect('/kyuuyaku/message/vote/%x' % message.pointer)
    else:
        try:
            num = int(num, 16)
            message = Message.objects.get(pointer=num)
        except (ValueError, Message.DoesNotExist):
            return HttpResponseRedirect("/kyuuyaku/message/vote")

    request.session['message'] = message
    formatted, unknowns, knowns = message.info
    knowns= [(k, "%x" % Char.reverse_lookup[k]) for k in knowns]
    data = RequestContext(request,
            {'formatted': formatted,
             'unknowns': sorted(["%x" % u for u in unknowns]),
             'knowns': knowns,
             'pointer': "%x" % message.pointer,
             'comments': message.messagevote_set.order_by('modified')})
    return render_to_response('votemessage.html', data)


def listblock(request):
    chars = Char.objects.order_by('code')
    data = RequestContext(request, {'chars': chars})
    return render_to_response('listblock.html', data)


def listmessage(request):
    messages = Message.objects.order_by('pointer')
    data = RequestContext(request, {'my_messages': messages})
    return render_to_response('listmessage.html', data)
