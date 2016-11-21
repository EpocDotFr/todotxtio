import os
import re

todo_pre_data_regex = re.compile('^((x) )?((\d{4}[-/]\d{2}[-/]\d{2}) )?(\(([A-Z])\) )?((\d{4}[-/]\d{2}[-/]\d{2}) )?')
todo_project_regex = re.compile(' \+(\w+)')
todo_context_regex = re.compile(' @(\w+)')


def from_stream(stream):
    """Load a todo list from an already opened stream."""
    string = stream.read()

    stream.close()

    return from_string(string)


def from_file(file_path):
    """Load a todo list from a file."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    stream = open(file_path, 'r')

    return from_stream(stream)


def from_string(string):
    """Load a todo list from a string."""
    todos = []

    for line in string.splitlines():
        todo_pre_data = todo_pre_data_regex.findall(line)

        todo = Todo()

        if len(todo_pre_data) == 1:
            todo_pre_data = todo_pre_data[0]

            todo.completed = todo_pre_data[1] == 'x'
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


def to_stream(stream, todos):
    """Write a list of todos to an already opened stream."""
    stream.write(to_string(todos))
    stream.close()


def to_file(file_path, todos):
    """Write a list of todos to a file."""
    stream = open(file_path, 'w')
    to_stream(stream, todos)


def to_string(todos):
    """Return a list of todos as a string."""
    return '\n'.join([str(todo) for todo in todos])


class Todo:
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
        self.completion_date = completion_date
        self.priority = priority
        self.creation_date = creation_date
        self.projects = projects
        self.contexts = contexts

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

        super().__setattr__(name, value)

    def __str__(self):
        """Convert this Todo object in a valid Todo.txt todo line."""
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
