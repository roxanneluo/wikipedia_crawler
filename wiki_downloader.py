from argparse import ArgumentParser
import wikipedia
import requests
import wptools
import pickle
import sys
import urllib.request as req
import urllib
import os
from os.path import join as pjoin
import json


def save_obj(obj, fn):
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    with open(fn, 'w') as f:
        json.dump(obj, f)

def load_obj(name ):
    with open('dict/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)

WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='

def get_wiki_image(search_term):
    try:
        #wkpage = wikipedia.page(search_term)
        title = search_term#wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        #print(json_data)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link
    except:
        return 0

def parse_args():
    parser = ArgumentParser()
    parser.add_argument('page_id')
    parser.add_argument('--subdir', default="")
    parser.add_argument('--check_is_person', action="store_true")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    link = wikipedia.search(args.page_id, results=1)[0]
    print(link)
    out_fn = pjoin("json", args.subdir, link + ".json")
    if os.path.isfile(out_fn):
        print(f"{out_fn} exists")
        exit(0)
    data = {}
    if args.check_is_person:
        TEMPLATE = "https://en.wikipedia.org/w/api.php?action=query&prop=templates&titles=%s&tllimit=500&format=json"
        url = TEMPLATE % urllib.parse.quote(link.replace(' ', '_'))
        uf = req.urlopen(url)
        template = str(uf.read())
        print(template)
        template_u = template.lowercase()
        if not any(x in template_u for x in ['person', 'birth date', 'death date']):
            print("not person")
            exit(-1)
    img = get_wiki_image(link)
    if img == 0:
        print("no img")
    try:
        p = wptools.page(link, silent=True).get_parse()#'Leopold II of Belgium').get_parse()
        infobox = p.data['infobox']
        data[link] = (img, infobox)
        save_obj(data, out_fn)
        print(len(data), f"caption: {infobox['caption']}" if 'caption' in infobox else f"birth: {infobox['birth_date']}")
    except Exception as e:
        print(f"[Error] can't download {link}")
