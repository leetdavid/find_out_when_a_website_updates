#!/usr/bin/python
import argparse
import download_page
import datetime
import time
import os
import filecmp

def main(source_urls, duration, frequency, output='.', verbose=False):
    if duration == "forever":
        forever = True
        end_time = datetime.datetime.now()
    else:
        forever = False
        end_time = datetime.datetime.now()+datetime.timedelta(hours=int(duration))
    newfile = {}
    oldfile = {}
    
    while forever or (end_time - datetime.datetime.now()).total_seconds() >= 0:
        for i, url in enumerate(source_urls):
            newfile[i] = download_page.main(url, output, verbose)
            
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

        if(verbose):
            print(f"[INFO] Downloaded pages at {datetime.datetime.now().isoformat()}, sleeping for {frequency} seconds...\n")
        time.sleep(int(frequency))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Finds out when a page updates.')
    parser.add_argument('urls', nargs="+", help='the page(s) to find out when it changes')
    parser.add_argument('-d', '--duration', help="How long to run the script for, in hours. If not specified, it will run forever.", default="forever")
    parser.add_argument('-f', '--frequency', help='frequency of checking, in seconds. Default is 60 seconds.', default="60")
    parser.add_argument('-o', '--output', help = 'Saves the download page to a file. Default is ./out', default='./out')
    parser.add_argument('-v', '--verbose', help='increase output verbosity', action="store_true")
    args = parser.parse_args()
    main(args.urls, args.duration, args.frequency, args.output, args.verbose)