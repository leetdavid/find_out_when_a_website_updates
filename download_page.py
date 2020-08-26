#!/usr/bin/python
import argparse
import urllib3
import os
import datetime
from pathlib import Path

abspath = ''
filename = ''

def main(source_url, output='.', verbose=False):
    http = urllib3.PoolManager()
    url = urllib3.util.parse_url(source_url)

    if(verbose):
        print(f"[INFO] Attempting to download page from {url.url} ...")
    r = http.request('GET', url.url)
    if(verbose):
        print(f"[INFO] Downloaded page from {url.url}")

    abspath = os.path.abspath(output)

    if(verbose):
        print(f"[INFO] Attempting to save the downloaded file to {abspath}...")

    #Create the folders
    if(verbose):
        print(f"[INFO] Creating folders if needed {abspath}...")
    Path(abspath).mkdir(parents=True, exist_ok=True)

    #Save the File
    filename = f"{url.hostname}_{datetime.datetime.now().isoformat().replace(':', '_')}.txt"
    with open(os.path.join(abspath, filename), 'wb') as f:
        f.write(r.data)

    return filename

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Downloads the page specified from the URL.')
    parser.add_argument('url', help='the page to download')
    parser.add_argument('-o', '--output', help = 'Saves the download page to a file.', default='.')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action="store_true")
    args = parser.parse_args()
    main(args.url, args.output, args.verbose)