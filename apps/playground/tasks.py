from time import sleep

# from storefront.celery import celery
from celery import shared_task


# @celery.task
@shared_task
def notify_customers(message):
    print(message)
    sleep(10) # simulating a long-running task
    print("video is ready")


@shared_task
def monthly_report(message):
    print(message)
