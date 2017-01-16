Todo.txt I/O documentation
==========================

Welcome! This documentation is about Todo.txt I/O, a simple Python module to parse, manipulate and write `Todo.txt <http://todotxt.com/>`_ data.

|pyversion| |pypiv| |pypil|

This module tries to comply to the `Todo.txt specifications <https://github.com/ginatrapani/todo.txt-cli/wiki/The-Todo.txt-Format>`_ (disclaimer: there aren't any unit tests).

Prerequisites
-------------

Should work on any Python 3.x version. Feel free to test with another Python version and give me feedback.

Installation
------------

The usual way:

.. code-block:: console

    $ pip install todotxtio

The McGyver way, after cloning/downloading this repo:

.. code-block:: console

    $ python setup.py install

Usage
-----

Import the :mod:`todotxtio` module and you are ready to use any of its functions.

Parsing
*******

The functions below all return a plain-old Python list filled with :class:`todotxtio.Todo` objects (or an empty one if there's no todos).

.. code-block:: python

    import todotxtio

    list_of_todos = todotxtio.from_file('todo.txt')
    # Or: list_of_todos = todotxtio.from_string(string_full_of_todos)
    # Or: list_of_todos = todotxtio.from_stream(stream_full_of_todos)
    # Or: list_of_todos = todotxtio.from_dicts(list_of_todos_dict)

Manipulating todos
******************

#### Basics

Create a new todo by instantiating a `Todo` object. You can feed todo data via its constructor arguments (none are required):

```python
todo = todotxtio.Todo(
    text='Thank Guido for such an awesome programming language',
    priority='A',
    creation_date='2016-11-20'
)

print(todo) # (A) 2016-11-20 Thank Guido for such an awesome programming language
```

Or you also can instantiate an empty (or partially-instantiated) `Todo` object and define its parameters later:

```python
todo = todotxtio.Todo(
    creation_date='2016-11-20' # For example only, but constructor can be empty and this can be defined later as well
)

todo.text = 'Thank Guido for such an awesome programming language'
todo.priority = 'A'

print(todo) # (A) 2016-11-20 Thank Guido for such an awesome programming language
```

Once a `Todo` is instantiated, you can use its attributes to modify its data.

```python
# todo is a Todo instance

todo.text = 'Hello, I\'m the new text'
todo.priority = 'C'
todo.creation_date = None # Deleting the creation date
```

Playing with todo lists is easy, the same way when manipulating any Python lists:

```python
todos = []

todos.append(todotxtio.Todo(text='A todo in its simplest form!'))

# Updating the completion of the first todo in the todo list (plain Python syntax)
todos[0].completed = True

# Adding a new todo
todos.append(todotxtio.Todo(text='A second todo in its simplest form!'))

# Remove a todo
del todos[0]
```

#### Todo dicts

You can export a `Todo` to a Python dict. Keys and values are exactly the same as the `Todo` constructor:

```python
# todo is a Todo instance

todo_dict = todo.to_dict()
```

And vice-versa, you can instantiate a `Todo` object from a dict using the standard Python way:

```python
todo_dict = {
    'text': 'Hey ho!',
    'completed': True,
    'priority': 'D',
    'projects': ['blah']
}

todo = todotxtio.Todo(**todo_dict)
```

#### Projects and contexts

They are both plain-old Python lists without leadings `+` and `@`:

```python
todo = todotxtio.Todo(
    text='Thank Guido for such an awesome programming language',
    priority='A',
    creation_date='2016-11-20'
)

# Define some projects and contexts
todo.projects = ['python']
todo.contexts = ['awesomeness', 'ftw']

# Append to existings projects or contexts
todo.projects.append('awesome-project')
todo.contexts.append('cool')

# Remove a context
todo.contexts.remove('cool')

# Empty the projects list
todo.projects = [] # Or None

print(todo) # (A) 2016-11-20 Thank Guido for such an awesome programming language @awesomeness @ftw
```

#### Todo completion

You can either mark a todo as completed by setting its `completed` attribute to `True`:

```python
todo = todotxtio.Todo(
    text='Thank Guido for such an awesome programming language',
    priority='A',
    creation_date='2016-11-20'
)

todo.completed = True

print(todo) # x (A) 2016-11-20 Thank Guido for such an awesome programming language
```

Or by defining its completion date, which automatically set its `completed` attribute to `True`:

```python
todo = todotxtio.Todo(
    text='Thank Guido for such an awesome programming language',
    priority='A',
    creation_date='2016-11-20'
)

todo.completion_date = '2016-12-01'

print(todo) # x 2016-12-01 (A) 2016-11-20 Thank Guido for such an awesome programming language
```

This is also applicable to the `Todo` constructor.

Of course, inverse is also applicable (setting `completed` to `False` removes the completion date).

#### Tags

Tags, also called add-ons metadata, are represented by a simple one-dimension dictionary. They allow you to easily
define and retrieve custom formatted data:

```python
todo = todotxtio.Todo(
    text='Thank Guido for such an awesome programming language'
)

todo.tags = { # Define some tags
    'key': 'value',
    'second': 'tag'
}

todo.tags['due'] = '2016-12-01'

# Remove a tag
del todo.tags['second']

print(todo) # Thank Guido for such an awesome programming language key:value due:2016-12-01

# Empty tags
todo.tags = {} # Or None
```

### Writing

At some point you'll need to save your todo list.

**Writing to a file:**

```python
# todos is a list of Todo objects

todotxtio.to_file('todo.txt', todos, encoding='utf-8') # utf-8 is the default
```

**Caution:** This will overwrite the whole file. Also, data will be UTF-8 encoded.

**Export all todos to string:**

```python
# todos is a list of Todo objects

string_full_of_todos = todotxtio.to_string(todos)
```

**Writing to an already-opened stream:**

```python
# todos is a list of Todo objects
# stream is an already-opened stream

todotxtio.to_stream(stream, todos, close=False) # Will not close the stream
```

**Convert to a list of todo dicts (e.g to serialize them to JSON):**

```python
# todos is a list of Todo objects

todo_dicts = todotxtio.to_dicts(todos)
```

Searching a todo list
*********************

You can search in a given todo list using the handy :func:`todotxtio.search` with its filter criteria. It takes the
exact same parameters as the Todo object constructor, and return a list of :class:`todotxtio.Todo` objects as well. All criteria
defaults to `None` which means that the criteria is ignored.

.. code-block:: python

    results = todotxtio.search(list_of_todos,
        priority=['A', 'C'], # priority, contexts and projects criteria are always lists (or None as said above)
        contexts=['home'],
        projects=['python', 'todo'], # If giving a list to search for, only one match is required to return a todo in the results list
        completed=True,
        completion_date='2016-11-20',
        creation_date='2016-11-15',
        tags={'due': '2016-12-01'}, # Tags are a dict, as usual (only one match, both key and value, is required to return a todo in the results list)
        text='todo content' # Will try to find this string in the todo text content
    )

A todo will be returned in the results list if all of the criteria matches. From the moment when a todo is sent in
the results list, it will never be checked again.

Writing
*******

Quite simple.

.. code-block:: python

    # list_of_todos is a list of Todo objects

    todotxtio.to_file('todo.txt', list_of_todos)
    # Or: string_full_of_todos = todotxtio.to_string(list_of_todos)
    # Or: todotxtio.to_stream(stream, list_of_todos)
    # Or: list_of_todos_dict = todotxtio.to_dicts(list_of_todos)

Gotchas
-------

  - Projects, contexts and tags will always be appended to the end of each todos when exporting them. This means that if you're parsing such a todo:

.. code-block::

    I'm in love with +python. due:2016-12-01 Python @ftw guys

And then if you're writing it to a file (without even modifying it), you'll end with:

.. code-block::

    I'm in love with. Python guys +python @ftw due:2016-12-01

Not ideal, I know (at least for projects and contexts).

  - This is my very first PyPI package.

API docs
--------

.. automodule:: todotxtio
   :members:
   :undoc-members:

.. |pyversion| image:: https://img.shields.io/pypi/pyversions/todotxtio.svg?link=https://pypi.python.org/pypi/todotxtio
.. |pypiv| image:: https://img.shields.io/pypi/v/todotxtio.svg?link=https://pypi.python.org/pypi/todotxtio
.. |pypil| image:: https://img.shields.io/pypi/l/todotxtio.svg?link=https://github.com/EpocDotFr/todotxtio/blob/master/LICENSE.md