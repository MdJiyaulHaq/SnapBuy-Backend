import logging

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.mail import (BadHeaderError, EmailMessage, mail_admins,
                              send_mail)
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.views import APIView
from templated_mail.mail import BaseEmailMessage

from .tasks import notify_customers

logger = logging.getLogger(__name__)


# If we have class based views
class SayHelloView(APIView):
    # @method_decorator(cache_page(5 * 60))
    def get(self, request):
        try:
            logger.info("logging starts")
            response = requests.get("https://httpbin.org/delay/3")
            logger.info("logging ends")
            data = response.json()
        except requests.ConnectionError:
            logger.critical(" the httpbin is offline")
        return render(request, "hello.html", {"name": data})


# @cache_page(5 * 60)  # better way for caching
# def say_hello(request):
#     response = requests.get("https://httpbin.org/delay/3")
#     data = response.json()
#     return render(request, "hello.html", {"name": data})


# def say_hello(request):
#     key = "httpbin_result"  # Key name can be anything you want
#     if cache.get(key) is None:
#         response = requests.get(
#             "https://httpbin.org/delay/3"
#         )  # simulates slow 3rd party service or api
#         data = response.json()
#         cache.set(key, data)
#     return render(request, "hello.html", {"name": cache.get(key)})


# def say_hello(request):
#     notify_customers.delay("Your video is being processed")
#     return render(request, "hello.html", {"name": "Shankar"})


# def say_hello(request):
#     try:
#         # normal mails to anyone
#         send_mail(
#             subject="Welcome to Storefront",
#             message="This is plain message,",
#             html_message="This is html message",
#             from_email=settings.DEFAULT_EMAIL_FROM,
#             recipient_list=["to@storefront.com"],
#         )
#         # to admins
#         mail_admins(
#             subject="Admins, Welcome to Storefront.",
#             message="This is plain message,",
#             html_message="This is html message",
#         )
#         # Above implementation comes from class EmailMessage.
#         # Also if you want to attach files
#         msg = EmailMessage(
#             subject="Welcome to Storefront",
#             body="This is a plain message.",
#             from_email=settings.DEFAULT_EMAIL_FROM,
#             to=["to@storefront.com"],
#         )
#         msg.attach_file("playground/static/images/Md.jpg")
#         msg.send()
#         # if you want to send templated_emails
#         message = BaseEmailMessage(
#             template_name="emails/hello2.html", context={"name": "Shankar"}
#         )
#         message.send(["to@storefront.com"])
#         return render(
#             request,
#             "hello.html",
#             {"message": "Email sent successfully!", "name": "Shankar"},
#         )
#         return render(request, "hello.html", {"message": "Email sent successfully!"})
#     except BadHeaderError:
#         return render(request, "hello.html", {"message": "Invalid header found."})
#     except Exception as e:
#         return render(
#             request, "hello.html", {"message": f"Failed to send email: {str(e)}"}
#         )
