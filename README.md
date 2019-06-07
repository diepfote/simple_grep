[![travis-ci.com](https://api.travis-ci.com/florianbegusch/simple_grep.svg)](https://travis-ci.com/florianbegusch/simple_grep)
# Simple grep

Simple grep is a minimal implementation of grep entirely written in Python.

Most notable difference between simple\_grep and grep:  
* If no file or directory is specified simple\_grep starts searching in the current directory.
 
\
Missing features:  
* stdin support for Windows

Simple grep is tested on:  
* CPython 2.7 and 3.4-7  
(Tests might fail on Windows)


## Running it

    $ python -m grep.__main__ -h


### Installation


#### On any system:

    $ pip install --user .


#### On Arch:


    $ makepkg

    $ sudo pacman -U simple_grep-1.11-1-x86_64.pkg.tar.xz

