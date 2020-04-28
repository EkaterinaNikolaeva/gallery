from data import db_session
from flask import Flask, render_template, redirect, request
from loginform import LoginForm
from registerform import RegisterForm
import sqlite3
from PIL import Image
import io
import maps
import requests
import lxml.etree
from data import users
from flask_login import LoginManager, login_user, logout_user, login_required
import os



app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


con = sqlite3.connect("db/1.db")
cur = con.cursor()
painters = cur.execute("""SELECT * FROM Painters""").fetchall()
pict = cur.execute("""SELECT * FROM Pictures""").fetchall()
m = cur.execute("""SELECT * FROM Museums""").fetchall()
pictures = dict()
for painter in painters:
    pictures[painter[1]] = cur.execute("""SELECT * FROM Pictures
                    WHERE Painter IN (SELECT id FROM 
                    Painters WHERE Name = ?)
        """, (painter[1],)).fetchall()
artists = []
for painter in painters:
    artists.append([painter[2], painter[1]])

virtual = dict()
for museum in m:
    virtual[museum[1]] = cur.execute("""SELECT * FROM Pictures
                    WHERE Museum IN (SELECT id FROM 
                    Museums WHERE Name = ?)
        """, (museum[1],)).fetchall()


def main():
    maps
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

@login_manager.user_loader
def load_user(user_id):
    session = db_session.create_session()
    return session.query(users.User).get(user_id)


@app.route('/')
def root():
    return render_template('gallery.html',
                           artists=artists)


@app.route('/success')
def success():
    return render_template("success.html")




if __name__ == '__main__':
    db_session.global_init("db/1.db")
    main()
