import ssl

from celery import Celery
from django.conf import settings

use_ssl = getattr(settings, "CELERY_USE_SSL", True)
if use_ssl:
    celery_app = Celery(
        "core", broker_use_ssl={"ssl_cert_reqs": ssl.CERT_NONE}, redis_backend_use_ssl={"ssl_cert_reqs": ssl.CERT_NONE}
    )
else:
    celery_app = Celery("core")
celery_app.config_from_object(settings)
celery_app.autodiscover_tasks()


@celery_app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
