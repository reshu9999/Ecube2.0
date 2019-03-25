"""
WSGI config for eCube_UI_2 project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Apache Conf #

# Uncomment below for Production
import sys
sys.path.append('/var/www/eCube_Hotel_2/eCube_UI_2')
os.environ['DJANGO_SETTINGS_MODULE'] = 'eCube_UI_2.settings'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
# end uncomment

# Comment below for Production
#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eCube_UI_2.settings")
# end comment

# end Apache Conf #

application = get_wsgi_application()
