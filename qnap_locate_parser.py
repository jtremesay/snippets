#!/usr/bin/env python3

import json
import sys

import clize


def get_file_handler(input_file):
    if input_file is None:
        return sys.stdin

    return open(input_file, 'r')


@clize.clize
def main(input_file=None):
    result = {'datas': []}
    with get_file_handler(input_file) as input_handler:
        result = json.load(input_handler)

    for data in result['datas']:
        print(data['filename'])


if __name__ == '__main__':
    clize.run(main)
