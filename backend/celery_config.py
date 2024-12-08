# celery_config.py
from celery import Celery
from flask import current_app as app
def make_celery():
    celery = Celery(
        'my_app',
        broker='redis://localhost:6379/0',  # Redis URL
        backend='redis://localhost:6379/0'   # Redis URL for results
    )
    return celery

celery = make_celery()

class ContextTask(celery.Task):
    def _call_(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)


# main.py
