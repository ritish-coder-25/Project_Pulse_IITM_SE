from celery import Celery
from flask import current_app as app

celery = Celery('app', broker= 'redis://localhost:6379/0', backend= 'redis://localhost:6379/0')

    # Create a custom task class that wraps Flask app context
class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return super().__call__(*args, **kwargs)


celery.Task = ContextTask
