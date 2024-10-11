import threading

from django.shortcuts import redirect

request_local = threading.local()

def get_request():
    return getattr(request_local, 'request', None)

class RequestMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_local.request = request

        response = self.get_response(request)

        # if response.status_code == 401:

        #     response = redirect('login')

        return response

    def process_exception(self, request, exception):
        request_local.request = None

    def process_template_response(self, request, response):
        request_local.request = None
        return response