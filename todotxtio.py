import os
import re

todo_pre_data_regex = re.compile('^((x) )?((\d{4}[-/]\d{2}[-/]\d{2}) )?(\(([A-Z])\) )?((\d{4}[-/]\d{2}[-/]\d{2}) )?')
todo_project_regex = re.compile(' \+(\w+)')
todo_context_regex = re.compile(' @(\w+)')


def from_dicts(todos):
    """Convert a list of todo dicts to a list of Todo objects."""
    return [Todo(**todo) for todo in todos]


def from_stream(stream, close=True):
    """Load a todo list from an already-opened stream.

    :return: A list of Todo objects
    """
    string = stream.read()

    if close:
        stream.close()

    return from_string(string.strip())


def from_file(file_path):
    """Load a todo list from a file.

    :return: A list of Todo objects
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError('File doesn\'t exists: ' + file_path)

    stream = open(file_path, 'r')

    return from_stream(stream)


def from_string(string):
    """Load a todo list from a string.

    :return: A list of Todo objects
    """
    todos = []

    for line in string.splitlines():
        todo_pre_data = todo_pre_data_regex.findall(line)

        todo = Todo()

        if len(todo_pre_data) == 1:
            todo_pre_data = todo_pre_data[0]

            todo.completed = todo_pre_data[1] == 'x'

            if todo_pre_data[3]:
                todo.completion_date = todo_pre_data[3]
            
            todo.priority = todo_pre_data[5]
            todo.creation_date = todo_pre_data[7]

            text = todo_pre_data_regex.sub('', line)
        else:
            text = line

        todo_projects = todo_project_regex.findall(text)

        if len(todo_projects) > 0:
            todo.projects = todo_projects
            text = todo_project_regex.sub('', text)

        todo_contexts = todo_context_regex.findall(text)

        if len(todo_contexts) > 0:
            todo.contexts = todo_contexts
            text = todo_context_regex.sub('', text)

        todo.text = text

        todos.append(todo)

    return todos


def to_dicts(todos):
    """Convert a list of Todo objects to a list of todo dict."""
    return [todo.to_dict() for todo in todos]


def to_stream(stream, todos, close=True):
    """Write a list of todos to an already-opened stream."""
    stream.write(to_string(todos))

    if close:
        stream.close()


def to_file(file_path, todos):
    """Write a list of todos to a file."""
    stream = open(file_path, 'w')
    to_stream(stream, todos)


def to_string(todos):
    """Return a list of todos as a string.

    :return: The todo as a string
    """
    return '\n'.join([str(todo) for todo in todos])


class Todo:
    """Represent one todo.

    :param str text: The text of the todo
    :param bool completed: Should this todo be marked as completed or not (default to False)
    :param str completion_date: A completion date, in the YYYY-MM-DD format. Setting this property will automatically set completed to True (default to None)
    :param str priority: The priority of the todo represented by a char bewteen A-Z (default to None)
    :param str creation_date: A create date, in the YYYY-MM-DD format (default to None)
    :param list projects: A list of projects without + (default to an empty list)
    :param list contexts: A list of projects without @ (default to an empty list)
    """
    text = None
    completed = False
    completion_date = None
    priority = None
    creation_date = None
    projects = []
    contexts = []

    def __init__(self, text=None, completed=False, completion_date=None, priority=None, creation_date=None, projects=None, contexts=None):
        self.text = text
        self.completed = completed

        if completion_date:
            self.completion_date = completion_date

        self.priority = priority
        self.creation_date = creation_date
        self.projects = projects
        self.contexts = contexts

    def to_dict(self):
        """Return a dict representation of this Todo instance."""
        return {
            'text': self.text,
            'completed': self.completed,
            'completion_date': self.completion_date,
            'priority': self.priority,
            'creation_date': self.creation_date,
            'projects': self.projects,
            'contexts': self.contexts
        }

    def __setattr__(self, name, value):
        if name == 'completed':
            if not value:
                super().__setattr__('completion_date', None) # Uncompleted todo must not have any completion date
        elif name == 'completion_date':
            if value:
                super().__setattr__('completed', True) # Setting the completion date must set this todo as completed...
            else:
                super().__setattr__('completed', False) # ...and vice-versa
        elif name in ['projects', 'contexts']:
            if not value:
                super().__setattr__(name, []) # Force contexts and projects to be lists when setting them to a falsely value
                return
            elif type(value) is not list: # Make sure, otherwise, that the provided value is a list
                raise ValueError(name + ' should be a list')

        super().__setattr__(name, value)

    def __str__(self):
        """Convert this Todo object in a valid Todo.txt line."""
        ret = []

        if self.completed:
            ret.append('x')

        if self.completion_date:
            ret.append(self.completion_date)

        if self.priority:
            ret.append('(' + self.priority + ')')

        if self.creation_date:
            ret.append(self.creation_date)

        ret.append(self.text)

        if self.projects:
            ret.append(''.join([' +' + project for project in self.projects]).strip())

        if self.contexts:
            ret.append(''.join([' @' + context for context in self.contexts]).strip())

        return ' '.join(ret)

    def __repr__(self):
        """Call the __str__ method to return a textual representation of this Todo object."""
        return self.__str__()


def search(todos, text=None, completed=None, completion_date=None, priority=None, creation_date=None, projects=None, contexts=None):
    """Return a list of todos that matches the provided filters."""
    results = []

    for todo in todos:
        if text is not None and text in todo.text:
            results.append(todo)
            continue

        if completed is not None and todo.completed == completed:
            results.append(todo)
            continue

        if completion_date is not None and todo.completion_date == completion_date:
            results.append(todo)
            continue

        if priority is not None and todo.priority in priority:
            results.append(todo)
            continue

        if creation_date is not None and todo.creation_date == creation_date:
            results.append(todo)
            continue

        if projects is not None and any(i in projects for i in todo.projects):
            results.append(todo)
            continue

        if contexts is not None and any(i in contexts for i in todo.contexts):
            results.append(todo)
            continue

    return results
