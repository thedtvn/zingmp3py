import aiohttp
import re

from yarl import URL

from .util import *
from .zsync import ZingMp3
from .sobj import *

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
    cooke = aiohttp.CookieJar()
    apikey = {}
    zpsid = None
    last_updated = 0

    async def get_ck(self, request: aiohttp.ClientSession):
        if int(self.last_updated + 60) < int(time.time()):
            if self.zpsid:
                ck = {"zpsid": self.zpsid}
                async with request.get("https://id.zalo.me/account?continue=https%3A%2F%2Fzingmp3.vn", cookies=ck) as r:
                    if str(r.url) != "https://zingmp3.vn":
                        raise Exception("zpsid is invalid cookie")
            async with request.get("https://zingmp3.vn") as r:
                pass
            for i in list(request.cookie_jar):
                self.cooke.update_cookies({i.key: i})
                request.cookie_jar.update_cookies({i.key: i})
            self.last_updated = int(time.time())
        else:
            for i in list(self.cooke):
                request.cookie_jar.update_cookies({i.key: i})

    async def get_key(self):
        if not self.apikey:
            async with aiohttp.ClientSession() as s:
                async with s.get("https://zingmp3.vn/") as r:
                    data = await r.text()
                outs = re.findall(r"<script type=\"text/javascript\" src=\"(https://zjs.zmdcdn.me/zmp3-desktop/releases/.*?/static/js/main\.min\.js)\"></script>", data)
                async with s.get(outs[0]) as r:
                    data = await r.text()
                outs = re.findall(r"\"([a-zA-Z0-9]{32})\"", data)
                key = outs[0]
                skey = outs[1]
                self.apikey.update({"data": [key, skey]})
                return [key, skey]
        else:
            return self.apikey["data"]

    async def requestZing(self, path, qs={}, haveParam=0):
        apikey, skey = await self.get_key()
        param = "&".join([f"{i}={k}" for i, k in qs.items()])
        sig = hashParam(skey, path, param, haveParam)
        qs.update({"apiKey": apikey})
        qs.update({"ctime": sig[1]})
        qs.update({"sig": sig[0]})
        url = "https://zingmp3.vn" + path
        async with aiohttp.ClientSession() as s:
            await self.get_ck(s)
            async with s.get(url, params=qs) as r:
                data = await r.json()
                if data['err'] != 0:
                    raise ZingMp3Error(data)
                return data

    async def login(self, zpsid):
        async with aiohttp.ClientSession() as s:
            async with s.get("https://id.zalo.me/account/logininfo", cookies={"zpsid": zpsid}) as r:
                out = await r.json()
            if out["error_code"] != 0:
                raise ZingMp3Error({"msg": f"Login Error: {out['error_message']}"})
            elif not out["data"]["logged"]:
                raise ZingMp3Error({"msg": f"zpsid is invalid"})
        self.zpsid = zpsid

    async def getDetailPlaylist(self, id):
        data = await self.requestZing("/api/v2/page/get/playlist", {"id": id})
        return Playlist(data["data"], client=self)

    async def getDetailArtist(self, alias):
        data = await self.requestZing("/api/v2/page/get/artist", {"alias": alias}, 1)
        return Artist(data["data"])

    async def getRadioInfo(self, id):
        data = await self.requestZing("/api/v2/livestream/get/info", {"id": id})
        return LiveRadio(data["data"])

    async def getSongInfo(self, id):
        data = await self.requestZing("/api/v2/song/get/info", {"id": id})
        return Song(data["data"], client=self)

    async def getSongStreaming(self, id):
        data = await self.requestZing("/api/v2/song/get/streaming", {"id": id})
        return [Stream(i, c) for i, c in data["data"].items()]

    async def getTop100(self):
        data = await self.requestZing("/api/v2/page/get/top-100", haveParam=1)
        dat = data["data"]
        return [Playlist(j, client=self) for i in dat for j in i["items"]]

    async def search(self, search):
        data = await self.requestZing("/api/v2/search/multi", {"q": search}, 1)
        return Search(data["data"], client=self)
