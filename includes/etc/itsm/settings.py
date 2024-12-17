# ITSM Docker Settings

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/data/db.sqlite3',
    }
}

#
# Example MariaDB/MySQL setup
#
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'itsm',
#         'USER': '<db username>',
#         'PASSWORD': '<db password>',
#         'HOST': '<db host/ip address>',
#         'PORT': '',
#     }
# }

#
#
#
# CELERY_BROKER_URL = 'amqp://<username>:<password>@<host>:<port>/[<message host>]'  # 'amqp://' is the connection protocol

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

SECURE_SSL_REDIRECT = True

USE_X_FORWARDED_HOST = True 
