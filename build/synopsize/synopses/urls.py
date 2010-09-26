from django.conf.urls.defaults import *


urlpatterns = patterns('synopses.views',
    url(r'^$', 'list_synopsis', name='synopses_list_synopsis'),
    url(r'^create/$', 'create_synopsis', name='synopses_create_synopsis'),
    url(r'^(?P<synopsis_id>[0-9]+)/$', 'detail_synopsis', name='synopses_detail_synopsis'),
    url(r'^(?P<synopsis_id>[0-9]+)/update/$', 'update_synopsis', name='synopses_update_synopsis'),
    url(r'^(?P<synopsis_id>[0-9]+)/delete/$', 'delete_synopsis', name='synopses_delete_synopsis'),
)
