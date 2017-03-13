import os
import platform
import pytest

from grep_redone.grep.grep import Searcher
from grep_redone.tests.helper_for_tests import with_f_write, with_f_read, with_restricted_file, with_f_bwrite


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
    assert  searcher.is_search_line_by_line == is_search_line_by_line


def test_run(with_f_write):
    with_f_write.write('docopt')
    # Rewind to read data back from file.
    with_f_write.seek(0)

    caller_dir = os.path.dirname(with_f_write.name)
    search_term = "docopt"
    is_abs_path = True

    matched_files = Searcher.run(
        Searcher(caller_dir=caller_dir,
                 search_term=search_term,
                 is_recursive=False,
                 is_abs_path=is_abs_path,
                 is_regex_pattern=False,
                 is_search_line_by_line=True
                 ))

    assert matched_files[os.path.abspath(with_f_write.name)] == {1: "docopt"}


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


def test_search_f(with_f_write):
    with_f_write.write('sdf\na\nrghsf')
    # Rewind to read data back from file.
    with_f_write.seek(0)

    search_term = "a"
    # Directory and recursive option are irrelevant for the test.
    matched_file = Searcher.search_f(
        Searcher(caller_dir="",
                 search_term=search_term,
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=True),
        with_f_write.name)

    assert matched_file[with_f_write.name] == {2: 'a'}


def test_search_binary_f(with_f_bwrite):
    with_f_bwrite.write(b'\x07\x08\x07')
    # Rewind to read data back from file.
    with_f_bwrite.close()

    search_term = "\x07"
    try:
        with_f_bwrite = open(with_f_bwrite.name, 'rb')
        # Directory and recursive option are irrelevant for the test.
        matched_file = Searcher.search_f(
            Searcher(caller_dir="",
                     search_term=search_term,
                     is_recursive=False,
                     is_abs_path=False,
                     is_regex_pattern=False,
                     is_search_line_by_line=True),
            with_f_bwrite.name)
    finally:
        with_f_bwrite.close()

    assert matched_file == {with_f_bwrite.name: {'file_matched': ''}}


def test_match_f_for_str(with_f_write):
    with_f_write.write('sdf\na\nrghsf')
    # Rewind to read data back from file.
    with_f_write.close()

    search_term = "sdf"
    is_search_line_by_line = False
    try:
        with_f_write = open(with_f_write.name, 'r')
        # Directory and recursive option are irrelevant for the test.
        matched_file = Searcher.match_f_for_str(
            Searcher(caller_dir="",
                     search_term=search_term,
                     is_recursive=False,
                     is_abs_path=False,
                     is_regex_pattern=False,
                     is_search_line_by_line=is_search_line_by_line),
            with_f_write.name)
    finally:
        with_f_write.close()

    assert matched_file == {'file': 'sdf\na'}


def test_match_f_for_pattern(with_f_write):
    with_f_write.write('sdf\na\nrghsf')
    # Rewind to read data back from file.
    with_f_write.close()

    search_term = "sdf"
    is_search_line_by_line = False
    try:
        with_f_write = open(with_f_write.name, 'r')
        # Directory and recursive option are irrelevant for the test.
        matched_file = Searcher.match_f_for_pattern(
            Searcher(caller_dir="",
                     search_term=search_term,
                     is_recursive=False,
                     is_abs_path=False,
                     is_regex_pattern=False,
                     is_search_line_by_line=is_search_line_by_line),
            with_f_write.name)
    finally:
        with_f_write.close()

    assert matched_file == {'file': 'sdf'}


def test_search_line_by_line_for_term(with_f_write):
    with_f_write.write('sdf\na\nrghsfz')
    # Rewind to read data back from file.
    with_f_write.seek(0)

    search_term = "a"
    # Directory and recursive option are irrelevant for the test.
    matched_lines = Searcher.search_line_by_line_for_term(
        Searcher(caller_dir="",
                 search_term=search_term,
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=True),
        with_f_write.name)

    assert matched_lines[2] == "a"


def test_search_line_by_line_for_regex(with_f_write):
    with_f_write.write('sdf\na\nrghsfz')
    # Rewind to read data back from file.
    with_f_write.seek(0)

    search_term = "^[d-s]{1,}$"
    # Directory and recursive option are irrelevant for the test.
    matched_lines = Searcher.search_line_by_line_for_regex(
        Searcher(caller_dir="",
                 search_term=search_term,
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=True),
        with_f_write.name)

    assert matched_lines[1] == "sdf"


@pytest.mark.skipif("platform.system() == 'Windows'")
def test_ioerror_due_to_restricted_file_in_search_line_by_line_for_term(with_restricted_file):

    Searcher.search_line_by_line_for_term(Searcher(caller_dir="",
                                                   search_term="",
                                                   is_recursive=False,
                                                   is_abs_path=False,
                                                   is_regex_pattern=False,
                                                   is_search_line_by_line=True),
                                          with_restricted_file)


@pytest.mark.skipif("platform.system() == 'Windows'")
def test_ioerror_due_to_restricted_file_in_search_line_by_line_for_regex(with_restricted_file):

    # Directory option is irrelevant for the test.
    Searcher.search_line_by_line_for_regex(
        Searcher(caller_dir="",
                 search_term="",
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=True),
        with_restricted_file)


def test_regular_expression_error(with_f_read):
    search_term = "[\\]"
    is_regex_pattern = True
    f = with_f_read.name

    # Directory option is irrelevant for the test.
    Searcher.search_f(Searcher(
        caller_dir="",
        search_term=search_term,
        is_recursive=False,
        is_abs_path=False,
        is_regex_pattern=is_regex_pattern,
        is_search_line_by_line=True),
        f)
