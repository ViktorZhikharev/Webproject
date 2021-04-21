from flask import Flask, redirect, render_template, session, jsonify
from data.users import User
from forms.user import RegisterForm, LoginForm
from forms.post import PostForm, CommentForm, MessageForm
import data.db_session as db_session
db_session.global_init("db/socnet.db")

from data.posts import Post
from data.comments import Comment
from data.messages import Message
from data import posts_api
from flask import make_response



app = Flask(__name__)
app.config['SECRET_KEY'] = 'efbgdkl458690uy94fu309uwcu4985hj8903u809fubgadmkmdfaklbndflsmbklwetmkthnjmlwtj'


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    if session.get('user_id', -1) == -1:
        form = RegisterForm()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Пароли не совпадают")
            db_sess = db_session.create_session()
            if db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('register.html', title='Регистрация',
                                       form=form,
                                       message="Такой пользователь уже есть")
            user = User(
                name=form.name.data,
                email=form.email.data,
                phone=form.phone.data,
                about=form.about.data,
                birth=form.birth.data
            )
            user.set_password(form.password.data)
            db_sess.add(user)
            db_sess.commit()
            return redirect('/login')
        if session.get('user_id', -1) != -1:
            username = db_sess.query(User).filter(User.id == session.get('user_id')).first().name
        else:
            username = 'pass'
        return render_template('register.html', title='Регистрация', form=form, username=username)
    else:
        return "<h1>You can't register new user while logged in</h1>"


@app.route('/edit_user_info', methods=['GET', 'POST'])
def eri():
    if session.get('user_id', -1) != -1:
        form = RegisterForm()
        db_sess = db_session.create_session()
        if form.validate_on_submit():
            if form.password.data != form.password_again.data:
                return render_template('edit.html', title='Редактирование профиля',
                                       form=form,
                                       message="Пароли не совпадают")
            if form.name.data:
                db_sess.query(User).filter(User.id == session.get('user_id')).update({'name': form.name.data})
            if form.birth.data:
                db_sess.query(User).filter(User.id == session.get('user_id')).update({'birth': form.birth.data})
            if form.phone.data:
                db_sess.query(User).filter(User.id == session.get('user_id')).update({'phone': form.phone.data})
            user = db_sess.query(User).filter(User.id == session.get('user_id')).first()
            if form.password.data:
                user.set_password(form.password.data)
            db_sess.commit()
            return redirect('/login')
        if session.get('user_id', -1) != -1:
            username = db_sess.query(User).filter(User.id == session.get('user_id')).first().name
        else:
            username = 'pass'
        return render_template('edit.html', title='Редактирование профиля', form=form, username=username)
    else:
        return redirect('/register')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id', -1) == -1:
        form = LoginForm()
        if form.validate_on_submit():
            db_sess = db_session.create_session()
            if session.get('user_id', -1) != -1:
                username = db_sess.query(User).filter(User.id == session.get('user_id')).first().name
            else:
                username = 'pass'
            if not db_sess.query(User).filter(User.email == form.email.data).first():
                return render_template('login.html', title='Вход',
                                       form=form,
                                       message="Упс, пользователь не обнаружен")
            user = db_sess.query(User).filter(User.email == form.email.data).first()
            if user.check_password(form.password.data):
                session['user_id'] = user.id
            else:
                return render_template('login.html', title='Вход',
                                       form=form,
                                       message="wrong password")
            db_sess.commit()
            return redirect('/')
        if session.get('user_id', -1) != -1:
            username = db_sess.query(User).filter(User.id == session.get('user_id')).first().name
        else:
            username = 'pass'
        return render_template('login.html', title='Вход', form=form, username=username)
    else:
        return redirect('/')


@app.route('/')
@app.route('/index')
def index():
    db_sess = db_session.create_session()
    news = db_sess.query(Post)
    if session.get('user_id', -1) != -1:
        username = db_sess.query(User).filter(User.id == session.get('user_id')).first().name
    else:
        username = 'pass'
    print(session.get('user_id'))
    return render_template("index.html", posts=news, username=username, title='ПроектСоцсеть').replace('&lt;', '<').replace('&gt;', '>')


@app.route('/logout')
def logout():
    session['user_id'] = -1
    return redirect('/')

@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post(id):
    db_sess = db_session.create_session()
    if session.get('user_id', -1) != -1:
        username = db_sess.query(User).filter(User.id == session.get('user_id')).first().name
    else:
        username = 'pass'
    item = db_sess.query(Post).filter(Post.id == id).first()
    form=CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            parent=id,
            content=form.text.data,
            author=session.get('user_id'))
        db_sess.add(comment)
        db_sess.commit()
        return redirect('/post/' + str(id))
    comments = db_sess.query(Comment).filter(Comment.parent == id).all()
    return render_template("post.html", item=item, comments=comments, form=form, username=username, title='Пост ' + item.title).replace('&lt;', '<').replace('&gt;', '>')


@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    db_sess = db_session.create_session()
    if session.get('user_id', -1) == -1:
        return redirect('/login')
    elif db_sess.query(User).filter(User.id == session.get('user_id')).first():
        form = PostForm()
        username = db_sess.query(User).filter(User.id == session.get('user_id')).first().name
        if form.validate_on_submit():
            post = Post(
                title=form.title.data,
                content=form.text.data,
                author=session.get('user_id'))
            db_sess.add(post)
            db_sess.commit()
            return redirect('/')
        return render_template('newpost.html', title='Новый пост', form=form, username=username).replace('&lt;', '<').replace('&gt;', '>')
    else:
        return 'Error: user is not registered but logged in'


@app.route('/user/<int:id>')
def user(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Post).filter(Post.author == id).all()
    user = db_sess.query(User).filter(User.id == id).first()
    if session.get('user_id', -1) != -1:
        username = db_sess.query(User).filter(User.id == session.get('user_id')).first().name
    else:
        username = 'pass'
    print(session.get('user_id'))
    return render_template("user.html", posts=news, user=user, username=username, title=username).replace('&lt;', '<').replace('&gt;', '>')

@app.route('/msg/<int:id>', methods=['GET', 'POST'])
def mess(id):
    db_sess = db_session.create_session()
    form = MessageForm()
    if session.get('user_id', -1) == -1:
        return redirect('/login')
    elif not db_sess.query(User).filter(User.id == id).first():
        return '''user not registred </br><a href="/">mainpage<a>'''
    elif id == session.get('user_id'):
        msg = db_sess.query(Message).filter(Message.reciever == id).all()
        title='Входящие'
    else:
        title='Исходящие для ' + db_sess.query(User).filter(User.id == id).first().name
        msg = db_sess.query(Message).filter(Message.reciever == id).filter(Message.author == session.get('user_id')).all()
        if form.validate_on_submit():
            message = Message(
                content=form.text.data,
                author=session.get('user_id'),
                reciever = id)
            db_sess.add(message)
            db_sess.commit()
            return redirect('/msg/' + str(id))
    if session.get('user_id', -1) != -1:
        username = db_sess.query(User).filter(User.id == session.get('user_id')).first().name
    else:
        username = 'pass'
    print(session.get('user_id'))
    return render_template("messages.html",title=title,id=id, form=form, msg=msg, username=username).replace('&lt;', '<').replace('&gt;', '>')


def main():
    app.register_blueprint(posts_api.blueprint)
    app.run(port=8080)


if __name__ == '__main__':
    main()