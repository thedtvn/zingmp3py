from hashlib import sha256
import hashlib
import time
import hmac

def getHash256(data):
    hx = sha256(data.encode('utf8'))
    return hx.hexdigest()

def getHmac512(data, key):
    h = hmac.new(key.encode(), data.encode(), hashlib.sha512)
    return h.hexdigest()

def hashParam(path, param, haveParam):
    now = int(time.time())
    strHash = f"ctime={now}"
    if (haveParam == 0): strHash += param;
    h1 = getHash256(strHash)
    return [getHmac512(path + h1, '2aa2d1c561e809b267f3638c4a307aab'),  now];
