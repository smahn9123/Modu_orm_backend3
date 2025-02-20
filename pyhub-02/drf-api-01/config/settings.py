"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.1.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from environ import Env
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()

ENV_PATH = BASE_DIR / ".env"
if ENV_PATH.is_file():

    # open("hello.txt", "rt",  encoding="utf8").read()  # 한글 윈도우 : cp949, 맥/리눅스 : utf8

    # with ENV_PATH.open("rt", encoding="utf8") as f:
    #     env.read_env(f, overwrite=True)

    env.read_env(ENV_PATH, overwrite=True)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str(
    "SECRET_KEY",
    default="django-insecure-++0w0t9*72(0*1^g0)(r70_qqqor+dke!e-35k_s%z=p9qhc2p",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["127.0.0.1", "localhost"])


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_bootstrap5",
    "django_extensions",
    "corsheaders",
    "rest_framework",
    "accounts",
    "blog",
    "melon",
    "health",
    "diary",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DEFAULT_DATABASE_URL = f"sqlite:///{BASE_DIR / 'melon-20231204.sqlite3'}"
# env.db("DATABASE_URL", default=DEFAULT_DATABASE_URL)

DATABASES = {
    "default": env.db("DATABASE_URL", default=DEFAULT_DATABASE_URL),
}


# AUTH_USER_MODEL = "auth.User"

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = env.str("LANGUAGE_CODE", default="en-us")

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# django-debug-toolbar
if DEBUG:
    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE
    INTERNAL_IPS = env.list("INTERNAL_IPS", default=["127.0.0.1"])


# django-rest-framework : 프로젝트 전역 설정
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        # "rest_framework.permissions.AllowAny",  # default
        "rest_framework.permissions.IsAuthenticated",
    ],
    # https://www.django-rest-framework.org/api-guide/renderers/
    "DEFAULT_RENDERER_CLASSES": [
        # 디폴트
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
        # 추가
        "blog.renderers.PandasXlsxRenderer",
        "blog.renderers.WordcloudRenderer",
    ],
}

# django-cors-headers
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
    ],
)

# credentials 설정 허용
CORS_ALLOW_CREDENTIALS = env.bool("CORS_ALLOW_CREDENTIALS", default=False)


LOGIN_AND_LOGOUT_SUCCESS_URL_ALLOWED_HOSTS = env.list(
    "LOGIN_AND_LOGOUT_SUCCESS_URL_ALLOWED_HOSTS",
    default=[
        "localhost:3000",
        "127.0.0.1:3000",
    ],
)

# 지정 도메인에서 서브도메인 포함하여 세션 쿠키 공유토록 허용
#   mytravel.com  api.mytravel.com
SESSION_COOKIE_DOMAIN = env.str("SESSION_COOKIE_DOMAIN", default=None) or None
