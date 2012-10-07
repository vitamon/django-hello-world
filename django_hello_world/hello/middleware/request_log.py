import datetime
from hello.models import RequestsLog

class RequestLogMiddleware():
    def process_request(self, request):
        try:
            log_item = RequestsLog(time=datetime.datetime.now(), url=request.path)
            log_item.save()
        except:
            pass
