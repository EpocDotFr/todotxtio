import todotxtio


def test_one_todo():
    todos = todotxtio.from_string('This is a test')
    assert len(todos) == 1
    assert todos[0].text == 'This is a test'


def test_multiple_todo():
    todos = todotxtio.from_string('This is a test\nThis is only a test\n')
    assert len(todos) == 2


def test_todo_with_contexts():
    todos = todotxtio.from_string('This is a test @test1 @test2')
    assert len(todos) == 1
    assert todos[0].text == 'This is a test'
    assert todos[0].contexts == ['test1', 'test2']


def test_todo_with_projects():
    todos = todotxtio.from_string('This is a test +test1 +test2')
    assert len(todos) == 1
    assert todos[0].text == 'This is a test'
    assert todos[0].projects == ['test1', 'test2']


def test_todo_with_simple_tags():
    todos = todotxtio.from_string('This is a test test1:value1 test2:value2')
    assert len(todos) == 1
    assert todos[0].text == 'This is a test'
    assert 'test1' in todos[0].tags
    assert 'test2' in todos[0].tags
    assert todos[0].tags['test1'] == 'value1'
    assert todos[0].tags['test2'] == 'value2'


def test_todo_with_url_tags():
    todos = todotxtio.from_string('This is a test test1:http://google.com/ test2:value2')
    assert len(todos) == 1
    assert todos[0].text == 'This is a test'
    assert 'test1' in todos[0].tags
    assert 'test2' in todos[0].tags
    assert todos[0].tags['test1'] == 'http://google.com/'
    assert todos[0].tags['test2'] == 'value2'


def test_todo_with_priority():
    todos = todotxtio.from_string('(A) This is a test')
    assert len(todos) == 1
    assert todos[0].text == 'This is a test'
    assert todos[0].priority == 'A'


def test_todo_completed():
    todos = todotxtio.from_string('x This is a test')
    assert len(todos) == 1
    assert todos[0].text == 'This is a test'
    assert todos[0].completed


def test_todo_with_creation_date():
    todos = todotxtio.from_string('2020-01-01 This is a test')
    assert len(todos) == 1
    assert todos[0].text == 'This is a test'
    assert todos[0].creation_date == '2020-01-01'


def test_todo_with_completion_date():
    todos = todotxtio.from_string('x 2020-01-02 2020-01-01 This is a test')
    assert len(todos) == 1
    assert todos[0].text == 'This is a test'
    assert todos[0].completed
    assert todos[0].creation_date == '2020-01-01'
    assert todos[0].completion_date == '2020-01-02'


def test_with_everything():
    todos = todotxtio.from_string('x 2020-01-02 2020-01-01 This is a test +project1 @context1 tag1:value1')
    assert len(todos) == 1
    assert todos[0].text == 'This is a test'
    assert todos[0].projects == ['project1']
    assert todos[0].contexts == ['context1']
    assert 'tag1' in todos[0].tags
    assert todos[0].tags['tag1'] == 'value1'
    assert todos[0].completed
    assert todos[0].creation_date == '2020-01-01'
    assert todos[0].completion_date == '2020-01-02'


def test_invalid_priority():
    todos = todotxtio.from_string('(z) This is a test')
    assert len(todos) == 1
    assert todos[0].priority is None
    assert todos[0].text == '(z) This is a test'
