
"""
grep_redone; grep re-implemented in python

Usage: __main__.py [-rfe] [SEARCH_TERM] ...

Search for a string in files in a directory; optionally do this recursively.

Arguments:
  SEARCH_TERM        string to search for

Options:
  -h --help
  -r       recursive search
  -f       display full/absolute path
  -e       search term is a regex pattern

"""

import os

from docopt import docopt
from grep import grep as grep_

def main(args=None):
    args = docopt(__doc__)

    search_term = args['SEARCH_TERM'] if args['SEARCH_TERM'] else [""]

    searcher = grep_.Searcher(
        caller_dir=os.path.abspath(os.path.curdir),
        search_term=search_term[0],
        is_recursive=args['-r'],
        is_abs_path=args['-f'],
        is_regex_pattern=args['-e']
    )

    searcher.run()

if __name__ == "__main__":
    main()