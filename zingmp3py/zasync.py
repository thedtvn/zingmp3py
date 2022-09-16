import aiohttp
import time
from .util import *

cooke = {"cookies": {}, "last_updated": 0}
async def get_ck(request: aiohttp.ClientSession):
    if int(time.time() - 60) < int(time.time()):
        async with request.get("https://zingmp3.vn") as r:
            cooke["cookies"] = r.cookies
            cooke["last_updated"] = int(time.time())
            return cooke["cookies"]
    else:
        return cooke["cookies"]
async def requestZing(path, qs={}, haveParam=0):
    param = "&".join([f"{i}={k}" for i,k in qs.items()])
    sig = hashParam(path, param, haveParam)
    qs.update({"apiKey": '88265e23d4284f25963e6eedac8fbfa3'})
    qs.update({"ctime": sig[1]})
    qs.update({"sig": sig[0]})
    url = "https://zingmp3.vn" + path
    async with aiohttp.ClientSession() as s:
        ck = await get_ck(s)
        async with s.get(url, params=qs, cookies=ck) as r:
            data = await r.json()
            if data['err'] != 0:
                raise ZingMp3Error(data)
            return data

class ZingMp3Async:
    def __init__(self):
        pass

    async def getDetailPlaylist(self, id):
        return await requestZing("/api/v2/page/get/playlist", {"id": id})

    async def getDetailArtist(self, alias):
        return await requestZing("/api/v2/page/get/artist", {"alias": alias}, 1)

    async def getRadioInfo(self, id):
        return await requestZing("/api/v2/livestream/get/info", {"id": id})

    async def getSongInfo(self, id):
        return await requestZing("/api/v2/song/get/info", {"id": id})

    async def getSongStreaming(self, id):
        return await requestZing("/api/v2/song/get/streaming", {"id": id})

    async def getHomePage(self, page=1):
        return await requestZing("/api/v2/page/get/home", {"page": page})

    async def getChartHome(self):
        return await requestZing("/api/v2/page/get/chart-home")

    async def getWeekChart(self, id):
        return await requestZing("/api/v2/page/get/week-chart", {"id": id})

    async def getNewReleaseChart(self):
        return await requestZing("/api/v2/page/get/newrelease-chart", haveParam=1)

    async def getTop100(self):
        return await requestZing("/api/v2/page/get/top-100", haveParam=1)

    async def search(self, search):
        return await requestZing("/api/v2/search/multi", {"q": search}, 1)
