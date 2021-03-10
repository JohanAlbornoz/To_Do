from flask_app import data
from flask_app import model


connection = model.connect()
model.create_database(connection)
model.fill_database(connection)
model.tasks(connection)
model.users(connection)
#liste = model.tasks(connection)

