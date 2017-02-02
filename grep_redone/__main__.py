import os
import sys

from grep import grep as grep_


def main(args=None):
    string_to_search_for = ""

    if sys.argv.__len__() == 2:

        # TODO implement
        if sys.argv[1] == '-h':
            pass

        elif sys.argv[1] and not sys.argv[1].startswith('-'):
            is_searchable = True
            string_to_search_for = sys.argv[1]
            grep_.Searcher(os.path.abspath(os.path.curdir), string_to_search_for)

        else:
            print ("""grep_redone: unrecognized option '"""
                   + "\'\ngrep_redone: Use the"
                   + " -h option for usage information.")

    else:
        grep_.Searcher(os.path.abspath(os.path.curdir), "")
        # raise RuntimeError("No string to search for. Exiting.")

if __name__ == "__main__":
    main()
