
"""
grep_redone, version 0.9 
Search files for pattern or string, optionally do this recursively.

usage: grep_redone [-rnfe] [SEARCH_TERM]

Arguments:
  SEARCH_TERM       string to search for

Options:
  -h --help         Display this page.
  -r                Do a recursive search.
  -f                Display full/absolute paths.
  -e                Use the search term as a regex pattern.
  -n                Display line numbers for matches.
"""

import os

from docopt import docopt
import grep as grep_


def main():
    """Entry point for grep_redone."""
    try:
        args = docopt(__doc__)

        search_term = args['SEARCH_TERM'] if args['SEARCH_TERM'] else [""]

        searcher = grep_.Searcher(
            caller_dir=os.path.abspath(os.path.curdir),
            search_term=search_term[0],
            is_recursive=args['-r'],
            is_abs_path=args['-f'],
            is_regex_pattern=args['-e'],
            is_search_line_by_line=args['-n']
        )

        searcher.run()

    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
