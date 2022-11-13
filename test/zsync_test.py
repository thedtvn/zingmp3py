from zingmp3py import ZingMp3, getUrlTypeAndID

getUrlTypeAndID("https://zingmp3.vn/liveradio/IWZ979CW.html")
zi = ZingMp3()
print(zi.getDetailPlaylist("ZB08FIBW").songs)
zi.getDetailArtist("Cammie")
zi.getRadioInfo("IWZ979CW")
zi.getSongInfo("ZWAF6UFD")
zi.getSongStreaming("ZWAF6UFD")
zi.getTop100()
zi.search("rick roll")