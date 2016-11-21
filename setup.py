from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md')) as f:
    long_description = f.read()

setup(
    name='todotxtio',
    version='0.1.0',
    description='A simple Python module to parse, manipulate and write Todo.txt data',
    long_description=long_description,
    url='https://github.com/EpocDotFr/todotxtio',
    author='Maxime "Epoc" G.',
    author_email='contact@epoc.fr',
    license='DBAD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
        'Programming Language :: Python :: 3'
    ],
    keywords='todotxt todo.txt file parse parser read reader',
    py_modules=['todotxtio']
)