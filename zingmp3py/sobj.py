
host = "https://zingmp3.vn/"


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
    __slots__ = ["title"
                 "artist", "album", "artist"]
    def __init__(self, indata, client):
        self.title = indata["title"]
        self.id = indata["encodeId"]
        self.artist = Artist(indata["artist"])
        self.duration = indata.get("duration")
        self.thumbnail = indata.get("thumbnailM")
        self.isOffical = indata.get("isOffical")
        self.like = indata.get("like")
        self.listen = indata.get("listen")

    def


class Artist:
    {
        "id": "IWZA6CIZ",
        "name": "ERIK",
        "link": "/ERIK",
        "spotlight": True,
        "alias": "ERIK",
        "thumbnail": "https://photo-resize-zmp3.zmdcdn.me/w240_r1x1_jpeg/avatars/5/5/b/6/55b66a1a7b1e2cf8d5fff1abfd0d4605.jpg",
        "thumbnailM": "https://photo-resize-zmp3.zmdcdn.me/w360_r1x1_jpeg/avatars/5/5/b/6/55b66a1a7b1e2cf8d5fff1abfd0d4605.jpg",
        "isOA": True,
        "isOABrand": False,
        "totalFollow": 480164
    }