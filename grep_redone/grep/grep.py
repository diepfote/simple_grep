"""Search functionality for grep_redone."""

import file_helper
import print_helper


class Searcher(object):
    """Searches files in dirs for specified string."""

    isfirst = True

    def __init__(self, caller_dir, string_to_search_for, is_recursive):

        self.string_to_search_for = string_to_search_for

        matched_files = self.search_files(
            file_helper.get_all_files(caller_dir, is_recursive)
        )

        # TODO add flag for full path
        if True:
            print_helper.print_matched_files_relative_path(matched_files)

        else:
            print_helper.print_matched_files_full_path(matched_files)


    def search_files(self, file_list):
        matched_files = {}

        for f in file_list:
            matched_line_dict = self.search_file_for_string(f)

            if matched_line_dict:
                matched_files[f] = matched_line_dict

        return matched_files

    def search_file_for_string(self, file_path):
        """Search a single file for occurrences of a string."""

        matched_lines = {}
        with open(file_path, 'r') as f:
            for index, line in enumerate(f):
                if self.string_to_search_for in line:
                    matched_lines[index + 1] = line

        return matched_lines
