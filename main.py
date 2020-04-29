from data import db_session
from flask import Flask, render_template, redirect, request
from loginform import LoginForm
from registerform import RegisterForm
import sqlite3
import io
import maps
import requests
import lxml.etree
from data import users
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import os
from data import l



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
@app.route('/my')
def my():
    con1 = sqlite3.connect("db/1.db")
    cur1 = con1.cursor()
    us = cur1.execute("""SELECT * FROM Users""").fetchall() 
    me = dict()
    for user in us:
        me[user[0]] = cur1.execute("""SELECT * FROM Likes
                        WHERE user_id = ?
            """, (user[0],)).fetchall()
    return render_template('my.html',
                           pictures=pict, me=me[current_user.id], artists=painters)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = db_session.create_session()
        user = session.query(users.User).filter(users.User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/like/<p>/<pic>',  methods=['GET', 'POST'])
def like(p, pic):
    session = db_session.create_session()
    likes = session.query(l.Likes).filter(l.Likes.picture.in_([pic])).first()
    if not likes:
        likes = l.Likes()
        likes.picture = pic
        current_user.likes.append(likes)
        session.merge(current_user)
        session.commit()
    
    
    return redirect(f'/picture/{p}/{pic}')

@app.route('/likes_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def likes_delete(id):
    session = db_session.create_session()
    likes = session.query(l.Likes).filter(l.Likes.id == id,
                                      l.Likes.user == current_user).first()
    if likes:
        session.delete(likes)
        session.commit()
    else:
        abort(404)
    return redirect('/my')
     
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/gallery')
def gallery():
    return render_template('gallery.html',
                           artists=artists)

@app.route('/museums')
def museums():
    return render_template('museums.html',
                           m=m)

@app.route('/museum/<m>')
def museum(m):
    return render_template('museum.html',
                           virtual=virtual[m], m=m, pictures=pict, painters=painters)

@app.route('/painter/<p>')
def painter(p):
    return render_template('painter.html',
                           pictures=pictures[p], p=p)


@app.route('/picture/<p>/<pic>')
def picture(p, pic):
    return render_template('picture.html',
                           pictures=pictures[p], p=pic, museums=m)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(users.User).filter(users.User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = users.User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)





if __name__ == '__main__':
    db_session.global_init("db/1.db")
    main()
