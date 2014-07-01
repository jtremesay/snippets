import json
import pprint
import sys

import clize


@clize.clize
def main(input_file=None):
    with open(input_file, 'r') if input_file is not None else sys.stdin as input_handler:
        pprint.pprint(json.load(input_handler))

if __name__ == '__main__':
    clize.run(main)
