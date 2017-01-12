import os

class Searcher(object):
    """Searches files in dirs for specified string."""
    def __init__(self, currentdir, string_to_search_for):
        self.currentdir = currentdir
        self.string_to_search_for = string_to_search_for
        
        self.get_files_in_currentdir()
    
    def search_files_in_dir_for_string(self, file_list):
        for f in file_list:
            self.search_file_for_string(f)
    
    def get_files_in_currentdir(self):
        # TODO implement iterator file; iterate lines
        file_list = []
        for f in os.listdir(self.currentdir):
            if not os.path.isdir(f):
                file_list.append(f)
    
        if self.string_to_search_for:
            self.search_files_in_dir_for_string(file_list)
            
        else:    
            for f in file_list:
                print f
    
    def search_file_for_string(self, f):
        with open(f) as f:
            for line in f:
                if self.string_to_search_for in line:
                    print 'now'
    
    def search_subdir(self):
        pass