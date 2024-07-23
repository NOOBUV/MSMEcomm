from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'msmeEcomm.settings')

app = Celery('msmeEcomm')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate-product-summaries-every-10-minutes': {
        'task': 'sellerPortal.tasks.generate_product_summaries',
        'schedule': crontab(minute='*/1'),  # Every 10 minutes
    },
}