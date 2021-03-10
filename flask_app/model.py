import sqlite3
import os
from flask_app import data
from werkzeug.security import generate_password_hash, check_password_hash


################################### base de données ############################## 

def dictionary_factory(cursor, row):
  dictionary = {}
  for index in range(len(cursor.description)):
    column_name = cursor.description[index][0]
    dictionary[column_name] = row[index]
  return dictionary

def connect(database = "database.sqlite"):
  connection = sqlite3.connect(database)
  connection.execute("PRAGMA foreign_keys = 1")
  connection.row_factory = dictionary_factory
  return connection

def read_build_script():
  path = os.path.join(os.path.dirname(__file__), 'build.sql')
  file = open(path)
  script = file.read()
  file.close()
  return script

def create_database(connection):
  script = read_build_script()
  connection.executescript(script)
  connection.commit()


####################################### fonctionalités ##############################


def insert_task(connection, task):
  sql = 'INSERT INTO tasks(id, title, description, creation_date, due_date, id_user) VALUES (:id, :title, :description, :creation_date, :due_date, :id_user);'
  connection.execute(sql, task)
  connection.commit()

def users(connection):
  sql = 'SELECT * FROM users ORDER BY id;'
  cursor = connection.execute(sql)
  rows = cursor.fetchall()
  return rows

def tasks(connection):
  sql = 'SELECT * FROM tasks ORDER BY id;'
  cursor = connection.execute(sql)
  rows = cursor.fetchall()
  return rows

def fill_database(connection):
  users = data.users()
  for user in users:
    insert_user(connection, user)
  tasks = data.tasks()
  for task in tasks:
    insert_task(connection, task)

def user(connection, user_id):
  sql = 'SELECT * FROM users WHERE id = :id;'
  cursor = connection.execute(sql, { 'id' : user_id })
  row = cursor .fetchone()
  if row == None:
    raise Exception('Équipe inconnue')
  return row

def task(connection, task_id):
  sql = 'SELECT * FROM tasks WHERE id = :id;'
  cursor = connection.execute(sql, { 'id' : task_id })
  row = cursor .fetchone()
  if row == None:
    raise Exception('Task inconnu')
  return row

def tasks_user(connection, task_id_user):
  sql = 'SELECT * FROM tasks WHERE id_user = :id_user; '
  cursor = connection.execute(sql, { 'id_user' : task_id_user })
  rows = cursor.fetchall()
  return rows

def limitated_tasks_user(connection, task_id_user):
  sql = 'SELECT * FROM tasks WHERE id_user = :id_user  LIMIT 3; '
  cursor = connection.execute(sql, { 'id_user' : task_id_user })
  rows = cursor.fetchall()
  return rows

def delete_task(connection, task_id):
  sql = """DELETE FROM tasks WHERE id = :id"""
  connection.execute(sql, {'id' : task_id})
  connection.commit()


####################################### Authentification ##############################

def insert_user(connection, user):
  sql = 'INSERT INTO users(id, email, password_hash ) VALUES (:id, :email, :password_hash);'
  connection.execute(sql, user)
  connection.commit()

def add_user(connection, email, password):
  password_hash = generate_password_hash(password)
  sql = """INSERT INTO users(email, password_hash) VALUES (:email, :password_hash)"""
  connection.execute(sql, { 'email' : email, 'password_hash' : password_hash})
  connection.commit()


def get_user(connection, email, password):
  sql = "SELECT * FROM users WHERE email = :email"
  rows = connection.execute(sql, { 'email' : email }).fetchall()
  if len(rows) == 0:
    raise Exception('Utilisateur inconnu')
  row = rows[0]
  password_hash = row['password_hash']
  if not check_password_hash(password_hash, password):
    raise Exception('Utilisateur inconnu')
  return {'id' : row['id'], 'email' : row['email']}


def change_password(connection, email, old_password, new_password):
  user = get_user(connection, email, old_password)
  sql = """UPDATE users SET password_hash = :password_hash
           WHERE id = :id"""
  id = user['id']
  password_hash = generate_password_hash(new_password)
  connection.execute(sql, {'id' : id, 'password_hash' : password_hash})
  connection.commit()