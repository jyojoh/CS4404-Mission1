CREATE TABLE questions(
    qid INTEGER,
    txt TEXT NOT NULL,
    PRIMARY KEY("qid" AUTOINCREMENT)
);

CREATE TABLE options(
    oid INTEGER, -- option ID
    qid INTEGER NOT NULL, -- question assignment
    txt TEXT NOT NULL, -- candidate name
    votes INTEGER DEFAULT 0, -- number of votes for candidate
    PRIMARY KEY("oid" AUTOINCREMENT),
    FOREIGN KEY ("qid") REFERENCES questions("qid")
);

CREATE TABLE accounts(
    id INTEGER,
    username varchar(10) NOT NULL,
    password varchar(10) NOT NULL
);

CREATE INDEX idx_qid on options(qid);

INSERT INTO questions (txt) VALUES
    ("Which candidate are you voting for?");

INSERT INTO accounts (id, username, password) VALUES
    (1, "1111", "password1"),
    (2, "2222", "password2"),
    (3, "3333", "password3");


INSERT INTO options (qid, txt, votes) VALUES
    (1, "Sole-vester Shoesworth", 0),
    (1, "Croc-odile Sneakingson", 0),
    (1, "Flippity Floppster", 0);