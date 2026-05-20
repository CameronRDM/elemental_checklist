CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS users (
    firebase_uid VARCHAR(128) PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS sets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    release_date DATE,
    total_cards INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS cards (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    set_id UUID NOT NULL REFERENCES sets(id),
    number VARCHAR(50) NOT NULL,
    name VARCHAR(255) NOT NULL,
    image_url VARCHAR(1024)
);

CREATE TABLE IF NOT EXISTS collection (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    firebase_uid VARCHAR(128) NOT NULL REFERENCES users(firebase_uid),
    card_id UUID NOT NULL REFERENCES cards(id),
    variant VARCHAR(50) NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    acquired_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(firebase_uid, card_id, variant)
);
