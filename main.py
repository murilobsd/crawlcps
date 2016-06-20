#!/usr/bin/env python
# coding=utf-8

import argparse
import json
import sys

from cps import crawl


def get_args():
    parser = argparse.ArgumentParser(
        description='Crawler Novas Vagas CPS.')
    parser.add_argument(
        '-j', '--json', type=str, help='Arquivo json de de configuracao.',
        required=True)
    args = parser.parse_args()
    filename = args.json
    return filename


def main(filename):
    c = crawl.CPS(filename)
    c.check_vaga()


if __name__ == '__main__':
    filename = get_args()

    try:
        with open(filename) as f:
            json.loads(f.read())
    except:
        print "Erro ao abrir: %s" % filename
        sys.exit(1)

    main(filename)
