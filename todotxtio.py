import os
import re

todo_pre_data_regex = re.compile('^((x) )?((\d{4}[-/]\d{2}[-/]\d{2}) )?(\(([A-Z])\) )?((\d{4}[-/]\d{2}[-/]\d{2}) )?')
todo_project_regex = re.compile(' \+(\w+)')
todo_context_regex = re.compile(' @(\w+)')


def from_stream(stream):
    string = stream.read()

    stream.close()

    return from_string(string)


def from_file(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    stream = open(file_path, 'r')

    return from_stream(stream)


def from_string(string):
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
    stream.write(to_string(todos))
    stream.close()


def to_file(file_path, todos):
    stream = open(file_path, 'w')
    to_stream(stream, todos)


def to_string(todos):
    return '\n'.join([str(todo) for todo in todos])


class Todo:
    text = '(No content)'
    completed = False
    completion_date = None
    priority = None
    creation_date = None
    projects = []
    contexts = []

    def __init__(self, text='(No content)', completed=False, completion_date=None, priority=None, creation_date=None, projects=None, contexts=None):
        self.text = text

        if completion_date:
            self.completed = True
            self.completion_date = completion_date
        else:
            self.completed = completed

        self.priority = priority
        self.creation_date = creation_date

        if projects:
            self.projects = projects

        if contexts:
            self.contexts = contexts

    def __str__(self):
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
        return self.__str__()
