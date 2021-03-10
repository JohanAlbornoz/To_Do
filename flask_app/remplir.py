


#ajouter task
from flask_app import model 
from flask_app import data
connection = model.connect()
model.insert_task(connection, {'id' : None, 'title' : 'faire le ménage', 'description' : 'je suis user 1', 'creation_date' : '2020-12-01 00:00:00', 'due_date' : '2020-12-07 00:00:00', 'id_user' : 3})
model.add_user(connection, 'test@gmail.com', 'test')



#-------------------------------------------notes johan-------------------------------------------
#  connection = model.connect()
# list_task = model.tasks(connection)
#control shit r = refrescar pagina
#pythoon3 index.html