import os
from clint.textui import colored 

class Searcher(object):
    """Searches files in dirs for specified string."""
    def __init__(self, currentdir, string_to_search_for):
        self.currentdir = currentdir
        self.string_to_search_for = string_to_search_for
        
        self.get_files_in_currentdir()
    
    def get_files_in_currentdir(self):
        # TODO implement iterator file; iterate lines
        file_list = []
        for f in os.listdir(self.currentdir):
            if not os.path.isdir(f):
                file_list.append(f)
    
        if self.string_to_search_for:
            matched_file_dict = self.search_files_in_dir_for_string(file_list)
            
            if matched_file_dict:
                self.print_nicely(matched_file_dict)
            
        else:    
            for f in file_list:
                print f


    def search_files_in_dir_for_string(self, file_list):
        matched_file_dict = {}
        
        for f in file_list:
            matched_line_dict = self.search_file_for_string(f)
            
            if matched_line_dict:
                matched_file_dict[f] = matched_line_dict
        
        return matched_file_dict

        
    def search_file_for_string(self, f):
        matched_line_dict = {}
        with open(f) as f:
            for index, line in enumerate(f):
                if self.string_to_search_for in line:
                    matched_line_dict[index+1] = line

        return matched_line_dict
                    
    
    def print_nicely(self, matched_file_dict):
        for key, value in matched_file_dict.iteritems():
            
            for k, v in value.iteritems():
                print (colored.magenta('./' + key + ':', True, False) +
                    str(k) + ':' + v),
                
                