"""Search functionality for simple_grep."""

import re
import sre_constants
import sys

from . import print_helper
from . import file_helper


class Searcher(object):
    """Grep's search functionality implemented as a class."""

    def __init__(self, caller_dir, search_term, specific_file, is_recursive,
                 is_abs_path, is_regex_pattern, is_search_line_by_line,
                 is_from_stdin):

        assert type(caller_dir) == str
        assert type(search_term) == str
        assert type(specific_file) == str
        assert type(is_recursive) == bool
        assert type(is_abs_path) == bool
        assert type(is_regex_pattern) == bool
        assert type(is_search_line_by_line) == bool
        assert type(is_from_stdin) == bool

        self.caller_dir = caller_dir
        self.search_term = search_term
        self.specific_file = specific_file
        self.is_recursive = is_recursive
        self.is_abs_path = is_abs_path
        self.is_regex_pattern = is_regex_pattern
        self.is_search_line_by_line = is_search_line_by_line
        self.is_from_stdin = is_from_stdin

    def __repr__(self):
        return (
            self.__class__.__name__ +
            ('(caller_dir="{}",'
             ' search_term="{}", '
             'specific_file="{}", '
             'is_recursive={}, '
             'is_abs_path={},'
             ' is_regex_pattern={}, '
             'is_search_line_by_line={}, '
             'is_from_stdin={})'.format(
                 self.caller_dir, self.search_term, self.specific_file,
                 self.is_recursive, self.is_abs_path, self.is_regex_pattern,
                 self.is_search_line_by_line, self.is_from_stdin)))

    def run(self):
        """Starts a search (using a file when specified)"""

        all_matched = []
        if self.specific_file == '':
            for f in file_helper.get_next_file(self.caller_dir,
                                               self.is_recursive):
                matched_file = self.search_wrapper(f)

                if matched_file:
                    self.printing(matched_file)
                    all_matched.extend(matched_file)

        else:
            matched_file = self.search_wrapper(self.specific_file)

            if matched_file:
                self.printing(matched_file)
                all_matched.extend(matched_file)

        return all_matched

    def printing(self, matched_file):
        """Prints a matching file or line."""

        if self.is_abs_path:
            print_helper.generate_output_for_matched_files_full_path(
                matched_file, self.search_term, self.is_from_stdin,
                self.is_search_line_by_line)

        else:
            print_helper.generate_output_for_matched_files_relative_path(
                matched_file, self.search_term, self.is_from_stdin,
                self.is_search_line_by_line)

    def search_wrapper(self, file_path):
        """Wraps search_f to accommodate for errors."""

        matched_file = {}
        try:
            matched_file = self.search_f(file_path)

        except IOError as io_error:
            pass

        except UnicodeDecodeError as unicode_error:
            pass

        return matched_file

    def with_read(self, file_path):
        def wrapper(func):
            matched = {}
            with open(file_path, 'r') as f:
                matched = func(self, f)
            return matched

        return wrapper

    def search_f(self, file_path):
        """Starts a search."""

        assert type(file_path) == str

        matched_line_dict = {}
        if self.is_search_line_by_line:
            if self.is_regex_pattern:
                try:
                    matched_line_dict = self.search_line_by_line_for_regex_wrapper(
                        file_path)

                except sre_constants.error as regex_error:
                    pass
            else:
                matched_line_dict = self.search_line_by_line_for_term_wrapper(
                    file_path)

        else:
            if self.is_regex_pattern:
                try:
                    matched_line_dict = self.match_f_for_pattern_wrapper(
                        file_path)
                except sre_constants.error as regex_error:
                    pass
            else:
                matched_line_dict = self.match_f_for_str_wrapper(file_path)

        if matched_line_dict:
            return {file_path: matched_line_dict}
        else:
            return None

    def match_f_for_str_wrapper(self, file_path):
        @self.with_read(file_path)
        def match_f_for_str(self, f):
            """Searches a file for the occurrence of a string."""

            assert type(file_path) == str

            entire_file = ''
            f.seek(0)
            for line in f.readlines():
                entire_file += line

            # Match literal str not regex pattern
            regexp = re.compile(re.escape(self.search_term))
            matches = regexp.findall(entire_file)
            match = ""
            try:
                match = matches.pop()

            except IndexError:
                pass

            matched = {}
            previous = []

            if self.search_term == '':
                return {'file': entire_file}

            if match:
                # Do not include matches if file is binary
                if file_helper.is_binary_file(file_path):
                    return {'file_matched': ''}

                for index, line in enumerate(entire_file.split()):

                    if match in line:
                        previous.append(line)
                        matched[index] = line

            return matched

        return match_f_for_str

    def match_f_for_pattern_wrapper(self, file_path):
        @self.with_read(file_path)
        def match_f_for_pattern(self, f):
            """Searches a file using a pattern."""

            assert type(file_path) == str

            entire_file = ''
            f.seek(0)
            entire_file = ""
            for line in f.readlines():
                entire_file += line

            regexp = re.compile(self.search_term)
            matches = regexp.findall(entire_file)
            match = ""
            try:
                match = matches.pop()

            except IndexError:
                pass

            previous = []
            matched = {}

            if self.search_term == '':
                return {'file': entire_file}

            if match:
                # Do not include matches if file is binary
                if file_helper.is_binary_file(file_path):
                    return {'file_matched': ''}

                for index, line in enumerate(entire_file.split()):

                    if match in line:
                        previous.append(line)
                        matched[index] = line

            return matched

        return match_f_for_pattern

    def search_line_by_line_for_term_wrapper(self, file_path):
        @self.with_read(file_path)
        def search_line_by_line_for_term(self, f):
            """
                    Searches a single file for occurrences of a string.
                    Each line is searched separately.
            """

            assert type(file_path) == str

            matched_lines = {}
            for line_num, line in enumerate(f):

                if self.search_term == '':
                    matched_lines[line_num + 1] = line.strip()

                elif self.search_term in line:
                    # Do not include matches if file is binary
                    if file_helper.is_binary_file(file_path):
                        return {'file_matched': ''}

                    split_str = line.split(self.search_term)
                    matched_lines[line_num + 1] = (
                        split_str[0] + self.search_term +
                        split_str[1][:-len(split_str[1]) + len(
                            split_str[0] + self.search_term)]).strip()

            return matched_lines

        return search_line_by_line_for_term

    def search_line_by_line_for_regex_wrapper(self, file_path):
        @self.with_read(file_path)
        def search_line_by_line_for_regex(self, f):
            """
                    Searches a file using a regex pattern.
                    Each line is searched separately.
            """

            assert type(file_path) == str

            regexp = re.compile(self.search_term)
            matched_lines = {}

            for line_num, line in enumerate(f):

                if self.search_term == '':
                    matched_lines[line_num + 1] = line.strip()

                match = regexp.findall(line)
                if match:
                    # Do not include matches if file is binary
                    if file_helper.is_binary_file(file_path):
                        return {'file_matched': ''}

                    for row in match:
                        if not row:
                            del row

                    try:
                        split_str = line.split(match[0])
                        matched_lines[line_num + 1] = (
                            split_str[0] + match[0] +
                            split_str[1][:-len(split_str[1]) + len(
                                split_str[0] + match[0])]).strip()

                    # Catch empty separator
                    except ValueError:
                        matched_lines[line_num + 1] = line.strip()

            return matched_lines

        return search_line_by_line_for_regex
