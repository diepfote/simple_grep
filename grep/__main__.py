
"""
grep_redone, version 0.9 
Search files for a pattern or string, optionally do this recursively.

usage: grep_redone [-rnfe] [SEARCH_TERM]

Arguments:
  SEARCH_TERM       The string to search for.

Options:
  -h --help         Display this page.
  -r                Do a recursive search.
  -f                Display full/absolute paths.
  -e                Use the search term as a regex pattern.
  -n                Display line numbers for matches.
"""

import os
import sys
import tempfile
import select

from docopt import docopt
import grep as grep_


def main():
    """Entry point for grep_redone."""

    temp_dir = tempfile.mkdtemp()
    fd, temp_f = tempfile.mkstemp(dir=temp_dir, suffix='.tmp', text=True)
    directory = 1
    try:

        args = docopt(__doc__)

        # If there's input ready, do something, else do something
        # else. Note timeout is zero so select won't block at all.
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            line = sys.stdin.readline()
            if line:
                f = open(temp_f, 'w')
                try:
                    f.write(line)
                    directory = os.path.dirname(f.name)

                finally:
                    f.close()
                    assert type(directory) == str

        else:  # an empty line means stdin has been closed
            directory = os.path.abspath(os.path.curdir)

        search_term = args['SEARCH_TERM'] if args['SEARCH_TERM'] else ''

        searcher = grep_.Searcher(
            caller_dir=directory,
            search_term=search_term,
            is_recursive=args['-r'],
            is_abs_path=args['-f'],
            is_regex_pattern=args['-e'],
            is_search_line_by_line=args['-n']
        )

        searcher.run()

    except KeyboardInterrupt:
        pass

    finally:
        os.close(fd)
        os.remove(temp_f)
        os.removedirs(temp_dir)

if __name__ == "__main__":
    main()
