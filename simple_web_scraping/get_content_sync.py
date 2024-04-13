import json
import os
import posixpath
import time

import requests
from bs4 import BeautifulSoup


def _parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    res = []
    ul = soup.find("ul", class_="results")
    for li in ul.find_all("li", class_='booklink'):
        try:
            title, author = li.text.strip('\n').split('\n')
        except ValueError:
            title, author = li.text.strip('\n').split('\n')[0], ''
        res.append(json.dumps({'author': author, 'title': title}))
    return res


def write_to_file(filename, response):
    filename = os.path.join('texts', filename)
    with open(filename, 'w') as file:
        file.writelines(',\n'.join(response))


def fetch_content(url, filename, session):
    response = session.get(url)
    if response.ok:
        html = _parse_html(response.text)
        print(f'Before write {filename}.json')
        write_to_file(f'{filename}.json', html)
        print(f'After write {filename}.json')
    else:
        raise Exception


def get_session():
    url = 'https://www.gutenberg.org/ebooks/bookshelf/150' \
          '?sort_order=author&start_index='
    with requests.Session() as session:
        for i in range(1, 250, 25):
            fetch_content(url + str(i), str(i), session)


def merge_files():
    filename_counter = 1
    with open('mergedfile.json', 'w') as newfile:
        newfile.write('[\n')
        while True:
            files = os.listdir(posixpath.join(os.getcwd(), 'texts'))
            if f'{filename_counter}.json' in files:
                print(f'{filename_counter}.json was found. Writing to merged')
                with open(posixpath.join(
                        os.getcwd(),
                        f'texts/{filename_counter}.json')) as infile:
                    contents = infile.read()
                    newfile.write(contents + ',\n')
                filename_counter += 25
            else:
                print(f'{filename_counter}.json wasn\'t found. Sleep for 1 s.')
                time.sleep(1)
            if filename_counter > 250:
                break

    with open('mergedfile.json', 'rb+') as newfile:
        newfile.seek(-2, 2)
        newfile.truncate()
        newfile.write(b']')


if __name__ == '__main__':
    start = time.time()
    print(f"Time start: {time.strftime('%X')}")
    # with ProcessPoolExecutor() as pool:
    #     pool.submit(get_session)
    #     pool.submit(merge_files)
    get_session()
    print(f"Download finished: {time.strftime('%X')}")
    print(f'======== Download time: {time.time() - start:0.2f} ========')

    merge_files()
    print(f"Time end: {time.strftime('%X')}")
    print(f'======== Total time: {time.time() - start:0.2f} ========')
