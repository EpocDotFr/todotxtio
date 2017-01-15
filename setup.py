from setuptools import setup
from os import path
import todotxtio

setup(
    name='todotxtio',
    version=todotxtio.__version__,
    description='A simple Python module to parse, manipulate and write Todo.txt data',
    long_description='You can find the documentation `here <https://github.com/EpocDotFr/todotxtio#readme>`_.',
    url='https://github.com/EpocDotFr/todotxtio',
    author='Maxime "Epoc" G.',
    author_email='contact.nospam@epoc.nospam.fr',
    license='DBAD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent'
    ],
    keywords='todotxt todo.txt file parse parser read reader',
    py_modules=['todotxtio'],
    download_url='https://github.com/EpocDotFr/todotxtio/archive/todotxtio-{version}.tar.gz'.format(version=todotxtio.__version__)
)