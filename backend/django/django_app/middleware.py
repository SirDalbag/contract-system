from django_app import utils
import threading
import requests
import datetime


class CustomLogsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        try:
            data = {
                "ip": utils.get_ip(request),
                "date": int(datetime.datetime.now().timestamp()),
            }

            def make_request():
                requests.post(
                    url="http://127.0.0.1:8001/api/log",
                    data=data,
                )

            thread = threading.Thread(target=make_request)
            thread.start()
        except Exception as error:
            print(error)
        return response
