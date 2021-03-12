from argparse import ArgumentParser
import pickle
import wget
import os
import urllib.request
import sys
import errno
import requests
import shutil
import time
import os.path
from os import path
from os.path import join as pjoin
import json


def load_obj(fn):
    with open(fn) as f:
        return json.load(f)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("page_id")
    parser.add_argument("--subdir", default="")
    return parser.parse_args()


args = parse_args()
out_dir = pjoin('images', args.subdir)
data = {}
year_mapper = {}
os.makedirs(out_dir, exist_ok=True)

fn_pre = pjoin(out_dir, args.page_id)
if any(os.path.isfile(fn_pre + ext) for ext in [".jpg", ".jpeg", ".png"]):
    print(f"{fn_pre} exists")
    exit(0)

data = load_obj(pjoin("json", args.subdir, args.page_id + ".json"))

for name, (img_url, infobox) in data.items():
    print(name + ' : ' + img_url)
    #if '.' not in img_url:
    #  continue
    # filepath = PATH #% year
    #f = open(filepath + name + '.txt', 'wt')
    #f.write(str(infobox))
    #f.close()
    #wget.download(img_url, 'images/' + name + ext)
    r = requests.get(img_url, stream = True)
    while r.status_code == 429:
        print('Waiting for API')
        time.sleep(0.5)
        r = requests.get(img_url, stream = True)
    if r.status_code == 200:
    # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        r.raw.decode_content = True

        # Open a local file with wb ( write binary ) permission.
        _, ext = os.path.splitext(img_url)
        with open(fn_pre + ext, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    else:
        print('Image download failed. Status code: ' + str(r.status_code))
    #urllib.request.urlretrieve(img_url, path + name + ext)

