import requests
from bs4 import BeautifulSoup
import threading
from queue import Queue


# For example, search query: adele hello
# 'https://www.youtube.com/results?search_query=adele+hello'
DOMAIN_NAME = r'https://youtube.com'
BASE_URL = DOMAIN_NAME + r'/results?search_query='

OUTPUT_FILE = r'crawled/crawled.txt'
NUMBER_OF_THREADS = 8
queue = Queue()


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
    results = dict()
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    # Url
    results['url'] = url

    # Watch Title
    watch_title_tag = soup.find('span', {'class': 'watch-title'})
    results['watch_title'] = watch_title_tag.string.strip()

    # View Count
    view_count_tag = soup.find('div', {'class': 'watch-view-count'})
    results['view_count'] = view_count_tag.string.strip()

    return results


def write_to_file(data, file):
    with open(file, 'a') as f:
        for item in data.values():
            f.write(str(item) + '\n')
        f.write('\n')


def create_workers():
    for _ in range(NUMBER_OF_THREADS):
        t = threading.Thread(target=work)
        t.daemon = True
        t.start()


def work():
    while True:
        url = queue.get()
        print(url)
        results = crawl_detail(url)
        write_to_file(results, OUTPUT_FILE)
        queue.task_done()


def main():
    stripped_query = ''
    open(OUTPUT_FILE, 'w').close()
    while True:
        query = str(input('Search query: '))
        stripped_query = query.strip()
        if len(stripped_query) == 0:
            print('Please enter valid search query again!')
        else:
            break
    print('You entered "' + stripped_query + '"\n')
    youtube_query = stripped_query.replace(' ', '+')
    create_workers()
    crawl_search_list(youtube_query)


if __name__ == '__main__':
    main()
