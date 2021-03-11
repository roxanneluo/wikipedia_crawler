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


def save_obj(obj, name ):
    os.makedirs('dict', exist_ok=True)
    with open('dict/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    os.makedirs('json', exist_ok=True)
    with open('json/' + name + '.json', 'w') as f:
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

#wiki_image = get_wiki_image('1880s')
#print(wiki_image)
if len(sys.argv) != 2:
  print("1 Argument required")
  exit()
link = sys.argv[1]
data = {}
TEMPLATE = "https://en.wikipedia.org/w/api.php?action=query&prop=templates&titles=%s&tllimit=500&format=json"
print(link)
if os.path.isfile(pjoin('dict', link + ".pkl")) and os.path.isfile(pjoin('json', link + ".json")):
    print(f"{link} exists")
    exit(0)
#if not link.isascii():
#  continue
url = TEMPLATE % urllib.parse.quote(link.replace(' ', '_'))
uf = req.urlopen(url)
template = str(uf.read())
if 'person' not in template and 'Person' not in template and 'Birth date' not in template:
    print("not person")
img = get_wiki_image(link)
if img == 0:
    print("no img")
#print(link)
try:
    p = wptools.page(link, silent=True).get_parse()#'Leopold II of Belgium').get_parse()
    infobox = p.data['infobox']
    data[link] = (img, infobox)
    save_obj(data, sys.argv[1])
    print(len(data))
    #print(str(infobox['birth_date']))
except Exception as e:
    print(f"[Error] can't download {link}")
