import asyncio
from urllib.parse import unquote
import aiohttp
from pyrogram import Client
import base64
from pyrogram.raw.functions.messages import RequestWebView

bot_peer = "getcapybot"
client = Client("CapyMine", api_id=11111, api_hash="api_hash")

client.start()


async def init_data():
    web_view = await client.invoke(RequestWebView(
        peer=await client.resolve_peer(bot_peer),
        bot=await client.resolve_peer(bot_peer),
        platform='ios',
        from_bot_menu=False,
        url="https://app.tgquest.com/clicker"
    ))

    auth_url = web_view.url
    web_data = unquote(unquote(auth_url.split('tgWebAppData=', 1)[-1].split('&tgWebAppVersion', 1)[0]))
    return base64.b64encode(web_data.encode())


async def mine(data):
    async with aiohttp.ClientSession(headers={"Authorization": data}) as session:
        async with session.post('https://api.tgquest.com/clicker/click', json={'count': 100000}) as resp:
            print(await resp.json())


async def main():
    data = await init_data()
    print(data)
    x = int(input("Сколько повторов делать: "))
    while x:
        await asyncio.create_task(mine(data.decode('utf-8')))


client.run(main())
