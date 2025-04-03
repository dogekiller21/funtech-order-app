import time

from worker.client import celery_app


@celery_app.task(name="process_order")
def process_order(data: dict):
    time.sleep(2)
    print(f"Order {data['id']} processed")
