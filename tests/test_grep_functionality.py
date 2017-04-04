import os
import platform
import pytest

from grep.grep import Searcher
from tests.helper_for_tests import *


def test_instantiating_searcher_class():
    caller_dir = os.curdir
    search_term = "docopt"
    specific_file = ''
    is_recursive = False
    is_abs_path = False
    is_regex_pattern = False
    is_search_line_by_line = True
    is_from_stdin = False
    searcher = Searcher(caller_dir,
                        search_term,
                        specific_file,
                        is_recursive,
                        is_abs_path,
                        is_regex_pattern,
                        is_search_line_by_line,
                        is_from_stdin)

    assert searcher.caller_dir == caller_dir
    assert searcher.search_term == search_term
    assert searcher.specific_file == specific_file
    assert searcher.is_recursive == is_recursive
    assert searcher.is_abs_path == is_abs_path
    assert searcher.is_regex_pattern == is_regex_pattern
    assert searcher.is_search_line_by_line == is_search_line_by_line
    assert searcher.is_from_stdin == is_from_stdin


def test_run(with_f_write):
    with_f_write.write('docopt')
    with_f_write.seek(0)

    caller_dir = os.path.dirname(with_f_write.name)
    search_term = "docopt"
    is_abs_path = True

    matched_files = Searcher.run(
        Searcher(caller_dir=caller_dir,
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=is_abs_path,
                 is_regex_pattern=False,
                 is_search_line_by_line=True,
                 is_from_stdin=False
                 ))

    assert matched_files == [os.path.abspath(with_f_write.name)]


def test_search_f(with_f_write):
    with_f_write.write('sdf\na\nrghsf')
    with_f_write.seek(0)

    search_term = "a"
    matched_file = Searcher.search_f(
        Searcher(caller_dir="",
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=True,
                 is_from_stdin=False),
        with_f_write.name)

    assert matched_file[with_f_write.name] == {2: 'a'}


def test_match_f_for_str(with_f_write):
    with_f_write.write('sbiugz8gfzuftzdrdsrts5445tzzftfjguikhoizbtzctzztcuzoh\nsdf\na\n rghsf')
    with_f_write.seek(0)

    search_term = "sdf"
    is_search_line_by_line = False
    matched_file = Searcher.match_f_for_str(
        Searcher(caller_dir="",
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=is_search_line_by_line,
                 is_from_stdin=False),
        with_f_write.name)

    assert matched_file == {'file': 'zuftzdrdsrts5445tzzftfjguikhoizbtzctzztcuzoh\nsdf\na\n rghsf'}


def test_match_f_for_pattern(with_f_write):
    with_f_write.write('sbiugz8gfzuftzdrdsrts5445tzzftfjguikhoizbtzctzztcuzoh\nsdf\na\n rghsf')
    with_f_write.seek(0)

    search_term = "sdf"
    is_search_line_by_line = False
    matched_file = Searcher.match_f_for_pattern(
        Searcher(caller_dir="",
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=is_search_line_by_line,
                 is_from_stdin=False),
        with_f_write.name)

    assert matched_file == {'file': 'zuftzdrdsrts5445tzzftfjguikhoizbtzctzztcuzoh\nsdf\na\n rghsf'}


def test_search_line_by_line_for_term(with_f_write):
    with_f_write.write('sdf\na\nrghsfz')
    with_f_write.seek(0)

    search_term = "a"
    matched_lines = Searcher.search_line_by_line_for_term(
        Searcher(caller_dir="",
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=True,
                 is_from_stdin=False),
        with_f_write.name)

    assert matched_lines[2] == "a"


def test_search_line_by_line_for_regex(with_f_write):
    with_f_write.write('sdf\na\nrghsfz')
    with_f_write.seek(0)

    search_term = "^[d-s]{1,}$"
    matched_lines = Searcher.search_line_by_line_for_regex(
        Searcher(caller_dir="",
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=True,
                 is_from_stdin=False),
        with_f_write.name)

    assert matched_lines[1] == "sdf"


def test_match_f_for_pattern_with_binary_file(with_f_bwrite):
    with_f_bwrite.write(b'\x07\x08\x07')
    with_f_bwrite.seek(0)

    search_term = "\x07"
    matched_file = Searcher.match_f_for_pattern(
        Searcher(caller_dir="",
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=False,
                 is_from_stdin=False),
        with_f_bwrite.name)

    assert matched_file == {'file_matched': ''}


def test_match_f_for_str_with_binary_file(with_f_bwrite):
    with_f_bwrite.write(b'\x07\x08\x07')
    with_f_bwrite.seek(0)

    search_term = "\x07"
    matched_file = Searcher.match_f_for_str(Searcher(caller_dir="",
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=False,
                 is_from_stdin=False),
        with_f_bwrite.name)

    assert matched_file == {'file_matched': ''}


def test_search_line_by_line_for_regex_with_binary_file(with_f_bwrite):
    with_f_bwrite.write(b'\x07\x08\x07')
    with_f_bwrite.seek(0)

    search_term = "\x07"
    matched_file = Searcher.search_line_by_line_for_regex(Searcher(caller_dir="",
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=False,
                 is_from_stdin=False),
        with_f_bwrite.name)

    assert matched_file == {'file_matched': ''}


def test_search_line_by_line_for_term_with_binary_file(with_f_bwrite):
    with_f_bwrite.write(b'\x07\x08\x07')
    with_f_bwrite.seek(0)

    search_term = "\x07"
    matched_file = Searcher.search_line_by_line_for_term(Searcher(caller_dir="",
                 search_term=search_term,
                 specific_file='',
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=True,
                 is_from_stdin=False),
        with_f_bwrite.name)

    assert matched_file == {'file_matched': ''}


def test_match_f_for_str_using_specific_file(with_f_write):
    with_f_write.write('sbiugz8gfzuftzdrdsrts5445tzzftfjguikhoizbtzctzztcuzoh\nsdf\na\n rghsf')
    with_f_write.seek(0)

    search_term = "sdf"
    is_search_line_by_line = False
    matched_files = Searcher.run(
        Searcher(caller_dir="",
                 search_term=search_term,
                 specific_file=with_f_write.name,
                 is_recursive=False,
                 is_abs_path=False,
                 is_regex_pattern=False,
                 is_search_line_by_line=is_search_line_by_line,
                 is_from_stdin=False))

    assert matched_files == [os.path.abspath(with_f_write.name)]
