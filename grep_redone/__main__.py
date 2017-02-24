import os
import sys

from grep import grep as grep_

def run_grep(string_to_search_for, is_recursive):
    # TODO implement
    if len(sys.argv) > 1:

        if sys.argv[1].startswith('-h'):

        elif sys.argv[1] and not sys.argv[1].startswith('-'):
            string_to_search_for = sys.argv[1]

            if not string_to_search_for:
                string_to_search_for = ""

    print is_recursive
    grep_.Searcher(os.path.abspath(os.path.curdir), string_to_search_for, is_recursive)


def main(args=None):
    if sys.argv.__len__() == 1:
        run_grep(string_to_search_for="", is_recursive=False)

    elif sys.argv.__len__() == 2:
        run_grep(sys.argv[1], is_recursive=False)

    # For testing; should be a flag in the future
    elif sys.argv.__len__() == 3:
        run_grep(sys.argv[1], sys.argv[2])

    else:
        print ("""grep_redone: unrecognized option '"""
               + "\'\ngrep_redone: Use the"
               + " -h option for usage information.")

if __name__ == "__main__":
    main()