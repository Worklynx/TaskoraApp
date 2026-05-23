CREATE DATABASE taskora_db;

\c taskora_db;

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    phone VARCHAR(20) UNIQUE,
    password VARCHAR(100),
    role VARCHAR(20),
    rank VARCHAR(20) DEFAULT 'Bronze',
    points INTEGER DEFAULT 0
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    location VARCHAR(255),
    reward INTEGER,
    status VARCHAR(20) DEFAULT 'Open',
    creator_phone VARCHAR(20),
    assigned_worker VARCHAR(20)
);

CREATE TABLE applications (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id),
    worker_phone VARCHAR(20),
    status VARCHAR(20) DEFAULT 'Pending'
);