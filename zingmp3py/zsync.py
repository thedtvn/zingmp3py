import re
from .util import *
from .sobj import *


class ZingMp3:
    def __init__(self):
        self.apikey = {}
        self.cooke = {"cookies": {}, "last_updated": 0}

    def get_ck(self, request: requests.Session):
        if int(self.cooke["last_updated"] - 60) < int(time.time()):
            with request.get("https://zingmp3.vn") as r:
                self.cooke["cookies"] = r.cookies
                self.cooke["last_updated"] = int(time.time())
                return self.cooke["cookies"]
        else:
            return self.cooke["cookies"]

    def get_key(self):
        if not self.apikey:
            with requests.Session() as s:
                with s.get("https://zingmp3.vn/") as r:
                    data = r.text
                outs = re.findall(r"<script type=\"text/javascript\" src=\"(https://zjs.zmdcdn.me/zmp3-desktop/releases/.*?/static/js/main\.min\.js)\"></script>", data)
                with s.get(outs[0]) as r:
                    data = r.text
                outs = re.findall(r"\"([a-zA-Z0-9]{32})\"", data)
                key = outs[0]
                skey = outs[1]
                self.apikey.update({"data": [key, skey]})
                return [key, skey]
        else:
            return self.apikey["data"]

    def requestZing(self, path, qs={}, haveParam=0):
        apikey, skey = self.get_key()
        param = "&".join([f"{i}={k}" for i, k in qs.items()])
        sig = hashParam(skey, path, param, haveParam)
        qs.update({"apiKey": apikey})
        qs.update({"ctime": sig[1]})
        qs.update({"sig": sig[0]})
        url = "https://zingmp3.vn" + path
        with requests.Session() as s:
            with s.get(url, params=qs, cookies=self.get_ck(s)) as r:
                data = r.json()
                if data['err'] != 0:
                    raise ZingMp3Error(data)
                return data

    def getDetailPlaylist(self, id):
        data = self.requestZing("/api/v2/page/get/playlist", {"id": id})
        return Playlist(data["data"], client=self)

    def getDetailArtist(self, alias):
        data = self.requestZing("/api/v2/page/get/artist", {"alias": alias}, 1)
        return Artist(data["data"])

    def getRadioInfo(self, id):
        data = self.requestZing("/api/v2/livestream/get/info", {"id": id})
        return LiveRadio(data["data"])

    def getSongInfo(self, id):
        data = self.requestZing("/api/v2/song/get/info", {"id": id})
        return Song(data["data"], client=self)

    def getSongStreaming(self, id):
        data = self.requestZing("/api/v2/song/get/streaming", {"id": id})
        return [Stream(i, c) for i, c in data["data"].items()]

    def getTop100(self):
        data = self.requestZing("/api/v2/page/get/top-100", haveParam=1)
        dat = data["data"]
        return [Playlist(j, client=self) for i in dat for j in i["items"]]

    def search(self, search):
        data = self.requestZing("/api/v2/search/multi", {"q": search}, 1)
        return Search(data["data"], client=self)


