from hashlib import sha256
import hashlib
import time
import hmac
import urllib.parse

def getUrlTypeAndID(url):
    ourl = urllib.parse.urlparse(url)
    if ourl.hostname != 'zingmp3.vn':
        raise ZingMp3Error({"msg": "Link Không Hợp Lệ: %s" % url})
    ph = ourl.path.split('/')[1:]
    urltype = ph[0]
    urlid = ph[-1][:-5]
    return {"type": urltype, "id": urlid}

def getHash256(data):
    hx = sha256(data.encode('utf8'))
    return hx.hexdigest()

def getHmac512(data, key):
    h = hmac.new(key.encode(), data.encode(), hashlib.sha512)
    return h.hexdigest()

def hashParam(key, path, param, haveParam):
    now = int(time.time())
    strHash = f"ctime={now}"
    if (haveParam == 0): strHash += param;
    h1 = getHash256(strHash)
    return [getHmac512(path + h1, key),  now]


class ZingMp3Error(Exception):
    def __init__(self, data):
        self.data = data
        super().__init__(data["msg"])

    @property
    def raw(self):
        return self.data
