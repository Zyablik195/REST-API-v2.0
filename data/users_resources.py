from . import db_session
from .users import User
from flask_restful import reqparse, abort, Api, Resource
import flask
from flask import jsonify, request, render_template
from .reqparse import parser


def abort_if_users_not_found(users_id):
    if not type(users_id) == int:
        abort(404, message=f"Wrong arg type")
        return
    session = db_session.create_session()
    news = session.query(User).get(users_id)
    if not news:
        abort(404, message=f"News {users_id} not found")


class UsersResource(Resource):
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        return jsonify(
        {
            'users': users.to_dict(only=('id', 'name', 'surname', 'age', 'position', 'speciality', 'address', 'city_from', 'email'))
        }
    )

    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        users = session.query(User).get(users_id)
        session.delete(users)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify(
        {
            'users':
                [item.to_dict(only=('id', 'name', 'surname', 'age', 'position', 'speciality', 'address', 'city_from', 'email'))
                 for item in users]
        }
    )


    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        users = User(
            id=args['id'],
            name=args['name'],
            surname=args['surname'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            city_from=args['city_from'],
            email=args['email']
        )
        users.set_password(args['hashed_password'])
        session.add(users)
        session.commit()
        return jsonify({'success': 'OK'})