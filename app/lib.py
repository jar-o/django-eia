from django.conf import settings
import httplib
import redis
import json
from socket import gethostbyname, gaierror

eia_gov_srv = 'api.eia.gov'
eia_gov_prefix = '/series/?api_key=' + settings.EIA_GOV_API_KEY + '&series_id='

r = redis.StrictRedis(host=settings.REDIS_SRV, port=settings.REDIS_PORT, db=0, password=settings.REDIS_PASSWORD)

def _req(series_id):
    conn = httplib.HTTPConnection(eia_gov_srv)

    try:
        conn.request('GET', eia_gov_prefix + series_id)
    except gaierror:
        return "{}"

    resp = conn.getresponse()
    if resp.status == 200:
        return resp.read()
    else:
        return "{}"

def _fetch_cache(rkey, series_id):
    ret = r.get(rkey)
    if not ret:
        r.set(rkey, _req(series_id), settings.REDIS_DEFAULT_CACHE_TIME)
        ret = r.get(rkey)
    return json.loads(ret)

def coal():
    return _fetch_cache('eia-coal-US-net-generation-response', 'ELEC.GEN.COW-US-98.A')

def conventional_hydro():
    return _fetch_cache('eia-conventional-hydro-US-net-generation-response', 'ELEC.GEN.HYC-US-99.A')

def geothermal():
    return _fetch_cache('eia-geothermal-US-net-generation-response', 'ELEC.GEN.GEO-US-99.A')

def wind():
    return _fetch_cache('eia-wind-US-net-generation-response', 'ELEC.GEN.WND-US-99.A')

def solar():
    return _fetch_cache('eia-solar-US-net-generation-response', 'ELEC.GEN.TSN-US-99.A')

def natural_gas():
    return _fetch_cache('eia-natural-gas-US-net-generation-response', 'ELEC.GEN.NG-US-99.A')

def nuclear():
    return _fetch_cache('eia-nuclear-US-net-generation-response', 'ELEC.GEN.NUC-US-99.A')

def annual():
    ret = {}
    rkey = 'api-annual'
    if not r.get(rkey):
        # As you add "fetch" functions above, be sure to update this list to
        # include them in the output.
        funcs = ['coal', 'conventional_hydro', 'geothermal', 'wind', 'solar', 'natural_gas', 'nuclear']
        for i in range(0, len(funcs)):
            # Introspection here to call appropriate func based on above list
            c = globals()[funcs[i]]()

            if 'series' not in c: continue

            for s in c['series'][0]['data']:
                if s[0] not in ret:
                    ret[s[0]] = {}
                # Data comes in thousand megawatt hours, we convert to gigawatt
                ret[s[0]][funcs[i]] = s[1]/1000
        r.set(rkey, json.dumps(ret), settings.REDIS_DEFAULT_CACHE_TIME)
    return r.get(rkey)
