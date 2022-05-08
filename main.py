import requests
from flask import Flask, url_for, request, render_template, redirect, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_restful import reqparse, abort, Api, Resource
from data import db_session, jobs_api, users_resources, jobs_resources
from data.users import User
from data.jobs import Jobs
from data.departments import Departments
from data.hazards import Hazards
from data.forms.user import RegisterForm, LoginForm, JobForm, DepartmentForm



app = Flask(__name__)
api = Api(app)

api.add_resource(users_resources.UsersListResource, '/api/v2/users')
api.add_resource(users_resources.UsersResource, '/api/v2/users/<int:users_id>')

api.add_resource(jobs_resources.JobsListResource, '/api/v2/jobs')
api.add_resource(jobs_resources.JobsResource, '/api/v2/jobs/<int:jobs_id>')

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_sess = 0
login_manager = LoginManager()
login_manager.init_app(app)

                                              
'''
@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id > 0).all()
    for i in jobs:
        if i.is_finished:
            i.is_finished1 = 'Is finished'
        else:
            i.is_finished1 = 'Is not finished'
        user = db_sess.query(User).filter(User.id == i.team_leader).first()
        i.team_leader1 = user.name + user.surname
    return render_template("register.html", jobs=jobs)
'''

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/')
def index():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id > 0).all()
    for i in jobs:
        if i.is_finished:
            i.is_finished1 = 'Is finished'
        else:
            i.is_finished1 = 'Is not finished'
        user = db_sess.query(User).filter(User.id == i.team_leader).first()
        i.team_leader1 = user.name + ' ' + user.surname
    return render_template("index.html", jobs=jobs)


@app.route('/departments')
def index1():
    db_sess = db_session.create_session()
    departments = db_sess.query(Departments).filter(Departments.id > 0).all()
    for i in departments:
        user = db_sess.query(User).filter(User.id == i.chief).first()
        i.chief1 = user.name + ' ' + user.surname
    return render_template("departments.html", departments=departments)


@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_job(id):
    form = JobForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.creater == current_user.id
                                          ).first()
        if jobs:
            form.team_leader.data = jobs.team_leader
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.hazard.data = jobs.hazard
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          Jobs.creater == current_user.id
                                          ).first()
        if jobs:
            jobs.team_leader = form.team_leader.data
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.hazard = form.hazard.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('addjob.html',
                           title='Редактирование работы',
                           form=form
                           )


@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_job(id):
    db_sess = db_session.create_session()
    news = db_sess.query(Jobs).filter(Jobs.id == id).filter(
        (Jobs.creater == current_user.id) | (current_user.id == 1)
                                      ).first()
    if news:
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')


