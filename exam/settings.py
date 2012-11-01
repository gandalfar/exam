from localsettings import *
import os
here = lambda x: os.path.join(os.path.dirname(os.path.abspath(__file__)), x)

ADMINS = (
    ('Jure', 'gandalfar@gmail.com'),
)

MANAGERS = ADMINS

# Local time zone for this installation. All choices can be found here:
# http://www.postgresql.org/docs/current/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
TIME_ZONE = 'Europe/Ljubljana'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'sl-si'

SITE_ID = 1

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/admin-media/'
MEDIA_ROOT = 'exam/media/'

MEDIA_URL = '/exam/media/'
STATIC_URL = '/exam/media/'

ROOT_URLCONF = 'exam.urls'

TEMPLATE_DIRS = (
    'exam/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'exam.calc',
)

AUTH_PROFILE_MODULE = 'calc.UserProfile'

EMAIL_SUBJECT_PREFIX = "[FDVexam]"
SERVER_EMAIL = "jure.cuhalev@guest.arnes.si"

SESSION_EXPIRE_AT_BROWSER_CLOSE = True
