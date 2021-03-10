DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS tasks;

CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    email VARCHAR(128) NOT NULL UNIQUE,
    password_hash VACHAR(128) NOT NULL
);

CREATE TABLE tasks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR NOT NULL,
    description VARCHAR,
    creation_date DATETIME NOT NULL,
    due_date DATETIME NOT NULL, 
    id_user INTEGER NOT NULL,
    FOREIGN KEY (id_user) REFERENCES users(id) 
);