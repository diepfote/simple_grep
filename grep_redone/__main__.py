import os
import sys

from grep import grep as grep_
def main(args=None):
    
    string_to_search_for = ""
    is_to_search = False
    currentdir = os.path.abspath(os.path.curdir)
    
    if sys.argv.__len__() == 2:
        
        if sys.argv[1] == '-h':
            pass
        
        elif sys.argv[1] and not sys.argv[1].startswith('-'):
            is_to_search = True
            string_to_search_for = sys.argv[1]
            
        else:
            print ("""grep_redone: unrecognized option '""" 
                   + "\'\ngrep_redone: Use the"
                   + " -h option for usage information.")
    
    if is_to_search:        
        grep_.Searcher(currentdir, string_to_search_for)

if __name__ == "__main__":
    main()
