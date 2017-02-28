import os
import tempfile
import pytest

from grep_redone.grep.grep import Searcher

def setup_module(module):
    global temp_dir, fd, temp_path
    temp_dir = tempfile.mkdtemp()
    fd, temp_path = tempfile.mkstemp(dir=temp_dir)

def teardown_module(module):
    os.close(fd)
    os.remove(temp_path)
    os.removedirs(temp_dir)

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
    with open(temp_path, 'wr') as f:
            f.write('docopt')
            # Rewind to read data back from file.
            f.seek(0)

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

            assert matched_files[temp_path] == {1: "docopt"}



def test_search_files():
    with open(temp_path, 'wr') as f:
        f.flush()
        f.write('sdf\na\nrghsf')
        # Rewind to read data back from file.
        f.seek(0)

        search_term = "a"
        files = [temp_path]
        # Directory and recursive option are irrelevant for the test.
        matched_files = Searcher.search_files(
            Searcher(caller_dir="",
                     search_term=search_term,
                     is_recursive=False,
                     is_abs_path=False,
                     is_regex_pattern=False),
            files
        )

        assert matched_files[temp_path] == {2: 'a\n'}

def test_search_file_for_string():
    with open(temp_path, 'wr') as f:
        f.flush()
        f.write('sdf\na\nrghsfz')
        # Rewind to read data back from file.
        f.seek(0)

        search_term = "a"
        # Directory and recursive option are irrelevant for the test.
        matched_lines = Searcher.search_file_for_string(
            Searcher(caller_dir="",
                     search_term=search_term,
                     is_recursive=False,
                     is_abs_path=False,
                     is_regex_pattern=False),
            temp_path
        )

        assert matched_lines[2] == "a\n"

def test_search_file_for_regex():
    with open(temp_path, 'wr') as f:
        f.flush()
        f.write('sdf\na\nrghsfz')
        # Rewind to read data back from file.
        f.seek(0)

        search_term = "^[d-s]{1,}$"
        # Directory and recursive option are irrelevant for the test.
        matched_lines = Searcher.search_file_for_regex(
            Searcher(caller_dir="",
                     search_term=search_term,
                     is_recursive=False,
                     is_abs_path=False,
                     is_regex_pattern=False),
            temp_path
        )

        assert matched_lines[1] == "sdf\n"

def test_ioerror_due_to_restricted_file_in_search_file_for_string():
        try:
            # Change permissions to rw root only
            os.chmod(temp_path, 600)

            Searcher.search_file_for_string(
                Searcher(caller_dir="",
                         search_term="",
                         is_recursive=False,
                         is_abs_path=False,
                         is_regex_pattern=False),
                temp_path
            )

        except IOError, ioerror:
            pytest.fail("An IOError was raised:\n\t" + ioerror.__str__())

        finally:
            os.chmod(temp_path, 777)


def test_ioerror_due_to_restricted_file_in_search_file_for_regex():
        try:
            # Change permissions to rw root only
            os.chmod(temp_path, 600)

            Searcher.search_file_for_regex(
                Searcher(caller_dir="",
                         search_term="",
                         is_recursive=False,
                         is_abs_path=False,
                         is_regex_pattern=False),
                temp_path
            )

        except IOError, ioerror:
            pytest.fail("An IOError was raised:\n\t" + ioerror.__str__())

        finally:
            os.chmod(temp_path, 777)

def test_regular_expression_error():
    with open(temp_path, 'r') as f:

        search_term = "[\\]"
        is_regex_pattern = True
        files = [temp_path]

        Searcher.search_files(
            Searcher(caller_dir="",
                search_term=search_term,
                is_recursive=False,
                is_abs_path=False,
                is_regex_pattern=is_regex_pattern),
            files
        )