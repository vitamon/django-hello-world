import datetime
from hello.models import RequestsLog

class RequestLogMiddleware():

    def process_request(self, request):
        #print request.path, datetime.datetime.now()
        log_item = RequestsLog(time=datetime.datetime.now(), url=request.path )
        log_item.save()
