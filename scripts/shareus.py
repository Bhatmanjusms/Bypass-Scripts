from aiohttp import ClientSession
from bs4 import BeautifulSoup
from asyncio import sleep as asleep

async def shareus(url):
    code = url.split('/')[-1]
    DOMAIN = "https://api.shrslink.xyz"
    headers = {'User-Agent':'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36', 'Origin':'https://shareus.io'}
    api = f"{DOMAIN}/v?shortid={code}&initial=true&referrer="
    async with ClientSession() as session:
        async with session.get(api, headers=headers) as resp:
            data = await resp.json()
            id = data.get('sid')
            if not id:
                return "ID Error"
            else:
                api_2 = f"{DOMAIN}/get_link?sid={id}"
                async with session.get(api_2, headers=headers) as resp_2:
                    data_2 = await resp_2.json()
                    final = data_2['link_info']['destination']
                    return final

#Usage Example:-
# url = "https://shrs.link/sORqzM"
# print(await shareus(url))
