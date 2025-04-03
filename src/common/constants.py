from datetime import timedelta

MAX_EMAIL_LENGTH = 320
MAX_PASSWORD_LENGTH = 128
MIN_PASSWORD_LENGTH = 8

ACCESS_TOKEN_EXPIRE_DELTA = timedelta(minutes=60)


CELERY_WORKER_NAME = "funtech-worker"
