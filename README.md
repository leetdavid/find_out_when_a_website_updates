## download_page.py
```
usage: download_page.py [-h] [-o OUTPUT] [-v] url

Downloads the page specified from the URL.

positional arguments:
  url                   the page to download

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Saves the download page to a file.
  -v, --verbose         increase output verbosity
```

## find_when_page_updates.py
This script requires download_page.py to be in the same working folder.
```
usage: find_when_page_updates.py [-h] [-d DURATION] [-f FREQUENCY] [-o OUTPUT] [-v] urls [urls ...]

Finds out when a page updates.

positional arguments:
  urls                  the page(s) to find out when it changes

optional arguments:
  -h, --help            show this help message and exit
  -d DURATION, --duration DURATION
                        How long to run the script for, in hours. If not specified, it will run forever.
  -f FREQUENCY, --frequency FREQUENCY
                        frequency of checking, in seconds. Default is 60 seconds.
  -o OUTPUT, --output OUTPUT
                        Saves the download page to a file. Default is ./out
  -v, --verbose         increase output verbosity
```

# Examples
```
$ python download_page.py google.com -o out
```
This will download google.com, and save it to a folder called 'out'.

```
$ python find_when_page_updates.py https://www.shobserver.com/journal/getHomePage.htm http://paper.people.com.cn/rmrb/ -d 24 -f 5 -o out -v
```
This will download the two pages mentioned, run for 24 hours, download every 5 seconds, and save the downloaded files to a folder called 'out', in verbose mode.
