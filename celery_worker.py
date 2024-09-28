#!/usr/bin/env python3
from tasks import download_video_task
from celery import Celery
import logging

logging.basicConfig(level=logging.DEBUG)


# Initialize the Celery application
celery_app = Celery(
    'app_name', broker='redis://localhost:6379/0'
)

# Celery configuration
celery_app.conf.update(
    result_backend='sqlite:///downloads.db',
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'],
    timezone='UTC',
    enable_utc=True,

)


@celery_app.task
def some_background_task():
    return 'Task Completed!'
