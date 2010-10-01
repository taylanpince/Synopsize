import os
import sys
import site

site.addsitedir('/home/snopsizeteam/sites/snopsize/lib/python2.6/site-packages')

sys.path.append("/home/snopsizeteam/sites/snopsize/src/snopsize/build")
sys.path.append("/home/snopsizeteam/sites/snopsize/src/snopsize/build/snopsize")

os.environ["DJANGO_SETTINGS_MODULE"] = "snopsize.settings"

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
