CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    hash TEXT NOT NULL
);

CREATE TABLE profiles (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    birthdate DATE NOT NULL,
    blood TEXT NOT NULL,
    allergies TEXT NOT NULL,
    diseases TEXT NOT NULL,
    medications TEXT NOT NULL,
    smoke TEXT NOT NULL,
    alcohol TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE appointments (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    specialty TEXT NOT NULL,
    date DATE,
    time TIME,
    FOREIGN KEY (profile_id) REFERENCES profiles (id)
);

CREATE TABLE vaccination (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    profile_id INTEGER NOT NULL,
    vaccine TEXT NOT NULL,
    dose TEXT NOT NULL,
    date DATE,
    FOREIGN KEY (profile_id) REFERENCES profiles (id)
);