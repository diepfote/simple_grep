import os
import tempfile

from grep_redone.grep import file_helper

def test_get_all_files():
    temp_dir = tempfile.mkdtemp()
    temp = tempfile.NamedTemporaryFile(dir=temp_dir)

    try:
        files = file_helper.get_all_files(temp_dir, is_recursive=False)
        assert  files == [temp.name]

    finally:
        temp.close()
        os.removedirs(temp_dir)
