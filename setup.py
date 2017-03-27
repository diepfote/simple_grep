from setuptools import setup

setup(
    name='Grep Redone',
    version='0.1',
    packages=['grep_redone'],
    install_requires=['docopt', 'clint', 'pytest'],
    entry_points={
        'console_scripts': [
            'grep_redone=grep.__main__:main'
            ]
    },
)
