from __future__ import print_function
from setuptools import setup

setup(
    name="cbtm",
    version="0.1",
    tests_require=['nose'],
    packages=['src'],
    include_package_data=True,
    platforms='any',
    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['SQLAlchemy>=1.1.10',
                      'p4python>=2016.2.1498648',
                      'GitPython>=2.1.3',
                      'lxml>=3.7.3'
                      ],

    # metadata for upload to PyPI
    author="Omkar Joshi",
    author_email="joshio@vmware.com",
    description="Change Based Test Management",
    keywords="Change Based Test Management ",
    test_suite='tests.test_cbtm_test',

    # could also include long_description, download_url, classifiers, etc.
)