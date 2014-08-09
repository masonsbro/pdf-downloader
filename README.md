pdf-downloader
==============

Crawl a website and download all the .pdf files on it. Note that if you use, say, '/', as the target directory, it will save them to root.

```
usage: main.py [-h] [-p PREFIX] base target

positional arguments:
  base                  URL at which to start the crawl
  target                Directory in which to store the downloaded files

optional arguments:
  -h, --help            show this help message and exit
  -p PREFIX, --prefix PREFIX
                        Remove this prefix from all files where it is present
```
