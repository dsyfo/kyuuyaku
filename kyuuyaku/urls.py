from django.conf.urls import patterns, include, url
import settings

from kyuuyaku.views import voteblock, votemessage

urlpatterns = patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        url(r'^voteblock/', voteblock),
        url(r'^votemessage/', votemessage),
)
