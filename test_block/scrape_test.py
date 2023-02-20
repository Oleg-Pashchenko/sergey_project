import asyncio
import aiohttp

async def fetch(session, url):
    async with session.get(url) as response:
        #print(response)
        await response.text()

async def run():
    for i in range(50):
        start = time.time()
        urls = ['https://wordroot.ru/бегать'] * 35
        async with aiohttp.ClientSession() as session:
            tasks = []
            for url in urls:
                task = asyncio.ensure_future(fetch(session, url))
                tasks.append(task)
            responses = await asyncio.gather(*tasks)

            # обработка ответов
        proccess_time = time.time() - start
        print(proccess_time)
        if 1 - proccess_time > 0:
            time.sleep(1 - proccess_time)
import time


loop = asyncio.get_event_loop()
loop.run_until_complete(run())
