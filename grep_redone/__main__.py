import os
import sys

from grep import grep as grep_
def main(args=None):
    if sys.argv.__len__() < 2:
        print "grep_redone: No string to search for. Exiting."
    elif sys.argv[1] == '-h':
        pass
    elif sys.argv[1].__class__ == str:
        string_to_search_for = sys.argv[1]
        currentdir = os.path.abspath(os.path.curdir)
        grep_.Searcher(currentdir, string_to_search_for)
        
    else:
        print ("""grep_redone: unrecognized option '""" 
            + sys.argv[1] + "\'\ngrep_redone: Use the"
            + " -h option for usage information.")

if __name__ == "__main__":
    main()