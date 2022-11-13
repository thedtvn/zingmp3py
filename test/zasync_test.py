import asyncio
import aiohttp
import re
from zingmp3py import ZingMp3Async

async def main():
    zi = ZingMp3Async()
    (await zi.getDetailPlaylist("ZB08FIBW")).songs
    await zi.getDetailArtist("Cammie")
    await zi.getSongInfo("ZWAF6UFD")
    await zi.getSongStreaming("ZWAF6UFD")
    await zi.getTop100()
    await zi.search("rick roll")

loop = asyncio.get_event_loop()
loop.run_until_complete(main())