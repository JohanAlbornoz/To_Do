def users():
    return[
        {'id' : 1, 'email' : 'johan@gmail.com', 'password_hash' : 'password'},
        {'id' : 2, 'email' : 'allan@gmail.com', 'password_hash' : 'password'}]

def tasks():
    return[
        {'id' : 1, 'title' : 'faire le ménage', 'description' : 'je suis user 1', 'creation_date' : '2020-12-01 00:00:00', 'due_date' : '2020-12-07', 'id_user' : 1},
        {'id' : 2, 'title' : 'faire la vaisselle', 'description' : 'je suis user 2', 'creation_date' : '2020-12-01 00:00:00', 'due_date' : '2020-12-07', 'id_user' : 2},
        {'id' : 3, 'title' : 'faire le linge', 'description' : 'je suis user 1', 'creation_date' : '2020-12-01 00:00:00', 'due_date' : '2020-12-07', 'id_user' : 1},
        {'id' : 4, 'title' : 'ranger les toys', 'description' : 'je suis user 1', 'creation_date' : '2020-12-01 00:00:00', 'due_date' : '2020-12-07', 'id_user' : 1},
        {'id' : 5, 'title' : 'faire le dinner', 'description' : 'je suis user 1', 'creation_date' : '2020-12-01 00:00:00', 'due_date' : '2020-12-07', 'id_user' : 1},
        {'id' : 6, 'title' : 'faire le petit dejuné', 'description' : 'je suis user 1', 'creation_date' : '2020-12-01 00:00:00', 'due_date' : '2020-12-07', 'id_user' : 1},
        {'id' : 7, 'title' : 'faire ce que je veux', 'description' : 'je suis user 1', 'creation_date' : '2020-12-01 00:00:00', 'due_date' : '2020-12-07', 'id_user' : 1},
        {'id' : 8, 'title' : 'faire le marché', 'description' : 'je suis user 2', 'creation_date' : '2020-12-01 00:00:00', 'due_date' : '2020-12-07', 'id_user' : 2}]

#urgent=1 second=2