@app.route('/addjob', methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        job = Jobs(
            team_leader=form.team_leader.data,
            job = form.job.data,
            work_size = form.work_size.data,
            collaborators = form.collaborators.data,
            hazard=form.hazard.data,
            is_finished = form.is_finished.data,
            creater = current_user.id
        )
        db_sess.add(job)
        db_sess.commit()
        return redirect('/')
    return render_template('addjob.html', title='Добавить работу', form=form)


@app.route('/departments/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_department(id):
    form = DepartmentForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        departments = db_sess.query(Departments).filter(Departments.id == id,
                                          Departments.creater == current_user.id
                                          ).first()
        if departments:
            form.title.data = departments.title
            form.chief.data = departments.chief
            form.members.data = departments.members
            form.email.data = departments.email
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        departments = db_sess.query(Departments).filter(Departments.id == id,
                                          Departments.creater == current_user.id
                                          ).first()
        if departments:
            departments.title = form.title.data
            departments.chief = form.chief.data
            departments.members = form.members.data
            departments.email = form.email.data
            db_sess.commit()
            return redirect('/departments')
        else:
            abort(404)
    return render_template('adddepartment.html',
                           title='Редактирование отдела',
                           form=form
                           )


@app.route('/departments_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_department(id):
    db_sess = db_session.create_session()
    departments = db_sess.query(Departments).filter(Departments.id == id).filter(
        (Departments.creater == current_user.id) | (current_user.id == 1)
                                      ).first()
    if departments:
        db_sess.delete(departments)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/departments')


@app.route('/adddepartment', methods=['GET', 'POST'])
@login_required
def add_department():
    form = DepartmentForm()
    if form.validate_on_submit():
        department = Departments(
            title=form.title.data,
            chief = form.chief.data,
            members = form.members.data,
            email = form.email.data,
            creater = current_user.id
        )
        db_sess.add(department)
        db_sess.commit()
        return redirect('/departments')
    return render_template('adddepartment.html', title='Добавить отдел', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
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
            surname = form.surname.data,
            age = form.age.data,
            position = form.position.data,
            speciality = form.speciality.data,
            address = form.address.data,
            email = form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/users_show/<int:user_id>')
def city(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return 'Пользователь не найден'
    try:
        text = user.city_from
        geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"

        geocoder_params = {
            "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
            "geocode": text,
            "format": "json"}
        response = requests.get(geocoder_api_server, params=geocoder_params)
        json_response = response.json()
        try:
            toponym = json_response["response"]["GeoObjectCollection"][
                "featureMember"][0]["GeoObject"]["Point"]["pos"]
        except Exception as ee:
            return f'По запросу "{text}" ничего не было найдено, попробуйте другой запрос.'

        api_key = "8b36d8d1-7081-4f84-b56e-b96c77e39694"

        address_ll = toponym.replace(' ', ',')
        map_api_server = f"https://static-maps.yandex.ru/1.x/?ll={address_ll}&l=sat&spn=0.1,0.1&pt={address_ll},pmwtm1"

        img = map_api_server
        return render_template('show_city.html', title='hometown', item=user, img=img)
    except Exception as e:
        return f'Произошла ошибка, вот её текст: {e}'


def main():
    global db_sess
    # name = input()
    db_session.global_init("db/blogs.db")
    app.register_blueprint(jobs_api.blueprint)
    db_sess = db_session.create_session()
    app.run(host='127.0.0.1', port=5000)

    """
    user = User()
    user.surname = "Scott"
    user.name = "Ridley"
    user.age = 21
    user.position = "captain"
    user.speciality = "research engineer"
    user.address = "module_1"
    user.email = "scott_chief@mars.org"
    user.hashed_password = "cap"
    db_sess.add(user)

    user = User()
    user.surname = "Weir"
    user.name = "Andy"
    user.age = 27
    user.position = "support1"
    user.speciality = "geologist"
    user.address = "module_1"
    user.email = "22222@mars.org"
    user.hashed_password = "cap2"
    db_sess.add(user)

    user = User()
    user.surname = "Watny"
    user.name = "Mark"
    user.age = 26
    user.position = "support2"
    user.speciality = "biologist"
    user.address = "module_2"
    user.email = "33333@mars.org"
    user.hashed_password = "cap3"
    db_sess.add(user)

    job = Jobs()
    job.team_leader = 1
    job.job = 'Deployment of residential modules 1 and 2'
    job.work_size = 15
    job.collaborators = '2, 3'
    job.is_finished = False
    db_sess.add(job)

    job = Jobs()
    job.team_leader = 2
    job.job = 'Exploration of mineral resources'
    job.work_size = 15
    job.collaborators = '4, 3'
    job.is_finished = False
    db_sess.add(job)

    job = Jobs()
    job.team_leader = 3
    job.job = 'Development of a management system'
    job.work_size = 25
    job.collaborators = '5'
    job.is_finished = False
    db_sess.add(job)
    '''
    for i in range(4):
        user = User()
        user.surname = dick['user.surname'][i]
        user.name = dick['user.name'][i]
        user.age = dick['user.age'][i]
        user.position = dick['user.position'][i]
        user.speciality = dick['user.speciality'][i]
        user.address = dick['user.address'][i]
        user.email = dick['user.email'][i]
        db_sess.add(user)
    '''
    db_sess.commit()
    """


if __name__ == '__main__':
    main()