import os
import tempfile
import pytest

from grep_redone.grep.grep import Searcher

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

def test_run():
    temp_dir = tempfile.mkdtemp()
    temp = tempfile.NamedTemporaryFile(dir=temp_dir)

    try:
        temp.write('docopt')
        # Rewind to read data back from file.
        temp.seek(0)

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

        assert matched_files[temp.name] == {1: "docopt"}

    finally:
        temp.close()
        os.removedirs(temp_dir)


def test_search_files():
    temp = tempfile.NamedTemporaryFile()
    try:
        temp.write('sdf\na\nrghsf')
        # Rewind to read data back from file.
        temp.seek(0)

        search_term = "a"
        files = [temp.name]
        # Directory and recursive option are irrelevant for the test.
        matched_files = Searcher.search_files(
            Searcher(caller_dir="",
                     search_term=search_term,
                     is_recursive=False,
                     is_abs_path=False,
                     is_regex_pattern=False),
            files
        )

        assert matched_files[temp.name] == {2: 'a\n'}

    finally:
        temp.close()

def test_search_file_for_string():
    temp = tempfile.NamedTemporaryFile()
    try:
        temp.write('sdf\na\nrghsfz')
        # Rewind to read data back from file.
        temp.seek(0)

        search_term = "a"
        f = temp.name
        # Directory and recursive option are irrelevant for the test.
        matched_lines = Searcher.search_file_for_string(
            Searcher(caller_dir="",
                     search_term=search_term,
                     is_recursive=False,
                     is_abs_path=False,
                     is_regex_pattern=False),
            f
        )

        assert matched_lines[2] == "a\n"

    finally:
        temp.close()

def test_search_file_for_regex():
    temp = tempfile.NamedTemporaryFile()
    try:
        temp.write('sdf\na\nrghsfz')
        # Rewind to read data back from file.
        temp.seek(0)

        search_term = "^[d-s]{1,}$"
        f = temp.name
        # Directory and recursive option are irrelevant for the test.
        matched_lines = Searcher.search_file_for_regex(
            Searcher(caller_dir="",
                     search_term=search_term,
                     is_recursive=False,
                     is_abs_path=False,
                     is_regex_pattern=False),
            f
        )

        assert matched_lines[1] == "sdf\n"

    finally:
        temp.close()

def test_ioerror_due_to_restricted_file_in_search_file_for_string():
    temp_dir = tempfile.mkdtemp()
    temp = tempfile.NamedTemporaryFile(dir=temp_dir)

    try:
        # Change permissions to rw root only
        os.chmod(temp.name, 600)

        f = temp.name
        Searcher.search_file_for_string(
            Searcher(caller_dir="",
                     search_term="",
                     is_recursive=False,
                     is_abs_path=False,
                     is_regex_pattern=False),
            f
        )

    except IOError, ioerror:
        pytest.fail("An IOError was raised:\n\t" + ioerror.__str__())

    finally:
        temp.close()
        os.removedirs(temp_dir)


def test_ioerror_due_to_restricted_file_in_search_file_for_regex():
    temp_dir = tempfile.mkdtemp()
    temp = tempfile.NamedTemporaryFile(dir=temp_dir)

    try:
        # Change permissions to rw root only
        os.chmod(temp.name, 600)

        f = temp.name
        Searcher.search_file_for_regex(
            Searcher(caller_dir="",
                     search_term="",
                     is_recursive=False,
                     is_abs_path=False,
                     is_regex_pattern=False),
            f
        )

    except IOError, ioerror:
        pytest.fail("An IOError was raised:\n\t" + ioerror.__str__())

    finally:
        temp.close()
        os.removedirs(temp_dir)