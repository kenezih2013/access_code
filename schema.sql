DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    guest_name TEXT NOT NULL,
    host_address TEXT NOT NULL,
    access_code INTEGER NOT NULL,
    expired TIMESTAMP
);

DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    resident_address TEXT NOT NULL,
    email TEXT NOT NULL,
    validity_date TIMESTAMP NOT NULL,
    u_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS user_login;

CREATE TABLE user_login (
    login_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name UNIQUE NOT NULL,
    user_psswrd NOT NULL,
    l_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
