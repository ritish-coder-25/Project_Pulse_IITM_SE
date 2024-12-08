# celery_config.py
from celery import Celery

def make_celery():
    celery = Celery(
        'my_app',
        broker='redis://localhost:6379/0',  # Redis URL
        backend='redis://localhost:6379/0'   # Redis URL for results
    )
    return celery

celery = make_celery()


# main.py
