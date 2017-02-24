import os
import tempfile
from grep_redone.grep.grep import Searcher


def test_search_files():
    pass

def test_search_file_for_string():
    searcher = Searcher(os.curdir, "a")

    temp = tempfile.NamedTemporaryFile()
    try:
        temp.write('sdf\na\nrghsf')
        # Rewind to read data back from file.
        temp.seek(0)

        dict = searcher.search_file_for_string(temp.name)
        assert(dict[2], ["a"])

    finally:
        temp.close()