import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CeleryProject.settings")

app = Celery("CeleryProject") # 이 이름을 기억해두세요
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()