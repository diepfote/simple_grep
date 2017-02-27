"""Search functionality for grep_redone."""

import time
import re
import sre_constants

import file_helper
from grep_redone.grep import print_helper


class Searcher(object):
    """Search functionality implemented as a class."""

    #TESTING
    global start_time
    start_time = time.time()
    # TESTING

    def __init__(self, caller_dir, search_term, is_recursive, is_abs_path, is_regex_pattern):

        assert type(caller_dir) == str
        assert type(search_term) == str
        assert type(is_recursive) == bool
        assert type(is_abs_path) == bool
        assert type(is_regex_pattern) == bool

        self.caller_dir = caller_dir
        self.search_term = search_term
        self.is_recursive = is_recursive
        self.is_abs_path = is_abs_path
        self.is_regex_pattern = is_regex_pattern

    def run(self):

        files = file_helper.get_all_files(self.caller_dir, self.is_recursive)
        matched_files = self.search_files(files)

        if self.is_abs_path:
            print_helper.print_matched_files_full_path(matched_files, self.search_term)

        else:
            print_helper.print_matched_files_relative_path(matched_files, self.search_term)

        # TESTING
        print("--- %s seconds ---" % (time.time() - start_time))
        # TESTING

        return matched_files

    def search_files(self, file_paths):
        """Look through all files supplied by the file_helper."""

        assert type(file_paths) == list
        matched_files = {}

        for f in file_paths:
            matched_line_dict = {}

            if self.is_regex_pattern:
                try:
                    matched_line_dict = self.search_file_for_regex(f)

                except sre_constants.error, error:
                    print "Regex expression error:\n\t%s" % error
                    break

            else:
                matched_line_dict = self.search_file_for_string(f)

            if matched_line_dict:
                matched_files[f] = matched_line_dict

        return matched_files

    def search_file_for_string(self, file_path):
        """Search a single file for occurrences of a string."""

        assert type(file_path) == str
        matched_lines = {}

        try:
            with open(file_path, 'r') as f:
                for index, line in enumerate(f):
                    if self.search_term in line:
                        matched_lines[index + 1] = line

        except IOError, ioerror:
            print "Error while reading file: %s" % ioerror

        return matched_lines

    def search_file_for_regex(self, file_path):
        """Search a single file for a regex pattern."""

        assert type(file_path) == str

        regexp = re.compile(self.search_term)
        matched_lines = {}

        try:
            with open(file_path, 'r') as f:
                for index, line in enumerate(f):
                    if regexp.search(line):
                        matched_lines[index + 1] = line

        except IOError, ioerror:
            print "Error while reading file:\n\t%s" % ioerror

        return matched_lines