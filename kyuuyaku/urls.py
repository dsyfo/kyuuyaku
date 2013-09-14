from django.conf.urls import patterns, include, url
import settings

from kyuuyaku.views import voteblock, votemessage, listblock, listmessage

urlpatterns = patterns('',
        url(r'block/vote/(\w*)$', voteblock),
        url(r'block/vote/?$', voteblock),
        url(r'block/?$', listblock),
        url(r'message/vote/(\w*)$', votemessage),
        url(r'message/vote/?$', votemessage),
        url(r'message/?$', listmessage),
)

if settings.DEBUG:
    urlpatterns += patterns('',
            url(r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
                {'document_root': settings.MEDIA_ROOT}),
    )
