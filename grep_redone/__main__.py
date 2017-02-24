"""Be able to execute grep_redone by pointing it at a working tree."""

import os
import sys

# TODO refactor command line parsing
from docopt import docopt
from grep import grep as grep_

def run_grep(string_to_search_for):
    # TODO implement
    if len(sys.argv) > 1:

        if sys.argv[1].startswith('-'):
            pass

        elif sys.argv[1] and not sys.argv[1].startswith('-'):
            string_to_search_for = sys.argv[1]

            if not string_to_search_for:
                string_to_search_for = ""

    # TODO 'is_recursive' should be a flag in the future
    grep_.Searcher(
        os.path.abspath(os.path.curdir), string_to_search_for, is_recursive=False
    )


def main(args=None):
    if sys.argv.__len__() == 1:
        run_grep(string_to_search_for="")

    elif sys.argv.__len__() == 2:
        run_grep(sys.argv[1])

    else:
        print ("""grep_redone: unrecognized option '"""
               + "\'\ngrep_redone: Use the"
               + " -h option for usage information.")

if __name__ == "__main__":
    main()