from aiohttp import ClientSession
from bs4 import BeautifulSoup
from asyncio import sleep as asleep

async def try2link(url):
    DOMAIN = 'https://try2link.com'
    code = url.split('/')[-1]

    async with ClientSession() as session:
        async with session.get(f'{DOMAIN}/{code}', headers={"Referer": 'https://hightrip.net/'}) as res:
             if res.status == 200:
                 html = await res.text()
             else:
                 async with session.get(f'{DOMAIN}/{code}', headers={"Referer": 'https://to-travel.netl'}) as res:
                      if res.status == 200:
                          html = await res.text()
                      else:
                          async with session.get(f'{DOMAIN}/{code}', headers={"Referer": 'https://world2our.com/'}) as res:
                              html = await res.text()
        soup = BeautifulSoup(html, "html.parser")
        inputs = soup.find(id="go-link").find_all(name="input")
        data = { input.get('name'): input.get('value') for input in inputs }
        await asleep(6)
        async with session.post(f"{DOMAIN}/links/go", data=data, headers={ "X-Requested-With": "XMLHttpRequest" }) as resp:
            if 'application/json' in resp.headers.get('Content-Type'):
                json_data = await resp.json()  
                return json_data['url']
            else:
                return "Something Went Wrong :("



#Usage Example:-

# url = "https://try2link.com/cc0s0bolam"
# print(await try2link(url))
