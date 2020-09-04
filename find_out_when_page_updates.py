#!/usr/bin/python
import argparse
import download_page
import datetime
import time
import os
import glob
import filecmp
from urllib.parse import urlparse

def main(source_urls, duration, period, output='.', verbose=False):
    if duration == "forever":
        forever = True
        end_time = datetime.datetime.now()
    else:
        forever = False
        end_time = datetime.datetime.now()+datetime.timedelta(hours=int(duration))
    newfile = {}
    oldfile = {}

    # Attempt to look for newest file
    for i, source in enumerate(source_urls):
        sourcenetloc = urlparse(source).netloc + "*"
        list_of_files = glob.iglob(os.path.join(output, sourcenetloc))
        try:
            oldfile[i] = max(list_of_files, key=os.path.getctime)
            oldfile[i] = os.path.basename(oldfile[i])
            print(f"[INFO] Found most recent file, {oldfile[i]}")
        except:
            print("[INFO] Most recent file not found, downloading a new reference file...")

    while forever or (end_time - datetime.datetime.now()).total_seconds() >= 0:
        print(f"[INFO] {datetime.datetime.now().isoformat()}: Attempting to download pages...")
        for i, url in enumerate(source_urls):
            if(verbose):
                print(f"[INFO] {datetime.datetime.now().isoformat()}: Attempting to download {url}")
            try:
                newfile[i] = download_page.main(url, output, verbose)
                if(verbose):
                    print(f"[INFO] Page download successful")
            except:
                print(f"[ERROR] Page download failed for {url}, continuing")
                continue

            if i in oldfile.keys():
                #If Same File
                file1 = os.path.join(output, oldfile[i])
                file2 = os.path.join(output, newfile[i])
                if(verbose):
                    print(f"[INFO] Comparing {file1} and {file2}")
                if filecmp.cmp(file1, file2):
                    print(f"[INFO] File is same, deleting...")
                    os.remove(os.path.join(output, newfile[i]))
                else:
                    oldfile[i] = newfile[i]
            else:
                oldfile[i] = newfile[i]

        print(f"[INFO] {datetime.datetime.now().isoformat()}: sleeping for {period} seconds...\n")
        time.sleep(int(period))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finds out when a page updates.')
    parser.add_argument('urls', nargs="*", help='the page(s) to find out when it changes')
    parser.add_argument('-d', '--duration', help="How long to run the script for, in hours. If not specified, it will run forever.", default="forever")
    parser.add_argument('-p', '--period', help='period of checking, in seconds. Default is 60 seconds.', default="60")
    parser.add_argument('-f', '--file', help="gets list to check from a file")
    parser.add_argument('-o', '--output', help = 'Saves the download page to a file. Default is ./out', default='./out')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action="store_true")
    args = parser.parse_args()

    urls = args.urls
    if(hasattr(args, 'file')):
        with open(args.file) as f:
            content = f.read().splitlines()
            urls = content

    main(urls, args.duration, args.period, args.output, args.verbose)