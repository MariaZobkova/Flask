from time import time

from asyncio import ensure_future, gather, run
from aiohttp import ClientSession

urls = [
    'https://ru.wikipedia.org/wiki/%D0%A2%D0%BE%D0%BC%D0%B0%D1%82#/media/%D0%A4%D0%B0%D0%B9%D0%BB:Pomodorini_sulla_pianta.jpg',
    'https://ru.wikipedia.org/wiki/%D0%A2%D0%B5%D0%BF%D0%BB%D0%B8%D1%86%D0%B0#/media/%D0%A4%D0%B0%D0%B9%D0%BB:Glasshouse_crops_2.jpg',
    'https://ru.wikipedia.org/wiki/%D0%9B%D0%B8%D1%81%D1%82#/media/%D0%A4%D0%B0%D0%B9%D0%BB:Leaf_1_web.jpg',
    'https://ru.wikipedia.org/wiki/%D0%A2%D1%8B%D0%BA%D0%B2%D0%B8%D0%BD%D0%B0#/media/%D0%A4%D0%B0%D0%B9%D0%BB:Pumpkins.jpg']


async def download(url: str):
    async with ClientSession() as session:
        async with session.get(url) as response:
            content = await response.content
            filename = url.split(':')[-1]
            with open(filename, "wb") as f:
                f.write(content)
                print(f"Downloaded {url} in {time() - start_time:.2f} seconds")


async def main():
    tasks = []
    for url in urls:
        task = ensure_future(download(url))
        tasks.append(task)
    await gather(*tasks)


start_time = time()

if __name__ == '__main__':
    run(main())