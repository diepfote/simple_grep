import os
import tempfile
from grep_redone.grep.grep import Searcher


def test_search_file_for_string():
    temp = tempfile.NamedTemporaryFile()
    try:
        temp.write('sdf\na\nrghsf')
        # Rewind to read data back from file.
        temp.seek(0)

        # Directory and recursive option are irrelevant for the test.
        dict = Searcher.search_file_for_string(
            Searcher(caller_dir=os.curdir, search_term="a", is_recursive=False),
            temp.name
        )
        assert dict[2] == "a\n"

    finally:
        temp.close()


