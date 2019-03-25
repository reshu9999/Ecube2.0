#! /var/www/venv_services/bin/python3.5

"""
WSGI config for UI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import logging
import sys, os
path = os.path.abspath(__file__)
dir_path = os.path.dirname(path)
sys.path.append(dir_path)

sys.path.insert(0, "/var/www/eCube_Hotel_2/Services/")

# activate_this = 'var/www/venv_services/bin/activate_this.py'
# execfile(activate_this, dict(__file__=activate_this))

from HTMLProcessService import app as application
