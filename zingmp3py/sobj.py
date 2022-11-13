import requests

host = "https://zingmp3.vn"

class LiveRadio(object):
    __slots__ = [
    "id",
    "streaming_url",
    "title",
    "url",
    "description",
    "thumbnail",
    "total_reaction"
    ]

    def __init__(self, indata):
        self.id = indata["encodeId"]
        self.streaming_url = indata["streaming"]
        self.title = indata["title"]
        self.url = host+indata["link"]
        self.description = indata["description"]
        self.thumbnail = indata["thumbnail"]
        self.total_reaction = indata["totalReaction"]

class Song(object):
    __slots__ = [
                 "id",
                 "isOffical",
                 "listen",
                 "duration",
                 "thumbnail",
                 "like",
                 "artists",
                 "title",
                 "link",
                 "client"]
    def __init__(self, indata, client):
        self.client = client
        self.title = indata["title"]
        self.id = indata["encodeId"]
        self.artists = [Artist(i) for i in indata["artists"]] if indata.get("artists") else None
        self.duration = indata.get("duration")
        self.thumbnail = indata.get("thumbnail")
        self.isOffical = indata.get("isOffical")
        self.like = indata.get("like")
        self.listen = indata.get("listen")
        self.link = host+indata.get("link")


    def getStreaming(self):
        return self.client.getSongStreaming(self.id)

class Playlist(object):
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

class Artist(object):
    __slots__ = [
        "id",
        "name",
        "link",
        "spotlight",
        "alias",
        "thumbnail",
        "isOA",
        "totalFollow"
    ]

    def __init__(self, indata):
        self.name = indata["name"]
        self.id = indata["id"]
        self.link = host+indata ["link"]
        self.totalFollow = indata.get("totalFollow")
        self.thumbnail = indata["thumbnail"]

class Stream(object):
    __slots__ = ["url", "quality", "isVIP"]
    def __init__(self, quality, url):
        self.url = url if url != "VIP" else None
        self.quality = quality
        self.isVIP = bool(url == "VIP")

    def download(self, *args, **kwargs):
        if not self.isVIP:
            r = requests.get(self.url, stream=True)
            r.raise_for_status()
            kwargs["mode"] = "wb"
            with open(*args, **kwargs) as streamfile:
                streamfile.write(r.content)
        else:
            print("VIP Video Can Not Download")

class Search(object):
    def __init__(self, indata, client):
        self.indata = indata
        self.client = client

    @property
    def songs(self):
        return [Song(i, self.client) for i in self.indata["songs"]]

    @property
    def playlists(self):
        return [Playlist(i, self.client) for i in self.indata["playlists"]]