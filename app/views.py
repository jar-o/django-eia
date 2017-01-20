from django.http import HttpResponse
from django.conf import settings
from django.template import loader
import json

import lib # all the API calls to eia.gov happen here

def index(request):
    template = loader.get_template('index.html')
    data = sorted(json.loads(lib.annual()).iteritems(), reverse=True)[0:7]
    return HttpResponse(template.render({'data':data}, request))

# API
def annual(request):
    if settings.API_KEY == request.META['HTTP_AUTHORIZATION']:
        data = lib.annual()
    else:
        data = '{"error":"bad_auth"}'

    resp = HttpResponse(data, content_type='application/json')
    resp['Content-Length'] = len(data)
    return resp
