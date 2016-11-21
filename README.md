# Todo.txt I/O

A simple Python module to parse and write [Todo.txt](http://todotxt.com/) files.

[![Latest release](https://img.shields.io/github/release/EpocDotFr/todotxtio.svg)](https://github.com/EpocDotFr/todotxtio/releases) [![License](https://img.shields.io/github/license/EpocDotFr/todotxtio.svg)](https://github.com/EpocDotFr/todotxtio/blob/master/LICENSE.md) 

This module 100% comply to the [Todo.txt specifications](https://github.com/ginatrapani/todo.txt-cli/wiki/The-Todo.txt-Format). There aren't any unit tests, but trust me.

## Prerequisites

Python 3 (tested with Python 3.5, feel free to test on another one and give me feedback).

## Installation

```
pip install todotxtio
```

## Usage

Firstly, import the module:

```
import todotxtio
```

### Parsing

You can parse todos from a file:

```
todos = todotxtio.from_file('todo.txt')
```

Or from a string, why not:

```
todos = todotxtio.from_string(my_string_full_of_todos)
```

Or even from an already opened stream:

```
todos = todotxtio.from_stream(my_stream_full_of_todos) # Will also close the stream
```

They all return a plain-old Python list filled with `Todo` objects (or an empty one if there's no todos).

### `Todo` object

#### Basics

Create a new todo by instantiating a `Todo` object. You can feed todo data via its constructor arguments (none are required):

```
todo = Todo(
    text='Thank Guido for such an awesome programming language',
    priority='A',
    creation_date='2016-11-20'
)

print(todo) # (A) 2016-11-20 Thank Guido for such an awesome programming language +python @awesomeness @ftw
```

Or you also can instantiate an empty (or partially-instantiated) `Todo` object and define its parameters later:

```
todo = Todo(
    creation_date='2016-11-20' # For example only, but constructor can be empty and this can be defined later as well
)

todo.text = 'Thank Guido for such an awesome programming language'
todo.priority = 'A'

print(todo) # (A) 2016-11-20 Thank Guido for such an awesome programming language +python @awesomeness @ftw
```

Once a `Todo` is instantiated, you can use its attributes to modify its data.

```
# todo is a Todo instance

todo.text = 'Hello, I\'m the new text'
todo.priority = 'C'
todo.creation_date = None # Deleting the creation date
```

#### Projects and contexts

They are both plain-old Python lists without leading `+` and `@`:

```
# todo is a Todo instance

# Erase existing projects or contexts
todo.projects = ['python']
todo.contexts = ['awesomeness', 'ftw']

# Append to existings projects or contexts
todo.projects.append('awesome-project')
todo.contexts.append('home')

# Empty the projects list
todo.projects = []
```

#### Todo completion

You can either mark a todo as completed by setting its `completed` attribute to `True`:

```
# todo is a Todo instance

todo.completed = True
```

Or by defining its completion date, which automatically set its `completed` attribute to `True`:

```
# todo is a Todo instance

todo.completion_date = '2016-12-01'
```

This is also applicable to the `Todo` constructor.

### Writing

Write todos to a file:

```
# my_todos is a list of Todo objects

todotxtio.to_file('todo.txt', my_todos)
```

**Caution:** This will overwrite the whole file.

Also, you can write to a string:

```
# my_todos is a list of Todo objects

my_string_full_of_todos = todotxtio.to_string(my_todos)
```

Or even to an already-opened stream:

```
# my_todos is a list of Todo objects
# my_stream is an already-opened stream

todotxtio.to_stream(my_stream, my_todos) # Will also close the stream
```

## Gotchas

  - Projects and contexts will always be appended to the end of each todos when exporting them. This means that if you're parsing such a todo:

```
I'm in love with +python. Python @ftw guys
```

And then if you're writing it to a file (without even modifying it), you'll end with:

```
I'm in love with. Python guys +python @ftw
```

Not ideal, I know.

## Changelog

See [here](https://github.com/EpocDotFr/todotxtio/releases).

## End words

If you have questions or problems, you can [submit an issue](https://github.com/EpocDotFr/todotxtio/issues).

You can also submit pull requests. It's open-source man!