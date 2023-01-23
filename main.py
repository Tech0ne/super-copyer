#!/usr/bin/python3

from bs4 import BeautifulSoup as BS
from requests import get
from sys import argv
from os import mkdir
from os.path import join

url = argv[1]
loc = argv[2]

base_url = '/'.join(url.split('/')[:3]) + '/'

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
