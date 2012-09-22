from annoying.decorators import render_to
from hello.models import RequestsLog

@render_to('hello/home.html')
def home(request):
    return {}


@render_to('hello/requests.html')
def requests(request):
    top_ten = RequestsLog.objects.get_last_ten()
    return {"items": top_ten}
