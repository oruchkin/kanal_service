from split_settings.tools import include
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

include(
    'components/auth_password_validators.py',
    'components/database.py',
    'components/installed_apps.py',
    'components/middleware.py',
    'components/templates.py',
) 

DEBUG = True
ALLOWED_HOSTS = ["*"]

SECRET_KEY = 'django-insecure-(gy%az5f)!x4%@h&u4#8)+2tujn@%5&1n(kj_yh^xb@si664)n'
BASE_DIR = Path(__file__).resolve().parent.parent
ROOT_URLCONF = 'kanal.urls'
WSGI_APPLICATION = 'kanal.wsgi.application'
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'