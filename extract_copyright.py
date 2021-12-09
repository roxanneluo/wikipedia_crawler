from argparse import (
    ArgumentParser,
    Namespace,
)
import json
import os
from os.path import join
import unicodedata

import requests
from tqdm import tqdm
import numpy as np


def extract_wiki_paths(url_json_fns: str):
    wikipaths = {}
    for fn in url_json_fns:
        with open(fn) as f:
            urls = json.load(f)
        wikipaths.update({name: v[0] for name, v in urls.items()})
    return wikipaths


def query_metas(wikipaths):
    TEMPLATE = "https://commons.wikimedia.org/w/api.php?action=query&titles=Image:{}&prop=imageinfo&iiprop=extmetadata&format=json"

    metas = {}
    for name, url in tqdm(wikipaths.items()):
        try:
            response = requests.get(TEMPLATE.format(os.path.basename(url)))
            meta = json.loads(response.text)
        except Exception as e:
            print(f'[ERROR] {name} - {url}', meta)
        meta['image_url'] = url
        metas[name] = meta
    return metas


def extract_copyrights(metas):
    PAGE_URL_TEMPLATE = 'https://en.wikipedia.org/wiki/File:{}'

    headers = ['Name', 'page_url', 'image_url', 'Source', 'LicenseShortName', 'License']
    copyrights = []
    for name, meta in tqdm(metas.items()):
        try:
            url = meta['image_url']
            page_url = PAGE_URL_TEMPLATE.format(os.path.basename(url))
            imageinfo = list(meta['query']['pages'].values())[0]['imageinfo'][0]['extmetadata']
            source = imageinfo['Credit']
            license = imageinfo['License']
            license_short_name = imageinfo['LicenseShortName']
            copyrights.append(
                [name, page_url, url]
               +[' '.join(v['value'].split()) for v in [source, license_short_name, license]]
            )
        except Exception as e:
            print(f'[ERROR] {name} - {e}') #\n{meta}')
    return headers, np.array(copyrights), set(r[0] for r in copyrights)


def filter_names(d, names):
    names = {unicodedata.normalize('NFC', n) for n in names}
    d = {unicodedata.normalize('NFC', k): v for k, v in d.items()}

    names = {os.path.splitext(os.path.basename(n))[0] for n in names}
    names = {n.split('_')[0] for n in names}
    filtered = {k: v for k, v in d.items() if k in names}
    print('Uncovered names: ', names - filtered.keys())
    return filtered, names


def main(args: Namespace):
    wikipaths = extract_wiki_paths(args.url_json)

    if len(args.names) > 0: #and args.reload:
        wikipaths, names = filter_names(wikipaths, args.names)

    if args.samples is not None:
        wikipaths = {k: wikipaths[k] for k in list(wikipaths.keys())[:args.samples]}

    print(f'#wikipaths = {len(wikipaths)}')

    if os.path.isfile(args.meta) and not args.reload:
        with open(args.meta) as f:
            metas = json.load(f)
    else:
        metas = query_metas(wikipaths)
        os.makedirs(os.path.dirname(args.meta), exist_ok=True)
        with open(args.meta, 'w') as f:
            json.dump(metas, f)

    if len(args.names) > 0:
        metas, names = filter_names(metas, args.names)

    headers, copyrights, cp_names = extract_copyrights(metas)
    os.makedirs(os.path.dirname(args.copyright), exist_ok=True)
    print(f'#copyrights = {len(copyrights)}')
    print('Uncovered names: ', names - cp_names)
    print('\t'.join(headers))
    np.savetxt(args.copyright, copyrights, delimiter='\t', fmt='%s')


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("--url_json", nargs='+', help="path to the .json that has all the urls")
    parser.add_argument("--meta", help="output path to the .json file that saves all the meta file")
    parser.add_argument("--copyright", help="output path to the .tsv file that saves all the copyrights.")
    parser.add_argument("--samples", type=int, default=None, help="#samples")
    parser.add_argument("--reload", action='store_true', help="reload files")
    parser.add_argument("--names", nargs='*', help="names to filter the results")
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
