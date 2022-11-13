import aiohttp
import time
import re
from .util import *
from .zsync import ZingMp3
from .sobj import *

cooke = {"cookies": {}, "last_updated": 0}
apikey = {}
async def get_ck(request: aiohttp.ClientSession):
    if int(cooke["last_updated"] + 60) < int(time.time()):
        async with request.get("https://zingmp3.vn") as r:
            cooke["cookies"] = r.cookies
            cooke["last_updated"] = int(time.time())
            return cooke["cookies"]
    else:
        return cooke["cookies"]

async def get_key():
    if not apikey:
        async with aiohttp.ClientSession() as s:
            async with s.get("https://zjs.zmdcdn.me/zmp3-desktop/releases/v1.7.34/static/js/main.min.js") as r:
                data = await r.text()
            key = re.findall(r',h="(.*?)",p=\["ctime","id","type","page","count","version"\]', data)[0]
            skey = re.findall(r"return d\(\)\(t\+r,\"(.*?)\"\)", data)[0]
            apikey.update({"data": [key, skey]})
            return [key, skey]
    else:
        return apikey["data"]

async def requestZing(path, qs={}, haveParam=0):
    apikey, skey = await get_key()
    param = "&".join([f"{i}={k}" for i,k in qs.items()])
    sig = hashParam(skey, path, param, haveParam)
    qs.update({"apiKey": apikey})
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

class Stream(Stream):
    async def download(self, *args, **kwargs):
        if not self.isVIP:
            async with aiohttp.ClientSession() as s:
                async with s.get(self.url, raise_for_status=True) as r:
                    kwargs["mode"] = "wb"
                    with open(*args, **kwargs) as streamfile:
                        streamfile.write(await r.content.read())
        else:
            print("VIP Video Can Not Download")

class Song(Song):
    async def getStreaming(self):
        return await self.client.getSongStreaming(self.id)

class Playlist(Playlist):
    __slots__ = [
        "id",
        "title",
        "indata",
        "client"
    ]

    def __init__(self, indata, client):
        self.id = indata["encodeId"]
        self.indata = indata
        self.title = indata['title']
        self.client = client

    @property
    def songs(self):
        return [Song(song, self.client) for song in self.indata['song']["items"]]

class ZingMp3Async(ZingMp3):
    async def getDetailPlaylist(self, id):
        data = await requestZing("/api/v2/page/get/playlist", {"id": id})
        return Playlist(data["data"], client=self)

    async def getDetailArtist(self, alias):
        data = await requestZing("/api/v2/page/get/artist", {"alias": alias}, 1)
        return Artist(data["data"])

    async def getRadioInfo(self, id):
        data = await requestZing("/api/v2/livestream/get/info", {"id": id})
        return LiveRadio(data["data"])

    async def getSongInfo(self, id):
        data = await requestZing("/api/v2/song/get/info", {"id": id})
        return Song(data["data"], client=self)

    async def getSongStreaming(self, id):
        data = await requestZing("/api/v2/song/get/streaming", {"id": id})
        return [Stream(i, c) for i, c in data["data"].items()]

    async def getTop100(self):
        data = await requestZing("/api/v2/page/get/top-100", haveParam=1)
        dat = data["data"]
        return [Playlist(j, client=self) for i in dat for j in i["items"]]

    async def search(self, search):
        data = await requestZing("/api/v2/search/multi", {"q": search}, 1)
        return Search(data["data"], client=self)
