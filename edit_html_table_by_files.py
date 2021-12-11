from argparse import ArgumentParser
import os
from os.path import join as pjoin

from bs4 import BeautifulSoup
from tqdm import tqdm
from glob import glob


def prefix(path):
    return os.path.splitext(os.path.basename(path))[0]


def remove_rows(table, names):
    names = set(prefix(n) for n in names)

    trs = table.find_all('tr')
    for tr in tqdm(trs):
        path = tr.find_all('td', limit=2)[1].img['src']
        if prefix(path) not in names:
            tr.decompose()


def remove_files(path_fmt, names):
    names = set(prefix(n) for n in names)
    matched = glob(path_fmt)
    for p in tqdm(matched):
        if prefix(p) not in names:
            os.remove(p)


def main(args):
    with open(args.html_in) as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
    table = soup.table
    assert len(soup.find_all('table')) == 1
    
    remove_rows(table, args.names)
    print(f'#rows after filtering: {len(table.find_all("tr"))}')
    
    os.makedirs(os.path.dirname(args.html_out), exist_ok=True)
    with open(args.html_out, 'wb') as f:
        f.write(soup.prettify('utf-8'))

    if args.remove_fmt is not None:
        remove_files(args.remove_fmt, args.names)


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('html_in')
    parser.add_argument('html_out')
    parser.add_argument('--names', nargs='+', help='keep only rows where its path is in names')
    parser.add_argument('--remove_fmt', default=None, help='remove files matching this format but outside <names>')
    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
