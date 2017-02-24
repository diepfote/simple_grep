import os
import tempfile
from grep_redone.grep.grep import Searcher

def test_dunder_init():
    caller_dir = os.curdir
    search_term = "docopt"
    is_recursive = False
    searcher = Searcher(caller_dir, search_term, is_recursive)

    assert searcher.caller_dir == caller_dir and \
           searcher.search_term == search_term and \
           searcher.is_recursive == is_recursive

def test_run():
    matched_files = Searcher.run(
        Searcher(caller_dir=os.curdir, search_term="docopt", is_recursive=False)
    )

    print matched_files

    assert matched_files['./setup.py'] == {6: "    packages=['grep_redone', 'docopt'],\n"}

def test_search_files():
    temp = tempfile.NamedTemporaryFile()
    try:
        temp.write('sdf\na\nrghsf')
        # Rewind to read data back from file.
        temp.seek(0)

        # Directory and recursive option are irrelevant for the test.
        matched_files = Searcher.search_files(
            Searcher(caller_dir=os.curdir, search_term="a", is_recursive=False),
            [temp.name]
        )

        assert matched_files[temp.name] == {2: 'a\n'}

    finally:
        temp.close()

def test_search_file_for_string():
    temp = tempfile.NamedTemporaryFile()
    try:
        temp.write('sdf\na\nrghsf')
        # Rewind to read data back from file.
        temp.seek(0)

        # Directory and recursive option are irrelevant for the test.
        matched_lines = Searcher.search_file_for_string(
            Searcher(caller_dir=os.curdir, search_term="a", is_recursive=False),
            temp.name
        )

        assert matched_lines[2] == "a\n"

    finally:
        temp.close()


# test_run()