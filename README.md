# zingmp3py
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com) [![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
#### A light weight Python library for the ZingMp3 API
##### *all functions are return dict or ZingMp3 Object

# install 

## pypi
```
pip install zingmp3py
```

## Git (version in development)
```
pip install git+https://github.com/thedtvn/zingmp3py.git
```


# Sync :
```py
from zingmp3py import ZingMp3

zi = ZingMp3()
# login is not required 
zi.login("zpsid cookies")
zi.getDetailPlaylist("67ZFO8DZ")
zi.getDetailArtist("Cammie")
zi.getRadioInfo("IWZ979CW")
zi.getSongInfo("ZWAF6UFD")
zi.getSongStreaming("ZWAF6UFD")
zi.getTop100()
zi.search("rick roll")
```

# Async
```py
import asyncio
from zingmp3py import ZingMp3Async

async def main():
    zi = ZingMp3Async()
    # login is not required 
    await zi.login("zpsid cookies")
    await zi.getDetailPlaylist("67ZFO8DZ")
    await zi.getDetailArtist("Cammie")
    await zi.getSongInfo("ZWAF6UFD")
    await zi.getSongStreaming("ZWAF6UFD")
    await zi.getTop100()
    await zi.search("rick roll")

asyncio.run(main())
```

## how to get zpsid cookies

go to https://id.zalo.me/account/logininfo then check f12 go to tab application go to cookies and check for cookie name zpsid

note: please check check you are login or not by check key  `logged` in json return in that url is `true`

## Get Type And ID

```py
from zingmp3py import getUrlTypeAndID

getUrlTypeAndID("https://zingmp3.vn/liveradio/IWZ979CW.html")
```
