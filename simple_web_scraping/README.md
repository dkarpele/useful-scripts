# Simple web scraping

2 scripts do the same thing: download names of book authors and book titles from the gutenberg.org library and save them to the file. The first script is in a sync manner, the second is an async script.

1. Download names of book authors and book titles from the gutenberg.org library. Save them into the file. Do it for every page using link (1 file per 1 page):
https://www.gutenberg.org/ebooks/bookshelf/150?sort_order=author&start_index=1.
Replace last digit with the number.

2. Merge all files to one file with all data.

## Sync script
```get_content_sync.py```

It downloads data one by one using `request` library and saves to the file. After that all files merge to one file.

### Time:

```commandline
Time start: 16:28:05
Download finished: 16:28:08
======== Download time: 3.33 ========
Time end: 16:28:08
======== Total time: 3.33 ===========
```

## Async script
```get_content_async.py```

It downloads all data simultaneously using `asyncio` library and saves to the file. At the same time merging single files to one file starts in the separate process using `concurrent.futures.ProcessPoolExecutor`.

### Time:

It's not possible to separate downloading and merging time.
```commandline
Time start: 16:33:38
Time end: 16:33:39
======== Total time: 1.01 ========
```

## Results
As expected async script runs much faster than sync script for IO operation even against very small amount of data.
