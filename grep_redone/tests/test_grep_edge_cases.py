import os
import platform
import pytest

from grep_redone.grep.grep import Searcher
from grep_redone.tests.helper_for_tests import *


def test_instantiating_searcher_class():
    caller_dir = os.curdir
    search_term = "docopt"
    is_recursive = False
    is_abs_path = False
    is_regex_pattern = False
    is_search_line_by_line = True
    searcher = Searcher(caller_dir, search_term, is_recursive, is_abs_path, is_regex_pattern, is_search_line_by_line)

    assert searcher.caller_dir == caller_dir
    assert searcher.search_term == search_term
    assert searcher.is_recursive == is_recursive
    assert searcher.is_abs_path == is_abs_path
    assert searcher.is_regex_pattern == is_regex_pattern
    assert searcher.is_search_line_by_line == is_search_line_by_line


def test_run_with_empty_str_not_regex_line_by_line(with_f_write):
    with_f_write.write('docopt\nasdfwer')
    # Rewind to read data back from file.
    with_f_write.seek(0)

    caller_dir = os.path.dirname(with_f_write.name)
    search_term = ""
    is_regex_pattern = False
    is_search_line_by_line = True

    matched_file = Searcher.run(
        Searcher(caller_dir=caller_dir,
                 search_term=search_term,
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=is_regex_pattern,
                 is_search_line_by_line=is_search_line_by_line
                 ))

    assert matched_file[with_f_write.name] == {1: 'docopt', 2: 'asdfwer'}


def test_run_with_empty_str_is_regex_line_by_line(with_f_write):
    with_f_write.write('docopt\nasdfwer')
    # Rewind to read data back from file.
    with_f_write.seek(0)

    caller_dir = os.path.dirname(with_f_write.name)
    search_term = ""
    is_regex_pattern = True
    is_search_line_by_line = True

    matched_file = Searcher.run(
        Searcher(caller_dir=caller_dir,
                 search_term=search_term,
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=is_regex_pattern,
                 is_search_line_by_line=is_search_line_by_line
                 ))

    assert matched_file[with_f_write.name] == {1: 'docopt', 2: 'asdfwer'}


def test_run_with_empty_str_not_regex_file_level(with_f_write):
    with_f_write.write('docopt\nasdfwer')
    # Rewind to read data back from file.
    with_f_write.seek(0)

    caller_dir = os.path.dirname(with_f_write.name)
    search_term = ""
    is_regex_pattern = False
    is_search_line_by_line = False

    matched_file = Searcher.run(
        Searcher(caller_dir=caller_dir,
                 search_term=search_term,
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=is_regex_pattern,
                 is_search_line_by_line=is_search_line_by_line
                 ))

    assert matched_file[with_f_write.name] == {'file': 'docopt\nasdfwer'}


def test_run_with_empty_str_is_regex_file_level(with_f_write):
    with_f_write.write('docopt\nasdfwer')
    # Rewind to read data back from file.
    with_f_write.seek(0)

    caller_dir = os.path.dirname(with_f_write.name)
    search_term = ""
    is_regex_pattern = True
    is_search_line_by_line = False

    matched_file = Searcher.run(
        Searcher(caller_dir=caller_dir,
                 search_term=search_term,
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=is_regex_pattern,
                 is_search_line_by_line=is_search_line_by_line
                 ))

    assert matched_file[with_f_write.name] == {'file': 'docopt\nasdfwer'}


@pytest.mark.skipif("platform.system() == 'Windows'")
def test_ioerror_due_to_restricted_file(with_restricted_file):

    caller_dir = with_restricted_file
    Searcher.run(Searcher(caller_dir=caller_dir,
                          search_term="",
                          is_recursive=False,
                          is_abs_path=False,
                          is_regex_pattern=False,
                          is_search_line_by_line=True))


def test_regular_expression_error_file_level(with_f_read):
    search_term = "[\\]"
    is_regex_pattern = True
    is_search_line_by_line = False
    f = with_f_read.name

    Searcher.search_f(Searcher(
        caller_dir="",
        search_term=search_term,
        is_recursive=False,
        is_abs_path=False,
        is_regex_pattern=is_regex_pattern,
        is_search_line_by_line=is_search_line_by_line),
        f)


def test_regular_expression_error_line_by_line(with_f_read):
    search_term = "[\\]"
    is_regex_pattern = True
    is_search_line_by_line = True
    f = with_f_read.name

    # Directory option is irrelevant for the test.
    Searcher.search_f(Searcher(
        caller_dir="",
        search_term=search_term,
        is_recursive=False,
        is_abs_path=False,
        is_regex_pattern=is_regex_pattern,
        is_search_line_by_line=is_search_line_by_line),
        f)
