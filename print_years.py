from argparse import ArgumentParser
import json
import sys
import os
from os.path import join as pjoin


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("path")
    return parser.parse_args()


def main(args):
    if os.path.isfile(args.path):
        json_fns = [args.path]
    json_fns = [pjoin(args.path, n) for n in sorted(os.listdir(args.path))]
    print(len(json_fns))

    for fn in json_fns:
        with open(fn) as f:
            data = json.load(f)

        names = sorted(data.keys())
        #for name, (img_url, infobox) in data.items():
        for name in names:
            img_url, infobox = data[name]
            if not infobox:
                print(f'<error> {name} No infobox')
                continue
            print(f"[{name}]", f"caption: {infobox['caption']}" if 'caption' in infobox else '', f"birth: {infobox['birth_date']}" if "birth_date" in infobox else '')

if __name__ == "__main__":
    sys.exit(main(parse_args()))
