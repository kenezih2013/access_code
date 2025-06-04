DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    resident_address TEXT NOT NULL,
    email TEXT NOT NULL,
    validity_date TIMESTAMP NOT NULL,
    u_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    guest_name TEXT NOT NULL,
    host_address TEXT NOT NULL,
    access_code INTEGER NOT NULL,
    expired TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);


DROP TABLE IF EXISTS user_login;

CREATE TABLE user_login (
    login_id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name UNIQUE NOT NULL,
    user_psswrd NOT NULL,
    l_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

DROP TABLE IF EXISTS admin_users;

CREATE TABLE admin_users (
    admin_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    a_address TEXT NOT NULL,
    email TEXT NOT NULL,
    a_profile TEXT NOT NULL,
    validity_date TIMESTAMP NOT NULL,
    a_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS a_login;

CREATE TABLE a_login (
    a_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username UNIQUE NOT NULL,
    admin_psswrd NOT NULL,
    al_created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    admin_id INTEGER,
    FOREIGN KEY (admin_id) REFERENCES admin_users(admin_id)
);