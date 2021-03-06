"""
Django settings for bootstraplearn project.

Generated by 'django-admin startproject' using Django 3.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'u($0c(t^7@dds0hn_q$uiw546u*3v)ylk$s=0%ncwunq^9#ow9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'App'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'middleware.UserAuthMiddle.UserAuthMiddle',
]

ROOT_URLCONF = 'bootstraplearn.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bootstraplearn.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


CACHES = {
    'default': {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 引擎（默认）
SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名（默认）
SESSION_COOKIE_SECURE = False  # 是否Https传输cookie（默认）
SESSION_COOKIE_HTTPONLY = True  # 是否Session的cookie只支持http传输（默认）
SESSION_COOKIE_AGE = 1209600  # Session的cookie失效日期（2周）（默认）
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 是否关闭浏览器使得Session过期（默认）
SESSION_SAVE_EVERY_REQUEST = False  # 是否每次请求都保存Session，默认修改之后才保存（默认）


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS =[
    os.path.join(BASE_DIR, 'static')
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/upload')

RSA_PUBLIC_KEY = '''-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAu8ubZLdThmWypavbdD1p
mcgDntGDR3xECQ9LUGis9eXFzGm6/j3rLXTF4NbGUv8MN0PNcOwnREILLOmt/yrH
0fzcF6JkRxFL9COFteJYLf8lvzw0MVBtw/BVemaA4KS8gIekct2ZyvCKuKvYWQ9o
k3zIZCl5IhCsGSVrgffSDMkYNN9x5+lpZkRlZmNLVU1WQ44zg1sz4vQKkw5YsBbC
lwg3m24SVsEKGzQXTEJpTrAejCRG7+goZALaJUCnZHv1dzD5JPGYwIQCJNHcRoGB
MMQ3fYvh7pgi3A2+eX6tVHZv4I07Mg8lBn+RtAEQteKB3TiEzum3tKSOfXzlYUEl
kQIDAQAB
-----END PUBLIC KEY-----'''
RSA_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAu8ubZLdThmWypavbdD1pmcgDntGDR3xECQ9LUGis9eXFzGm6
/j3rLXTF4NbGUv8MN0PNcOwnREILLOmt/yrH0fzcF6JkRxFL9COFteJYLf8lvzw0
MVBtw/BVemaA4KS8gIekct2ZyvCKuKvYWQ9ok3zIZCl5IhCsGSVrgffSDMkYNN9x
5+lpZkRlZmNLVU1WQ44zg1sz4vQKkw5YsBbClwg3m24SVsEKGzQXTEJpTrAejCRG
7+goZALaJUCnZHv1dzD5JPGYwIQCJNHcRoGBMMQ3fYvh7pgi3A2+eX6tVHZv4I07
Mg8lBn+RtAEQteKB3TiEzum3tKSOfXzlYUElkQIDAQABAoIBAAUCoyQ2Qeu5heEm
qyW4R7t7GyGfHF4JYjVNq6g7CrZKyZKxFXSYCVC+p1Le2A650EUfMXl8S3XmPy8V
EvfWV9tx4BtfUUaWHw0l73jRT6H2hzbJb+kK6MrL/DPWTUTxEDhrpgcMg4BnF4Ri
zVRe9V7N+vi1JI60nCrVlT8z8e42WYwO9d/1TBYP/rTqC7F83P59WmqKJ3chNPF0
vL0JQxZ/NJwluwj32aZ2EUvPgp9qEfzxPPK2MQxVMRDeX4D/rLnMud75S0HgJGMh
fIpJvjrKZvMxaACAQ8IuMUFiDbcU2zYUSn1VWzc9qMwgvfkY9ChC9JepUGh5TX8N
WTU67usCgYEAy44BeOQf7zgR69KrH4ZmCG9fgDeu2j/TkEz3snF8LZ8OjlQ/YF7R
i/gHw0BdtSW/+73JtIAFrnJkK4HZ8Hu+RH3ddIMXqgrC6d8nEQMLyb7T0HybTW4j
omaHUt8zITkvIV0G5UsC52SgVI8f9N/ECQXUbCRFiXTNRuHBJufhYQMCgYEA7C4m
YgDoJNfgOcFKIJpVaGyLr25vg/tQfWXVUk+WZBpEBcIeMn0KRMWVoiy3w+kAVCUR
v5y9P/YfnLGvbSL8isOscBr7f/+PbEWvhv7l3W8Qk91iBS3EVMNsS5nPhcqFtU3K
oFWcYBkRrAIskaXQZcbBv2ltx1p0+A4abxuTuNsCgYAcWEvwL6Qaxa4JLq7Rlv+C
US/1RMu+bIDjaTRcztzB5ZI7U5P3sXxwhztdfwsNfJI9VfJOhj1ES32TaWOVz0Vx
eC1sWgzjitgVhROFlO0BTOdl8tQVdi7UIH7blWUjTTk45iFdsJJY8nQ5Ei0bBkXg
E8W+wVZFi9RB+JHS/xstTQKBgQC75ouK9QW8KjOuP2VmQuMoTRNk4wu9iTgkS9xH
vCH+ShdMLYAw0uJUjI3blJAvQTSNvWA9fcnjFUFZPNRAk9Ev5TVPi2gEEaJdlaNs
V2cxoKcjvMG7NQo6FbAXBavg2Zs+/0DyBqp+mfNBUgl7ZtxB3LtQOeSo8gKVR0Mo
mlwQeQKBgQCZ9dkM9y5P7c1JY/9nTz7f0pq8b8bZKHHuD/GEpqk++NBXDH9QXe16
8gCRLiKjFTAbpuXnoREpou0aqMEims+TJe2NuPnBusNT1fHaIgDlHOYVBpCQABRx
oXNLOM/1jH2L6I6NOO7vTXX8rxoelYsGFXz8R1cTjHg2E/v0LCwtag==
-----END RSA PRIVATE KEY-----'''