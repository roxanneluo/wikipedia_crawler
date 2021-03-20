from argparse import ArgumentParser
import json
import sys
import os
from os.path import join as pjoin

import cv2


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("dir_path")
    return parser.parse_args()


def main(args):
    names = os.listdir(args.dir_path)
    for name in names:
        if name.endswith('.json'):
            continue
        im = cv2.imread(pjoin(args.dir_path, name))
        if im.shape[0] < 400:
            print(name, im.shape)


if __name__ == "__main__":
    sys.exit(main(parse_args()))
