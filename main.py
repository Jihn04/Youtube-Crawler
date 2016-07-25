import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue
from urllib.parse import urlparse, parse_qs
from general import *
import json


# For example, search query: adele hello
# 'https://www.youtube.com/results?search_query=adele+hello'
DOMAIN_NAME = r'https://youtube.com'
BASE_URL = DOMAIN_NAME + r'/results?search_query='

NUMBER_OF_THREADS = 8
queue = Queue()
metadata = dict()


def crawl_search_list(search_query):
    url = BASE_URL + search_query
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for link in soup.findAll('a', {'class': 'yt-uix-sessionlink yt-uix-tile-'
                                            'link yt-ui-ellipsis yt-ui-ellips'
                                            'is-2 spf-link '}):
        href = DOMAIN_NAME + link.get('href')
        queue.put(href)
    queue.join()


def crawl_detail(url):
    parsed_url = urlparse(url)
    parsed_query = parse_qs(parsed_url.query)
    vid = parsed_query['v'][0]
    metadata[vid] = dict()

    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    # Url
    metadata[vid]['url'] = url

    # Watch Title
    watch_title_tag = soup.find('span', {'class': 'watch-title'})
    metadata[vid]['watch_title'] = watch_title_tag.string.strip()

    # View Count
    view_count_tag = soup.find('div', {'class': 'watch-view-count'})
    metadata[vid]['view_count'] = view_count_tag.string.strip()


def dump_file():
    create_project_dir()
    create_data_file()
    delete_file_contents('crawled/crawled.txt')
    for vid, video in metadata.items():
        append_to_file('crawled/crawled.txt', vid)
        for data in video.values():
            append_to_file('crawled/crawled.txt', data)
        append_to_file('crawled/crawled.txt', '')


def dump_json():
    create_project_dir()
    with open('crawled/crawled.json', 'w') as f:
        json.dump(metadata, f, sort_keys=True, indent=4, ensure_ascii=False)


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = queue.get()
        print(url)
        crawl_detail(url)
        queue.task_done()


def main():
    stripped_query = ''
    while True:
        query = str(input('Search query: '))
        stripped_query = query.strip()
        if len(stripped_query) == 0:
            print('Please enter valid search query again!')
        else:
            break
    print('You entered "' + stripped_query)
    youtube_query = stripped_query.replace(' ', '+')
    create_workers()
    crawl_search_list(youtube_query)
    dump_file()
    dump_json()


if __name__ == '__main__':
    main()
