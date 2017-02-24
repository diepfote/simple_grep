"""Search functionality for grep_redone."""

import file_helper
from grep_redone.grep import print_helper


class Searcher(object):
    """Searches files in dirs for specified string."""

    def __init__(self, caller_dir, search_term, is_recursive):

        self.caller_dir = caller_dir
        self.search_term = search_term
        self.is_recursive = is_recursive

    def run(self):

        matched_files = self.search_files(
            file_helper.get_all_files(self.caller_dir, self.is_recursive)
        )

        # TODO add flag for full path
        if True:
            print_helper.print_matched_files_relative_path(matched_files, self.search_term)

        else:
            print_helper.print_matched_files_full_path(matched_files, self.search_term)

        return matched_files

    def search_files(self, file_paths):
        matched_files = {}

        for f in file_paths:
            matched_line_dict = self.search_file_for_string(f)

            if matched_line_dict:
                matched_files[f] = matched_line_dict

        return matched_files

    def search_file_for_string(self, file_path):
        """Search a single file for occurrences of a string."""

        matched_lines = {}
        with open(file_path, 'r') as f:
            for index, line in enumerate(f):
                if self.search_term in line:
                    matched_lines[index + 1] = line

        return matched_lines

    def search_file_for_regex(self, file_path):
        # import re
        # word = 'fubar'
        # regexp = re.compile(r'ba[rzd]')
        # if regexp.search(word):
        #     print 'matched'
        pass
