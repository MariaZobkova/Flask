import requests
from time import time
from multiprocessing import Process

urls = [
    'https://ru.wikipedia.org/wiki/%D0%A2%D0%BE%D0%BC%D0%B0%D1%82#/media/%D0%A4%D0%B0%D0%B9%D0%BB:Pomodorini_sulla_pianta.jpg',
    'https://ru.wikipedia.org/wiki/%D0%A2%D0%B5%D0%BF%D0%BB%D0%B8%D1%86%D0%B0#/media/%D0%A4%D0%B0%D0%B9%D0%BB:Glasshouse_crops_2.jpg',
    'https://ru.wikipedia.org/wiki/%D0%9B%D0%B8%D1%81%D1%82#/media/%D0%A4%D0%B0%D0%B9%D0%BB:Leaf_1_web.jpg',
    'https://ru.wikipedia.org/wiki/%D0%A2%D1%8B%D0%BA%D0%B2%D0%B8%D0%BD%D0%B0#/media/%D0%A4%D0%B0%D0%B9%D0%BB:Pumpkins.jpg']


def download(url: str):
    response = requests.get(url)
    filename = url.split(':')[-1]
    with open(filename, "wb") as f:
        f.write(response.content)
        print(f"Downloaded {url} in {time() - start_time:.2f} seconds")


processes = []
start_time = time()

if __name__ == '__main__':
    for url in urls:
        process = Process(target=download, args=(url,), daemon=True)
        processes.append(process)
        process.start()
    for process in processes:
        process.join()