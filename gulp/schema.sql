CREATE TABLE IF NOT EXISTS gulp_user (
    id SERIAL NOT NULL,

    name VARCHAR(32) NOT NULL,
    email VARCHAR(128) NOT NULL,
    password VARCHAR(256) NOT NULL,
    token VARCHAR(256),

    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS library (
    id SERIAL NOT NULL,
    owner INTEGER NOT NULL,

    name VARCHAR(32) NOT NULL,

    PRIMARY KEY (id),
    UNIQUE (owner, name),
    FOREIGN KEY (owner) REFERENCES gulp_user(id)
);

CREATE TABLE IF NOT EXISTS author (
    id SERIAL NOT NULL,
    owner INTEGER NOT NULL,

    first_name VARCHAR(32) DEFAULT '' NOT NULL,
    last_name VARCHAR(32) NOT NULL,

	PRIMARY KEY (id),
	FOREIGN KEY (owner) REFERENCES gulp_user(id),
	UNIQUE (owner, last_name, first_name)
);

CREATE TABLE IF NOT EXISTS saga (
    id SERIAL NOT NULL,
    library INTEGER NOT NULL,

    name VARCHAR(32) NOT NULL,

    PRIMARY KEY (id),
    UNIQUE (library, name),
    FOREIGN KEY (library) REFERENCES library(id)
);

CREATE TABLE IF NOT EXISTS tag (
    id SERIAL NOT NULL,
    library INTEGER NOT NULL,

    name VARCHAR(32) NOT NULL,

    PRIMARY KEY (id),
    UNIQUE (library, name),
    FOREIGN KEY (library) REFERENCES library(id)
);

DO $$ BEGIN
    CREATE TYPE reading_status AS ENUM ('TBR', 'READING', 'READ', 'ABANDONED');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

CREATE TABLE IF NOT EXISTS book (
    id SERIAL NOT NULL,
    library INTEGER NOT NULL,

    isbn CHAR(13),
    title VARCHAR(128) NOT NULL,

    bdate DATE,
    sdate DATE,
    fdate DATE,
    status reading_status DEFAULT 'TBR' NOT NULL,

    saga INTEGER,
    saga_n INTEGER,

    stars INTEGER,
    favorite BOOLEAN,

    PRIMARY KEY (id),
    UNIQUE (library, isbn),
	FOREIGN KEY (library) REFERENCES library (id),
    CHECK ((saga IS NULL) = (saga_n IS NULL)),
    CHECK (stars <= 5 AND stars > 0)
);

CREATE TABLE IF NOT EXISTS book_authors (
    book INTEGER NOT NULL,
    author INTEGER NOT NULL,

	PRIMARY KEY(book, author),
    FOREIGN KEY (book) REFERENCES book(id),
    FOREIGN KEY (author) REFERENCES author(id)
);

CREATE TABLE IF NOT EXISTS book_tags (
    book INTEGER NOT NULL,
    tag INTEGER NOT NULL,

	PRIMARY KEY (book, tag),
    FOREIGN KEY (tag) REFERENCES tag(id),
    FOREIGN KEY (book) REFERENCES book(id)
);
