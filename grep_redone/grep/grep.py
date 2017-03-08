"""Search functionality for grep_redone."""

import time
import re
import sre_constants

import file_helper
from grep_redone.grep import print_helper


class Searcher(object):
    """Search functionality implemented as a class."""

    # TESTING
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

        matched_file = {}
        for f in file_helper.get_next_file(self.caller_dir, self.is_recursive):

            matched_file = self.search_file(f)
            if self.is_abs_path:
                print_helper.print_matched_files_full_path(matched_file, self.search_term)

            else:
                print_helper.print_matched_files_relative_path(matched_file, self.search_term)

        # TESTING
        print ("--- %s seconds ---" % (time.time() - start_time))
        # TESTING

        return matched_file

    def search_file(self, file_path):

        assert type(file_path) == str

        matched_line_dict = {}
        if self.is_regex_pattern:
            try:
                matched_line_dict = self.search_line_by_line_for_regex(file_path)

            except sre_constants.error, error:
                print "Regex expression error:\n\t%s" % error

        else:
            matched_line_dict = self.search_line_by_line_for_term(file_path)

        if matched_line_dict:
            matched_file = {file_path: matched_line_dict}
            return matched_file

        else:
            return {}

    def search_line_by_line_for_term(self, file_path):
        """Search a single file for occurrences of a string."""

        assert type(file_path) == str

        matched_lines = {}
        try:
            with open(file_path, 'r') as f:
                for index, line in enumerate(f):
                    if self.search_term in line:
                        # TODO 49 characters before term and 49 after
                        matched_lines[index + 1] = line[:-len(line)+100]

        except IOError, ioerror:
            print "Error while reading file: %s" % ioerror

        return matched_lines

    def search_line_by_line_for_regex(self, file_path):
        """Search a single file for a regex pattern."""

        assert type(file_path) == str

        regexp = re.compile(self.search_term)
        matched_lines = {}

        try:
            with open(file_path, 'r') as f:
                for index, line in enumerate(f):
                    if regexp.search(line):
                        # TODO 49 characters before term and 49 after
                        matched_lines[index + 1] = line[:-len(line)+100]

        except IOError, ioerror:
            print "Error while reading file:\n\t%s" % ioerror

        return matched_lines
