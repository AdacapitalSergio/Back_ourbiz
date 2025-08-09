import os
from celery import Celery

# Configura o Django como settings padrão
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

celery_app = Celery("core")

# Carrega as configurações do Celery do Django
celery_app.config_from_object("django.conf:settings", namespace="CELERY")

# Descobre automaticamente as tarefas dentro dos apps Django
celery_app.autodiscover_tasks()