import requests
from bs4 import BeautifulSoup


# For example, search query: adele hello
# 'https://www.youtube.com/results?search_query=adele+hello'
BASE_URL = 'https://youtube.com/results?search_query='


def youtube_crawler(search_query):
    url = BASE_URL + search_query
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    output_file = r'crawled/crawled.txt'
    open(output_file, 'w').close()
    for link in soup.findAll('a', {'class': 'yt-uix-sessionlink yt-uix-tile-'
                                   'link yt-ui-ellipsis yt-ui-ellipsis-2 spf'
                                   '-link '}):
        href = 'https://youtube.com' + link.get('href')
        title = link.string
        view_count = get_single_item_data(href)
        print(href)
        print(title)
        print(view_count + '\n')
        with open(output_file, 'a') as f:
            f.write(href + '\n')
            f.write(title + '\n')
            f.write(view_count + '\n\n')


def get_single_item_data(item_url):
    source_code = requests.get(item_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    for item_name in soup.findAll('div', {'class': 'watch-view-count'}):
        return item_name.string


def main():
    stripped_query = ''
    while True:
        query = str(input('Search query: '))
        stripped_query = query.strip()
        if len(stripped_query) == 0:
            print('Please enter valid search query again!')
        else:
            break
    print('You entered "' + stripped_query + '"\n')
    youtube_query = stripped_query.replace(' ', '+')
    youtube_crawler(youtube_query)


if __name__ == '__main__':
    main()
