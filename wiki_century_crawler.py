#!/usr/bin/env python3
# Download the names from "Significant people" in the century pages

from argparse import ArgumentParser
import wikipediaapi
import wikipedia
import requests
import json
import wptools
import pickle
import sys
import urllib.request as req
import urllib
import os
from os.path import join as pjoin


def parse_args():
    parser = ArgumentParser("Download names and json from wiki century page")
    parser.add_argument("page")
    return parser.parse_args()


def save(fn, obj):
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    with open(fn, "w") as f:
        json.dump(obj, f)


def parse(content, links):
    results = {}
    for k, v in links.items():
        if k in content:
            results[k] = v
    return results


def get_wiki_image(search_term):
    WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='
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



def main(args):
    wiki_wiki = wikipediaapi.Wikipedia('en')
    page = wiki_wiki.page(args.page)

    sec = [s for s in page.sections if s.title == "Significant people"][0]
    links = parse(str(sec), page.links)
    names = [v.title for k, v in links.items() if v.fullurl]
    print(names, len(names))

    data = {}
    for name in names:
        img = get_wiki_image(name)
        if img == 0:
            print(f"{name} has no image")
            continue
        p = wptools.page(name, silent=True).get_parse()#'Leopold II of Belgium').get_parse()
        infobox = p.data['infobox']
        data[name] = (img, infobox)
    save(pjoin("json", f"{args.page}.json"), data)
    print(len(data))


if __name__ == "__main__":
    main(parse_args())

