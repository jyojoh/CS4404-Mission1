import sqlite3 as sql

def checkUser(username, password):
    conn = sql.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM accounts WHERE username = ? AND password = ?", (username, password,))
    data = cursor.fetchall()

    if len(data) == 0:
        return False

    return True

def get(qid):
    question_dict = {
        "q": "",
        "o": {},
        "v": {}
    }

    conn = sql.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT txt FROM questions WHERE qid=?", (qid,))
    data = cursor.fetchone()
    if data is None:
        return None

    question_dict["q"] = data[0]
    cursor.execute("SELECT oid, txt, votes FROM options WHERE qid=?", (qid,))
    data = cursor.fetchall()
    if len(data) == 0:
        return None
    for index in data:
        question_dict["o"][index[0]] = index[1]
        question_dict["v"][index[0]] = index[2]

    conn.close()
    return question_dict


def save(qid, oid, oldid):
    conn = sql.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT oid, votes FROM options WHERE qid=?", (qid,))

    data = {}
    for index in cursor.fetchall():
        data[index[0]] = index[1]

    if oldid is not None:
        if data[oldid] > 1:
            count = data[oldid] - 1
        else:
            count = 0

        cursor.execute("UPDATE options SET votes=? WHERE qid=? AND oid=?", (count, qid, oldid,))
        data[oldid] -= 1

    count = data[oid] + 1
    cursor.execute("UPDATE options SET votes=? WHERE qid=? AND oid=?", (count, qid, oid,))

    conn.commit()
    conn.close()
    return True
