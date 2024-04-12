import asyncio
import json
import logging
import os
import posixpath
import time
from asyncio import Task
from concurrent.futures import ProcessPoolExecutor

import aiofiles
import aiohttp
from aiohttp import ClientSession
from bs4 import BeautifulSoup

PAGES_AMOUNT = 250
PAGINATION_STEP = 25
SINGLE_FILE = 'mergedfile.json'


lock = asyncio.Lock()
logging.getLogger().setLevel(logging.INFO)


async def _parse_html(html: str) -> list:
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        soup = await loop.run_in_executor(pool,
                                          BeautifulSoup,
                                          html,
                                          'html.parser')
        res: list = []
        ul = soup.find("ul", class_="results")
        for li in ul.find_all("li", class_='booklink'):  # type: ignore
            try:
                title, author = li.text.strip('\n').split('\n')
            except ValueError:
                title, author = li.text.strip('\n').split('\n')[0], ''
            res.append(json.dumps({'author': author, 'title': title},
                                  sort_keys=True,
                                  indent=4))
        return res


async def write_to_file(filename: str, response: list) -> None:
    full_filename: str = os.path.join('texts', filename)
    async with lock:
        async with aiofiles.open(full_filename, 'w') as file:
            logging.debug(
                f'Writing page {filename} content to {full_filename}')
            await file.writelines(',\n'.join(response))


async def fetch_content(url: str, filename: str,
                        session: ClientSession) -> None:
    async with session.get(url) as response:
        if response.ok:
            logging.debug(f'Page {filename} found. Trying to parse...')
            html: list = await _parse_html(await response.text())
            await write_to_file(f'{filename}.json', html)
        else:
            logging.warning('Failed to get from url. Exiting.')
            raise aiohttp.ServerConnectionError()


async def get_session() -> None:
    url: str = 'https://www.gutenberg.org/ebooks/bookshelf/150' \
               '?sort_order=author&start_index='
    tasks: list = []
    async with ClientSession() as session:
        for i in range(1, PAGES_AMOUNT, PAGINATION_STEP):
            task: Task = asyncio.create_task(
                fetch_content(url + str(i), str(i), session))
            tasks.append(task)
        await asyncio.gather(*tasks)


def merge_files() -> None:
    filename_counter: int = 1
    with open(SINGLE_FILE, 'w') as newfile:
        newfile.write('[\n')
        while True:
            files: list[str] = os.listdir(posixpath.join(os.getcwd(), 'texts'))
            filename = f'{filename_counter}.json'
            if filename in files:
                logging.debug(f'{filename} was found in `texts`')
                with open(posixpath.join(
                        os.getcwd(),
                        f'texts/{filename}')) as infile:
                    contents = infile.read()
                    newfile.write(contents + ',\n')
                filename_counter += PAGINATION_STEP
            else:
                logging.debug(f'{filename} wasn\'t found in `texts`. Sleeping '
                              f'for 1 second and retrying search.')
                time.sleep(1)
            if filename_counter > PAGES_AMOUNT:
                logging.debug('All files were written to the single file.')
                break

    with open(SINGLE_FILE, 'rb+') as newfile:
        newfile.seek(-2, 2)
        newfile.truncate()
        newfile.write(b']')


def main() -> None:
    """
    Sync function to wrap async get_session(). It will be used later by
    ProcessPoolExecutor() class.
    :return: None
    """
    asyncio.run(get_session())


if __name__ == '__main__':
    start: float = time.time()
    logging.info(f"Time start: {time.strftime('%X')}")
    with ProcessPoolExecutor() as ppool:
        ppool.submit(main)
        ppool.submit(merge_files)

    logging.info(f"Time end: {time.strftime('%X')}")
    logging.info(f'======== Total time: {time.time() - start:0.2f} ========')
