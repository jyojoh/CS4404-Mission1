from flask import Flask, session, render_template, request, redirect
from flask_session import Session
import database as init
import library as db

init.initDatabase()

app = Flask(__name__)
app.secret_key = "shoeserverkey"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    qid = 1
    if "vote" not in session:
        session["vote"] = {}

    if request.method == "POST":
        username = str(request.values.get("user"))
        password = str(request.values.get("pass"))

        if not db.checkUser(username, password):
            return render_template("loginfail.html")

        oid = int(request.values.get("vote"))
        oldid = None if qid not in session["vote"] else session["vote"][qid]

        db.save(qid, oid, oldid)
        session["vote"][qid] = oid

    data = db.get(qid)
    data["qid"] = qid

    return render_template("unsecuredwebpage.html", **data)


if __name__ == '__main__':
    app.run("0.0.0.0", 80)
