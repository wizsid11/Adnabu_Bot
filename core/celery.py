from __future__ import absolute_import, unicode_literals
from celery import Celery

celery_app = Celery('chatbot')
celery_app.config_from_object('settings')

# Optional configuration, see the application user guide.
celery_app.conf.update(result_expires=3600)