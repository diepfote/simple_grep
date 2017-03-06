import os
import platform
import pytest

from grep_redone.grep.grep import Searcher
from grep_redone.tests.test_helper import temp_dir, fd
from grep_redone.tests.test_helper import with_f_write, with_f_read, with_permission_denied


def test_dunder_init():
    caller_dir = os.curdir
    search_term = "docopt"
    is_recursive = False
    is_abs_path = False
    is_regex_pattern = False
    searcher = Searcher(caller_dir, search_term, is_recursive, is_abs_path, is_regex_pattern)

    assert searcher.caller_dir == caller_dir and \
           searcher.search_term == search_term and \
           searcher.is_recursive == is_recursive and \
           searcher.is_abs_path == is_abs_path and \
           searcher.is_regex_pattern == is_regex_pattern


def test_run(with_f_write):
    with_f_write.write('docopt')
    # Rewind to read data back from file.
    with_f_write.seek(0)

    caller_dir = temp_dir
    search_term = "docopt"
    is_abs_path = True

    matched_files = Searcher.run(
        Searcher(caller_dir=caller_dir,
                 search_term=search_term,
                 is_recursive=False,
                 is_abs_path=is_abs_path,
                 is_regex_pattern=False)
    )

    assert matched_files[with_f_write.name] == {1: "docopt"}


def test_search_files(with_f_write):
    with_f_write.flush()
    with_f_write.write('sdf\na\nrghsf')
    # Rewind to read data back from file.
    with_f_write.seek(0)

    search_term = "a"
    files = [with_f_write.name]
    # Directory and recursive option are irrelevant for the test.
    matched_files = Searcher.search_files(
        Searcher(caller_dir="",
                 search_term=search_term,
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False),
        files
    )

    assert matched_files[with_f_write.name] == {2: 'a\n'}


def test_search_line_by_line_for_term(with_f_write):
    with_f_write.flush()
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
                 is_regex_pattern=False),
        with_f_write.name
    )

    assert matched_lines[2] == "a\n"


def test_search_line_by_line_for_regex(with_f_write):
    with_f_write.flush()
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
                 is_regex_pattern=False),
        with_f_write.name)

    assert matched_lines[1] == "sdf\n"


@pytest.mark.skipif("platform.system() == 'Windows'")
def test_ioerror_due_to_restricted_file_in_search_line_by_line_for_term(with_permission_denied):

    Searcher.search_line_by_line_for_term(Searcher(caller_dir="",
                                                   search_term="",
                                                   is_recursive=False,
                                                   is_abs_path=False,
                                                   is_regex_pattern=False),
                                          with_permission_denied)


@pytest.mark.skipif("platform.system() == 'Windows'")
def test_ioerror_due_to_restricted_file_in_search_line_by_line_for_regex(with_permission_denied):

    Searcher.search_line_by_line_for_regex(Searcher(caller_dir="",
                                                    search_term="",
                                                    is_recursive=False,
                                                    is_abs_path=False,
                                                    is_regex_pattern=False),
                                               with_permission_denied)


def test_regular_expression_error(with_f_read):
    search_term = "[\\]"
    is_regex_pattern = True
    files = [with_f_read.name]

    Searcher.search_files(Searcher(
        caller_dir="",
        search_term=search_term,
        is_recursive=False,
        is_abs_path=False,
        is_regex_pattern=is_regex_pattern), files
        )
