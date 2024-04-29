from aiohttp import ClientSession
from bs4 import BeautifulSoup
from asyncio import sleep as asleep

async def gtlinks(url: str) -> str:
    code = url.split('/')[-1]
    useragent = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36"
    DOMAIN = "https://go.bloggingaro.com"
    
    async with ClientSession() as session:
        async with session.get(f"{DOMAIN}/{code}", headers={'Referer':'https://tech.hipsonyc.com/','User-Agent': useragent}) as res:
            cookies = res.cookies
            html = await res.text()
        async with session.get(f"{DOMAIN}/{code}", headers={'Referer':'https://hipsonyc.com/','User-Agent': useragent}, cookies=cookies) as resp:
            html = await resp.text()
        soup = BeautifulSoup(html, 'html.parser')
        data = {inp.get('name'): inp.get('value') for inp in soup.find_all('input')}
        await asleep(5)
        async with session.post(f"{DOMAIN}/links/go", data=data, headers={'X-Requested-With':'XMLHttpRequest','User-Agent': useragent, 'Referer': f"{DOMAIN}/{code}"}, cookies=cookies) as links:
            if 'application/json' in links.headers.get('Content-Type'):
                json_data = await links.json()
                try:
                    json_data['url']
                except:
                     print("Something Went wrong")

#Usage Example
# url = "https://gtlinks.me/JysE0s74m"
# await gyanilinks(url)
