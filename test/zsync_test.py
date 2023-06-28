from zingmp3py import ZingMp3, getUrlTypeAndID

getUrlTypeAndID("https://zingmp3.vn/liveradio/IWZ979CW.html")
zi = ZingMp3()
zi.login("zpsid cookies")
zi.getDetailPlaylist("ZB08FIBW").songs
zi.getDetailArtist("Cammie")
zi.getRadioInfo("IWZ979UB")
zi.getSongInfo("ZWAF6UFD")
zi.getSongStreaming("ZWDB08FB")
zi.getTop100()
zi.search("rick roll")