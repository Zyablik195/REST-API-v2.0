import flask
from flask import jsonify, request, render_template
from . import db_session
from .users import  User

blueprint = flask.Blueprint(
    'users_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users', methods=['POST'])
def create_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'surname', 'age', 'position', 'speciality', 'address', 'city_from', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(request.json['id'])
    if user:
        return jsonify({'error': 'Id already exists'})
    users = User(
        id=request.json['id'],
        name=request.json['name'],
        surname=request.json['surname'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        city_from=request.json['city_from'],
        email=request.json['email']
    )
    users.set_password(request.json['hashed_password'])
    db_sess.add(users)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users', methods=['PUT'])
def change_users():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ['id', 'name', 'surname', 'age', 'position', 'speciality', 'address', 'city_from', 'email', 'hashed_password']):
        return jsonify({'error': 'Bad request'})
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == request.json['id']).first()
    if not user:
        return jsonify({'error': 'Id doesnt exist'})
    user.id = request.json['id']
    user.name = request.json['name']
    user.surname = request.json['surname']
    user.age = request.json['age']
    user.position = request.json['position']
    user.speciality = request.json['speciality']
    user.address = request.json['address']
    user.city_from = request.json['city_from']
    user.email = request.json['email']
    user.set_password(request.json['hashed_password'])
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/users')
def get_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name', 'surname', 'age', 'position', 'speciality', 'address', 'city_from', 'email'))
                 for item in users]
        }
    )


@blueprint.route('/api/users/<users_id>', methods=['GET'])
def get_one_users(users_id):
    if not users_id.isdigit() or int(users_id) < 1:
        return jsonify({'error': 'Wrong parametr'})
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(int(users_id))
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(only=('id', 'name', 'surname', 'age', 'position', 'speciality', 'address', 'city_from', 'email'))
        }
    )


@blueprint.route('/api/users/<users_id>', methods=['GET'])
def get_one_users(users_id):
    if not users_id.isdigit() or int(users_id) < 1:
        return jsonify({'error': 'Wrong parametr'})
    db_sess = db_session.create_session()
    users = db_sess.query(User).get(int(users_id))
    if not users:
        return jsonify({'error': 'Not found'})
    return jsonify(
        {
            'users': users.to_dict(only=('id', 'name', 'surname', 'age', 'position', 'speciality', 'address', 'city_from', 'email'))
        }
    )