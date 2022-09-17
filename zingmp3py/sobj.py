
host = "https://zingmp3.vn"


class LiveRadio:
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

class Song:
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
        self.artists = [Artist(i) for i in indata["artists"]]
        self.duration = indata.get("duration")
        self.thumbnail = indata.get("thumbnailM")
        self.isOffical = indata.get("isOffical")
        self.like = indata.get("like")
        self.listen = indata.get("listen")
        self.link = host+indata.get("link")


    def getStreaming(self):
        return self.client.getSongStreaming(self.id)

class Playlist:
    __slots__ = [
        "songs",
        "title"
    ]

    def __init__(self, indata, client):
        self.songs = [Song(song, client) for song in indata['song']["items"]]
        self.title = indata['title']

class Artist:
    __slots__ = [
        "id",
        "name",
        "link",
        "spotlight",
        "alias",
        "thumbnail",
        "isOA",
        "isOABrand",
        "totalFollow"
    ]
    def __init__(self, indata):
        self.name = indata["name"]
        self.id = indata["id"]
        self.link = host+indata ["link"]
        self.isOABrand = indata["isOABrand"]
        self.totalFollow = indata.get("totalFollow")
        self.thumbnail = indata["thumbnailM"]
        self.isOA = indata["isOA"]
        self.spotlight = indata["spotlight"]