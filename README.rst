Simple grep
^^^^^^^^^^^

Simple grep is a minimal implementation of grep entirely written in Python.

Most notable alteration from grep: No file or directory specified implies searching in current directory.
Missing features: 
* stdin support for Windows.

Simple grep is tested on:
* CPython 2.7 and 3.6.

(Tests might fail on Windows)


Running it
----------

.. code-block:: bash

    $ python -m grep.__main__ -h


Installation
------------

On any system:

.. code-block:: bash

    $ pip install --user .


On Arch:

.. code-block:: bash

    $ makepkg

    $ sudo pacman -U simple_grep-1.11-1-x86_64.pkg.tar.xz

