# Написать программу, которая скачивает изображения с заданных URL-адресов и сохраняет их на диск.
# Каждое изображение должно сохраняться в отдельном файле, название которого соответствует названию
# изображения в URL-адресе.
# Например, URL-адрес: https://example/images/image1.jpg -> файл на диске: image1.jpg
# — Программа должна использовать многопоточный, многопроцессорный и асинхронный подходы.
# — Программа должна иметь возможность задавать список URL-адресов через аргументы командной строки.
# — Программа должна выводить в консоль информацию о времени скачивания каждого изображения
# и общем времени выполнения программы.
from pathlib import Path

import requests
from threading import Thread
from time import sleep, time

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



threads = []
start_time = time()
for url in urls:
    thread = Thread(target=download, args=[url], daemon=True)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
