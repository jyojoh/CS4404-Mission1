from flask import Flask, session, render_template, request, redirect
from flask_session import Session
import database as init
import library as db

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

from urllib.parse import parse_qsl

init.initDatabase()

app = Flask(__name__)
app.secret_key = "shoeserverkey"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

private_key = None

with open("privatekey.txt", "rb") as priv_key_file:
    private_key = serialization.load_pem_private_key(
        priv_key_file.read(),
        password=None,
        backend=default_backend()
    )

@app.route("/", methods=["GET", "POST"])
def index():
    qid = 1
    if "vote" not in session:
        session["vote"] = {}

    if request.method == "POST":
        content = request.json

        ciphertext = content["secret"]
        ciphertext = bytes.fromhex(ciphertext)

        plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
            )
        )

        query_str = plaintext.decode("utf-8")
        parsed_query = parse_qsl(query_str)

        username = str(parsed_query[0][1])
        password = str(parsed_query[1][1])

        if not db.checkUser(username, password):
            return render_template("loginfail.html"), 400

        oid = int(parsed_query[2][1])
        oldid = None if qid not in session["vote"] else session["vote"][qid]

        db.save(qid, oid, oldid)
        session["vote"][qid] = oid

    data = db.get(qid)
    data["qid"] = qid

    return render_template("webpage.html", **data)


if __name__ == '__main__':
    app.run("0.0.0.0", 80)
