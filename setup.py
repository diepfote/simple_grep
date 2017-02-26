from setuptools import setup

setup(
    name='Grep Redone',
    version='0.1',
    packages=['grep_redone'],
    install_requires=['docopt', 'clint'],
    entry_points={
        'console_scripts': [
            'grep_redone=grep_redone.__main__:main'
            ]
    },
)