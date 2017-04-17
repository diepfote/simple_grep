import os
import platform
import pytest

from grep import print_helper
from grep import file_helper
from grep.grep import Searcher
from tests.helper_for_tests import *


def test_run_with_empty_str_not_regex_line_by_line(with_f_write):
    with_f_write.write('docopt\nasdfwer')
    with_f_write.seek(0)

    caller_dir = os.path.dirname(with_f_write.name)
    search_term = ''
    is_regex_pattern = False
    is_search_line_by_line = True

    matched_files = Searcher.run(
        Searcher(caller_dir=caller_dir,
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=is_regex_pattern,
                 is_search_line_by_line=is_search_line_by_line,
                 is_from_stdin=False
                 ))

    assert matched_files == [os.path.abspath(with_f_write.name)]


def test_run_with_empty_str_is_regex_line_by_line(with_f_write):
    with_f_write.write('docopt\nasdfwer')
    with_f_write.seek(0)

    caller_dir = os.path.dirname(with_f_write.name)
    search_term = ''
    is_regex_pattern = True
    is_search_line_by_line = True

    matched_files = Searcher.run(
        Searcher(caller_dir=caller_dir,
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=is_regex_pattern,
                 is_search_line_by_line=is_search_line_by_line,
                 is_from_stdin=False
                 ))

    assert matched_files == [os.path.abspath(with_f_write.name)]


def test_run_with_empty_str_not_regex_file_level(with_f_write):
    with_f_write.write('docopt\nasdfwer')
    with_f_write.seek(0)

    caller_dir = os.path.dirname(with_f_write.name)
    search_term = ""
    is_regex_pattern = False
    is_search_line_by_line = False

    matched_files = Searcher.run(
        Searcher(caller_dir=caller_dir,
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=is_regex_pattern,
                 is_search_line_by_line=is_search_line_by_line,
                 is_from_stdin=False
                 ))

    assert matched_files == [os.path.abspath(with_f_write.name)]


def test_run_with_empty_str_is_regex_file_level(with_f_write):
    with_f_write.write('docopt\nasdfwer')
    with_f_write.seek(0)

    caller_dir = os.path.dirname(with_f_write.name)
    search_term = ""
    is_regex_pattern = True
    is_search_line_by_line = False

    matched_files = Searcher.run(
        Searcher(caller_dir=caller_dir,
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=is_regex_pattern,
                 is_search_line_by_line=is_search_line_by_line,
                 is_from_stdin=False
                 ))

    assert matched_files == [os.path.abspath(with_f_write.name)]


@pytest.mark.skipif("platform.system() == 'Windows'")
def test_ioerror_due_to_restricted_file(with_restricted_file):

    caller_dir = with_restricted_file
    Searcher.run(Searcher(caller_dir=caller_dir,
                          search_term="",
                          specific_file='',
                          is_recursive=False,
                          is_abs_path=False,
                          is_regex_pattern=False,
                          is_search_line_by_line=True,
                          is_from_stdin=False))


def test_regular_expression_error_file_level(with_f_read):
    search_term = "[\\]"
    is_regex_pattern = True
    is_search_line_by_line = False
    f = with_f_read.name

    Searcher.search_f(Searcher(
        caller_dir='',
        specific_file='',
        search_term=search_term,
        is_recursive=False,
        is_abs_path=False,
        is_regex_pattern=is_regex_pattern,
        is_search_line_by_line=is_search_line_by_line,
                 is_from_stdin=False),
        f)


def test_regular_expression_error_line_by_line(with_f_read):
    search_term = "[\\]"
    is_regex_pattern = True
    is_search_line_by_line = True
    f = with_f_read.name

    # Directory option is irrelevant for the test.
    Searcher.search_f(Searcher(
        caller_dir='',
        search_term=search_term,
                 specific_file='',
        is_recursive=False,
        is_abs_path=False,
        is_regex_pattern=is_regex_pattern,
        is_search_line_by_line=is_search_line_by_line,
                 is_from_stdin=False),
        f)
