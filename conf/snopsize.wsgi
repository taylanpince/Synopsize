import os
import sys
import site

site.addsitedir('/home/snopsizeteam/sites/synopsize/lib/python2.6/site-packages')

sys.path.append("/home/snopsizeteam/sites/synopsize/src/synopsize/build")
sys.path.append("/home/snopsizeteam/sites/synopsize/src/synopsize/build/synopsize")

os.environ["DJANGO_SETTINGS_MODULE"] = "synopsize.settings"

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
