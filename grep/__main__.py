
"""
grep_redone, version 0.9 

usage: grep_redone [-rnpe] [SEARCH_TERM] [FILE_TO_SEARCH] 

Arguments:
  SEARCH_TERM
  FILE_TO_SEARCH
  
Options:
  -h --help         
  -r                Search directory recursively.
  -p                Display full/absolute paths for matches.
  -e                Use the search term as a regex pattern.
  -n                Display line numbers for matches.
"""

import os
import sys
import tempfile
import select
import platform

from docopt import docopt
from . import grep as grep_


def main():
    """Entry point for grep_redone."""

    temp_dir = tempfile.mkdtemp()
    fd, temp_f = tempfile.mkstemp(dir=temp_dir, suffix='.tmp', text=True)
    directory = 1
    is_from_stdin = False
    try:
        args = docopt(__doc__)

        # If there's input ready, do something, else do something
        # else. Note timeout is zero so select won't block at all.
        if platform.system() == 'Windows':
            f = args['FILE_TO_SEARCH']
            if f:
                if os.path.isdir(os.path.abspath(f)):
                    directory = f
                    args['FILE_TO_SEARCH'] = ''

            else:
                directory = os.path.abspath(os.path.curdir)

        else:
            is_from_stdin = sys.stdin in select.select([sys.stdin], [], [], 0)[0]
            if is_from_stdin:
                f = open(temp_f, 'w')
                try:
                    f.write(sys.stdin.read())
                    directory = os.path.dirname(f.name)

                finally:
                    f.close()
                    assert type(directory) == str

            else:  # An empty line means stdin has been closed.
                # Check if the specified path is a directory.
                f = args['FILE_TO_SEARCH']
                if f:
                    if os.path.isdir(os.path.abspath(f)):
                        directory = f
                        args['FILE_TO_SEARCH'] = ''

                    else:
                        directory = ''

                else:
                    directory = os.path.abspath(os.path.curdir)

        search_term = args['SEARCH_TERM'] if args['SEARCH_TERM'] else ''
        specific_file = args['FILE_TO_SEARCH'] if args['FILE_TO_SEARCH'] else ''

        searcher = grep_.Searcher(
            caller_dir=directory,
            search_term=search_term,
            specific_file=specific_file,
            is_recursive=args['-r'],
            is_abs_path=args['-p'],
            is_regex_pattern=args['-e'],
            is_search_line_by_line=args['-n'],
            is_from_stdin=is_from_stdin
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
