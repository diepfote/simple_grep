import os
import print_helper

class Searcher(object):
    """Searches files in dirs for specified string."""

    isfirst = True

    def __init__(self, caller_directory, string_to_search_for):
        self.string_to_search_for = string_to_search_for

        # TODO refactor, ITERATOR should be used - eliminate overhead
        self.dir_list = self.get_all_subdirectories_in_directory(caller_directory)

        # TESTING
        print self.dir_list

        for i in range(self.dir_list.__len__() -1):
            self.get_files_in_currentdir(self.dir_list[i])


    # TODO call recursively
    def get_all_subdirectories_in_directory(self, curdir):
        dir_list = [curdir]
        for f in os.listdir(curdir):
            if os.path.isdir(f):
                dir_list.append(curdir + "/" + f)

        return dir_list

    # Build list with files in current directory
    def get_files_in_currentdir(self, curdir):
        file_list = []

        # TESTING
        print curdir + "right here"

        for f in os.listdir(curdir):
            if not os.path.isdir(f):
                file_list.append(f)

        # If there is a string to search --> do function call
        if self.string_to_search_for:
            matched_file_dict = self.search_files(file_list, curdir)

            # If there were any matches --> do print
            if matched_file_dict:
                print_helper.print_matched_files(matched_file_dict)

        # stub
        else:
            for f in file_list:
                print f

    # Loop through files
    def search_files(self, file_list, curdir):
        matched_file_dict = {}

        for f in file_list:
            matched_line_dict = self.search_file_for_string(f, curdir)

            if matched_line_dict:
                matched_file_dict[f] = matched_line_dict

        return matched_file_dict

    # Search a single file for occurrences of a string
    def search_file_for_string(self, file_path, curdir):
        matched_line_dict = {}
        file = curdir + "/" + file_path
        if not os.path.isdir(file):
            with open(file) as f:
                for index, line in enumerate(f):
                    if self.string_to_search_for in line:

                        matched_line_dict[index + 1] = line

        return matched_line_dict



