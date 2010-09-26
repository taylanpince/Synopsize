from django.conf.urls.defaults import *
from django.contrib import admin


admin.autodiscover()


urlpatterns = patterns('',
    # Admin
    (r'^admin/', include(admin.site.urls)),
    
    # Profiles (account / profiles)
    (r'^', include("profiles.urls")),
)

urlpatterns += patterns('django.views.generic.simple',
    # Home
    url(r"^$", "direct_to_template", {
        "template": "home.html",
    }, name="home"),
)
