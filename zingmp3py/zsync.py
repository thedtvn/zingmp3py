import requests
import re
from .util import *

cooke = {"cookies": {}, "last_updated": 0}
apikey = {}

def get_ck(request: requests.Session):
    if int(time.time() - 60) < int(time.time()):
        with request.get("https://zingmp3.vn") as r:
            cooke["cookies"] = r.cookies
            cooke["last_updated"] = int(time.time())
            return cooke["cookies"]
    else:
        return cooke["cookies"]

def get_key():
    if not apikey:
        with requests.Session() as s:
            with s.get("https://zjs.zmdcdn.me/zmp3-desktop/releases/v1.7.34/static/js/main.min.js") as r:
                data = r.text
            key = re.findall(r',h="(.*?)",p=\["ctime","id","type","page","count","version"\]', data)[0]
            skey = re.findall(r"return d\(\)\(t\+r,\"(.*?)\"\)", data)[0]
            apikey.update({"data": [key, skey]})
            return [key, skey]
    else:
        return apikey["data"]

def requestZing(path, qs={}, haveParam=0):
    apikey, skey = get_key()
    param = "&".join([f"{i}={k}" for i,k in qs.items()])
    sig = hashParam(skey, path, param, haveParam)
    qs.update({"apiKey": apikey})
    qs.update({"ctime": sig[1]})
    qs.update({"sig": sig[0]})
    url = "https://zingmp3.vn" + path
    with requests.Session() as s:
        with s.get(url, params=qs, cookies=get_ck(s)) as r:
            data = r.json()
            if data['err'] != 0:
                raise ZingMp3Error(data)
            return data

class ZingMp3:
    def __init__(self):
        pass

    def getDetailPlaylist(self, id):
        return requestZing("/api/v2/page/get/playlist", {"id": id})

    def getDetailArtist(self, alias):
        return requestZing("/api/v2/page/get/artist", {"alias": alias}, 1)

    def getRadioInfo(self, id):
        return requestZing("/api/v2/livestream/get/info", {"id": id})

    def getSongInfo(self, id):
        return requestZing("/api/v2/song/get/info", {"id": id})

    def getSongStreaming(self, id):
        return requestZing("/api/v2/song/get/streaming", {"id": id})

    def getHomePage(self, page=1):
        return requestZing("/api/v2/page/get/home", {"page": page})

    def getChartHome(self):
        return requestZing("/api/v2/page/get/chart-home")

    def getWeekChart(self, id):
        return requestZing("/api/v2/page/get/week-chart", {"id": id})

    def getNewReleaseChart(self):
        return requestZing("/api/v2/page/get/newrelease-chart", haveParam=1)

    def getTop100(self):
        return requestZing("/api/v2/page/get/top-100", haveParam=1)

    def search(self, search):
        return requestZing("/api/v2/search/multi", {"q": search}, 1)


