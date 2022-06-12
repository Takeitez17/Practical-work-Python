from flask import Flask, render_template, redirect, request, abort, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.jobs import Jobs
from flask_restful import Api
from forms.login import LoginForm
from forms.user import RegisterForm
from forms.jobs import JobsForm
from forms.index import IndexForm
import neuron_processing
import api_neuron

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.neural_network import MLPClassifier

app = Flask(__name__, static_folder="templates")
app.config['SECRET_KEY'] = 'my_secret_key'
api = Api(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route("/", methods=['GET', 'POST'])
def index():
    form = IndexForm()
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        if form.validate_on_submit():
            print(form.desc.data)
            form.answer.data = neuron_processing.neuron_work(form.desc.data)
            db_sess = db_session.create_session()
            request = Jobs(user_id=current_user.get_id(), description=form.desc.data, result=form.answer.data)
            db_sess.add(request)
            db_sess.commit()
    return render_template("index.html", form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        print("Зашёл")
        print(form.email.data)
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
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print("Тутачки")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/jobs', methods=['GET', 'POST'])
@login_required
def add_jobs():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.title = form.title.data
        jobs.content = form.content.data
        jobs.is_private = form.is_private.data
        current_user.jobs.append(jobs)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление новости',
                           form=form)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            form.title.data = jobs.title
            form.content.data = jobs.content
            form.is_private.data = jobs.is_private
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.user == current_user
                                          ).first()
        if jobs:
            jobs.title = form.title.data
            jobs.content = form.content.data
            jobs.is_private = form.is_private.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование новости',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      Jobs.user == current_user
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def main():
    db_session.global_init("db/lab_project.sqlite")
    api.add_resource(api_neuron.Request, '/api/request/<int:user_request_id>')
    api.add_resource(api_neuron.ListRequest, '/api/requests')
    app.run()


if __name__ == '__main__':
    main()
