# -*- coding: utf-8 -*-

CELERY_TASK_SERIALIZER='pickle'
CELERY_RESULT_SERIALIZER='pickle'
CELERY_TIMEZONE='Europe/Moscow'
CELERY_ENABLE_UTC=True
BROKER_URL=(
    'librabbitmq://%(rabbit_user)s:%(rabbit_secret)s@'
    '%(rabbit_host)s:%(rabbit_port)d/%(rabbit_vhost)s' % dict(
        rabbit_host='127.0.0.1',
        rabbit_user='celery',
        rabbit_secret='IVM2Sm5r9^$',
        rabbit_vhost='celery',
        rabbit_port=5672
    )
)
CELERY_RESULT_BACKEND='rpc://'
