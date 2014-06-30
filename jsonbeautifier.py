import json
import pprint

import clize


@clize.clize
def main(input_file, output_file=None):
    with open(input_file, 'r') as input_handler:
        pprint.pprint(json.load(input_handler))

if __name__ == '__main__':
    clize.run(main)
