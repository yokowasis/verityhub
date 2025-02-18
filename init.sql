CREATE EXTENSION IF NOT EXISTS vector;

DROP TABLE IF EXISTS posts CASCADE;
DROP TABLE IF EXISTS users_auth CASCADE;

CREATE TABLE users_auth (
    id BIGINT GENERATED ALWAYS AS IDENTITY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    username TEXT UNIQUE NOT NULL,
    password TEXT,
    full_name TEXT,
    avatar TEXT,
    role TEXT,
    PRIMARY KEY (id)
);

ALTER TABLE users_auth
    ADD COLUMN cover TEXT DEFAULT '',
    ADD COLUMN bio TEXT DEFAULT '',
    ADD COLUMN link TEXT DEFAULT '';

CREATE TABLE posts (
    id INTEGER GENERATED ALWAYS AS IDENTITY,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    content TEXT,
    summary TEXT,
    username TEXT NOT NULL,
    type TEXT NOT NULL,
    parent INTEGER,
    content_vec VECTOR,
    content_ts TSVECTOR GENERATED ALWAYS AS (to_tsvector('english', summary)) STORED,
    PRIMARY KEY (id),
    FOREIGN KEY (parent) REFERENCES posts(id) ON DELETE CASCADE,
    FOREIGN KEY (username) REFERENCES users_auth(username) ON DELETE CASCADE
);

CREATE INDEX idx_posts_parent ON posts(parent);
CREATE INDEX idx_posts_type ON posts(type);
CREATE INDEX idx_posts_created_at ON posts(created_at);
CREATE INDEX idx_users_auth_username ON users_auth(username);

ALTER TABLE posts ADD COLUMN title TEXT;