#!/usr/bin/python3

from bs4 import BeautifulSoup as BS
from requests import get
from sys import argv
from os import mkdir
from os.path import join
import threading


import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

class Waiter:
    def __init__(self, string):
        self.string     = string
        self.is_runing  = True
        self.thread     = threading.Thread(target=self.start_waiter, daemon=True)
        self.thread.start()
    
    def stop(self):
        self.is_runing  = False
        self.thread.join()

    def start_waiter(self):
        i = 0
        chars = "/-\\|"
        while self.is_runing:
            print(f"{self.string} [{chars[i]}]", end='\r', flush=True)
            time.sleep(0.1)
            i = (i + 1) % 4
        print(f"{self.string} [✓]")

w = Waiter("Coping, please wait...")

url = argv[1]

base_url = '/'.join(url.split('/')[:3]) + '/'
loc = '/'.join(url.split('/')[3:])

def dl_all(base_dir, path):
    r = get(base_dir + path)
    bs = BS(r.text, 'html.parser')
    is_dir = False
    total = []
    for e in bs.find_all('a'):
        if e.get('href') == '../':
            is_dir = True
        else:
            total.append(e)
    if is_dir:
        try:
            mkdir(join(path))
        except:
            pass
        for e in total:
            if e.get('href'):
                dl_all(base_dir, join(path, e.get('href')))
    else:
        with open(path, 'wb+') as f:
            f.write(r.content)

dl_all(base_url, loc)
w.stop()
