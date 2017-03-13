
"""
grep_redone  grep re-implemented in python with certain alterations
Usage: grep_redone [-rnfe] [SEARCH_TERM] ...

Search for str or pattern in files; optionally do this recursively.

Arguments:
  SEARCH_TERM        string to search for

Options:
  -h --help
  -r       recursive search
  -f       display full/absolute path
  -e       search term is a regex pattern
  -n       display line number for match


"""

import os

from docopt import docopt
from grep import grep as grep_


def main():
    """Entry point for grep_redone."""
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

# TESTING
    # searcher = grep_.Searcher(
    #     caller_dir='/home/flo',
    #     search_term="aware",
    #     is_recursive=args['-r'],
    #     is_abs_path=args['-f'],
    #     is_regex_pattern=False,
    #     is_search_line_by_line=False
    # )
# TESTING

    searcher.run()

if __name__ == "__main__":
    main()
