
"""
Django settings for ecommerce project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

import os
MAIN_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(MAIN_DIR,"templates")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'm-qfkw!b=n@20zla%8wh+#jq9^)@bw^#n2--o$_k*==2xgly7v'

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
    'crispy_forms',

    #applications
    'store',
    'accounts',

    #social login app
    'social_django',
    # login using google
    'django.contrib.sites',   # <--

     'allauth',   # <--
     'allauth.account',   # <--
     'allauth.socialaccount',   # <--
     'allauth.socialaccount.providers.google',   # <--

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # <-- for authorization
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'ecommerce.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR, ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # social Login
                'social_django.context_processors.backends',  # <-- Here
                'social_django.context_processors.login_redirect', # <-- Here
            ],
        },
    },
]

################# authenticate with backend ######################

AUTHENTICATION_BACKENDS = (
    'social_core.backends.facebook.FacebookOAuth2',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',

    'django.contrib.auth.backends.ModelBackend',
    # login with google
    'allauth.account.auth_backends.AuthenticationBackend',
)
SITE_ID = 1


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

#################################################

WSGI_APPLICATION = 'ecommerce.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


## setting up email sending process
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
###### Email information
EMAIL_HOST_USER = 'expressyourthought05@gmail.com'
EMAIL_HOST_PASSWORD = 'thisisbusinessemail05'
############################################################

# Social Auth Login Facebook
SOCIAL_AUTH_FACEBOOK_KEY = '661452851457363'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET = '389c368ebc37846245f1677219acaa19'  # App Secret

# # Social Auth Login Twitter
SOCIAL_AUTH_TWITTER_KEY = '4kc6BfBKEJwwzKKUgWO3vBgqW'
SOCIAL_AUTH_TWITTER_SECRET = '4nJpmkTJ6UlubYoJo6g3U7NfRNG6j3Ww6HqhtcUH6N0vaaEsFC'

# # Social Auth Login Github
SOCIAL_AUTH_GITHUB_KEY = '941883d2736cdf483a4a'
SOCIAL_AUTH_GITHUB_SECRET = '123cb659df6462f2691fd75d201743ea5b5cf791'

# Social Auth Login
SOCIAL_AUTH_LOGIN_ERROR_URL = 'social_complete'
SOCIAL_AUTH_LOGIN_REDIRECT_URL = 'social_complete'
SOCIAL_AUTH_RAISE_EXCEPTIONS = False



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(MAIN_DIR, 'media')

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(MAIN_DIR, 'static')

STATICFILES_DIRS = [
    STATIC_DIR,
]

LOGIN_REDIRECT_URL = 'social_complete'
LOGOUT_REDIRECT_URL = 'login'
