import requests
import re
from .util import *
from .sobj import *

cooke = {"cookies": {}, "last_updated": 0}
apikey = {}

def get_ck(request: requests.Session):
    if int(cooke["last_updated"] - 60) < int(time.time()):
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
        data = requestZing("/api/v2/page/get/playlist", {"id": id})
        return Playlist(data["data"], client=self)

    def getDetailArtist(self, alias):
        data = requestZing("/api/v2/page/get/artist", {"alias": alias}, 1)
        return Artist(data["data"])

    def getRadioInfo(self, id):
        data = requestZing("/api/v2/livestream/get/info", {"id": id})
        return LiveRadio(data["data"])

    def getSongInfo(self, id):
        data = requestZing("/api/v2/song/get/info", {"id": id})
        return Song(data["data"], client=self)

    def getSongStreaming(self, id):
        data = requestZing("/api/v2/song/get/streaming", {"id": id})
        return [Stream(i, c) for i, c in data["data"].items()]

    def getTop100(self):
        data = requestZing("/api/v2/page/get/top-100", haveParam=1)
        dat = data["data"]
        return [Playlist(j, client=self) for i in dat for j in i["items"]]

    def search(self, search):
        data = requestZing("/api/v2/search/multi", {"q": search}, 1)
        return Search(data["data"], client=self)


