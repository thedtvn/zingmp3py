import requests
import time
from .util import *

cooke = {"cookies": {}, "last_updated": 0}

def get_ck(request: requests.Session):
    if int(time.time() - 60) < int(time.time()):
        with request.get("https://zingmp3.vn") as r:
            cooke["cookies"] = r.cookies
            cooke["last_updated"] = int(time.time())
            return cooke["cookies"]
    else:
        return cooke["cookies"]
def requestZing(path, qs={}, haveParam=0):
    param = "&".join([f"{i}={k}" for i,k in qs.items()])
    sig = hashParam(path, param, haveParam)
    qs.update({"apiKey": '88265e23d4284f25963e6eedac8fbfa3'})
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


