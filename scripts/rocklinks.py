from aiohttp import ClientSession
from bs4 import BeautifulSoup
from asyncio import sleep as asleep

async def rocklinks(url):
    code = url.rstrip("/").split("/")[-1]
    useragent = 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36'
    original = f"https://land.povathemes.com/{code}?source=Direct"
    async with ClientSession() as session:
        async with session.get(original, headers={'Referer': 'https://blog.disheye.com/', 'User-Agent': useragent}) as res:
            html = await res.text()
            cookies = res.cookies
        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find('title')
        if title_tag and title_tag.text == 'Just a moment...':
            return "Unable To Bypass Due To Cloudflare Protected"
        else:
            data = {inp.get('name'): inp.get('value') for inp in soup.find_all("input")}
            await asleep(5)
            async with session.post("https://land.povathemes.com/links/go", data=data, headers={'Referer': original, 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': useragent}, cookies=cookies) as resp:
                if 'application/json' in resp.headers.get('Content-Type'):
                    json_data = await resp.json()
                    return json_data['url']
                else:
                    return "Something Went Wrong :("

#Usage example
# url = "https://go.rocklinks.net/vb6nD"
# print(await rocklinks(url))
