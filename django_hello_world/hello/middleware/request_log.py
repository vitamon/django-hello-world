import datetime
from requests.models import RequestsLog


class RequestLogMiddleware():
    def process_request(self, request):
        try:
            RequestsLog.objects.create(time=datetime.datetime.now(), url=request.path)
        except:
            pass