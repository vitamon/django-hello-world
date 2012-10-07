import datetime
from hello.models import RequestsLog


class RequestLogMiddleware():
    def __init__(self):
        self.priority_lookup_cache = {}

    def process_request(self, request):
        try:
            url=request.path
            #self.get_priority(url)
            log_item = RequestsLog(time=datetime.datetime.now(), url=url)
            log_item.save()
        except:
            pass
