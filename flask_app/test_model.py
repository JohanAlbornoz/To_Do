from flask_app import model
from flask_app import data
import pytest

def test_tasks_and_insert_task():
  connection = model.connect(":memory:")
  model.create_database(connection)
  tasks = data.tasks()
  users = data.users()
  model.insert_user(connection, users[0])
  model.insert_user(connection, users[1])
  model.insert_task(connection, tasks[6])
  model.insert_task(connection, tasks[1])
  model.insert_task(connection, tasks[5])
  assert model.tasks(connection) == [tasks[1], tasks[5], tasks[6]]

def test_users_and_insert_user():
  connection = model.connect(":memory:")
  model.create_database(connection)
  users = data.users()
  model.insert_user(connection, users[1])
  model.insert_user(connection, users[0])
  assert model.users(connection) == [users[0], users[1]]

def test_fill_database():
  connection = model.connect(":memory:")
  model.create_database(connection)
  model.fill_database(connection)
  assert model.users(connection) == data.users()
  assert model.tasks(connection) == data.tasks()

def test_user():
  connection = model.connect(":memory:")
  model.create_database(connection)
  model.fill_database(connection)
  for user in data.users():
    assert model.user(connection, user['id']) == user


def test_user_exception():
    connection = model.connect(":memory:")
    model.create_database(connection)
    model.fill_database(connection)
    with pytest.raises(Exception) as exception_info:
        model.user(connection, 1000)
    assert str(exception_info.value) == 'Équipe inconnue'

def test_task():
  connection = model.connect(":memory:")
  model.create_database(connection)
  model.fill_database(connection)
  for task in data.tasks():
    assert model.task(connection, task['id']) == task


def test_task_exception():
    connection = model.connect(":memory:")
    model.create_database(connection)
    model.fill_database(connection)
    with pytest.raises(Exception) as exception_info:
        model.task(connection, 1000)
    assert str(exception_info.value) == 'Task inconnu'


def test_add_and_get_user():
    connection = model.connect(":memory:")
    model.create_database(connection)
    model.add_user(connection, 'test1@example.com', 'secret1')
    model.add_user(connection, 'test2@example.com', 'secret2')
    user1 = model.get_user(connection, 'test1@example.com', 'secret1')
    user2 = model.get_user(connection, 'test2@example.com', 'secret2')
    assert user1 == {'id' : 1, 'email' : 'test1@example.com'}
    assert user2 == {'id' : 2, 'email' : 'test2@example.com'}


def test_get_user_exception():
    connection = model.connect(":memory:")
    model.create_database(connection)
    model.add_user(connection, 'test@example.com', 'secret')
    with pytest.raises(Exception) as exception_info:
        model.get_user(connection, 'test1@example.com', 'secret')
    assert str(exception_info.value) == 'Utilisateur inconnu'
    with pytest.raises(Exception) as exception_info:
        model.get_user(connection, 'test@example.com', 'secret1')
    assert str(exception_info.value) == 'Utilisateur inconnu'
    with pytest.raises(Exception) as exception_info:
        model.get_user(connection, 'test1@example.com', 'secret1')
    assert str(exception_info.value) == 'Utilisateur inconnu'


def test_add_user_email_unique():
    connection = model.connect(":memory:")
    model.create_database(connection)
    model.create_database(connection)
    model.add_user(connection, 'test1@example.com', 'secret1')
    with pytest.raises(Exception) as exception_info:
        model.add_user(connection, 'test1@example.com', 'secret2')
    assert str(exception_info.value) == 'UNIQUE constraint failed: users.email'


def test_change_password():
    connection = model.connect(":memory:")
    model.create_database(connection)
    model.add_user(connection, 'test@example.com', 'secret1')
    model.change_password(connection, 'test@example.com', 'secret1', 'secret2')
    user = model.get_user(connection, 'test@example.com', 'secret2')
    assert user == {'id' : 1, 'email' : 'test@example.com'}
    with pytest.raises(Exception) as exception_info:
        model.get_user(connection, 'test@example.com', 'secret1')
    assert str(exception_info.value) == 'Utilisateur inconnu'


def test_change_password_old_password_check():
    connection = model.connect(":memory:")
    model.create_database(connection)
    model.add_user(connection, 'test@example.com', 'secret1')
    with pytest.raises(Exception) as exception_info:
        model.change_password(connection, 'test@example.com', 'secret2', 'secret1')
    assert str(exception_info.value) == 'Utilisateur inconnu'

def test_delete_task():
    connection = model.connect(":memory:")
    model.create_database(connection)
    model.create_database(connection)
    model.fill_database(connection)
    model.delete_task(connection, 1)
    model.delete_task(connection, 4)
    model.delete_task(connection, 100)
    assert model.task(connection, 2) == {'id' : 2, 'title' : 'faire la vaisselle', 'description' : 'je suis user 2', 'creation_date' : '2020-12-01 00:00:00', 'due_date' : '2020-12-07', 'id_user' : 2}