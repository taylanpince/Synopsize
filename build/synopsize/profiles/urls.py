from django.conf.urls.defaults import *


urlpatterns = patterns('profiles.views',
    url(r'^profiles/$', 'profile_landing', name='profiles_profile_landing'),
    url(r'^profiles/(?P<username>[-\w]+)/$', 'profile', name='profiles_profile'),
    url(r'^account/favorites/add/(?P<synopsis_id>[0-9]+)/$', 'favorites_add', name='profiles_favorites_add'),
    url(r'^account/favorites/remove/(?P<synopsis_id>[0-9]+)/$', 'favorites_remove', name='profiles_favorites_remove'),
    url(r'^account/edit/$', 'profile_edit', name='profiles_profile_edit'),
    url(r'^account/register-or-login/$', 'register_or_login', name='profiles_register_or_login'),
    url(r'^account/logout/$', 'logout', name='profiles_logout'),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^account/password/reset/$', 'password_reset', name="profiles_password_reset"),
    url(r'^account/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'password_reset_confirm', name="profiles_password_reset_confirm"),
    url(r'^account/password/reset/complete/$', 'password_reset_complete', name="profiles_password_reset_complete"),
    url(r'^account/password/reset/done/$', 'password_reset_done', name="profiles_password_reset_done"),
    url(r'^account/password/change/$', 'password_change', name="profiles_password_change"),
    url(r'^account/password/change/done/$', 'password_change_done', name="profiles_password_change_done"),
)
