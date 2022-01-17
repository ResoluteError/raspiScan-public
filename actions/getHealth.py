import asyncio
import aiohttp

raspis = ['raspi-{}'.format(x) for x in range(1, 9)]

urls = ['http://{}.local:5000/health'.format(raspi) for raspi in raspis]

# Following snippet taken from:
# https://stackoverflow.com/questions/57126286/fastest-parallel-requests-in-python


async def get(url, session):
    try:
        async with session.get(url=url) as response:
            resp = await response.read()
            print(resp)
    except Exception as e:
        print(e)


async def main(urls):
    async with aiohttp.ClientSession() as session:
        ret = await asyncio.gather(*[get(url, session) for url in urls])

asyncio.run(main(urls))
