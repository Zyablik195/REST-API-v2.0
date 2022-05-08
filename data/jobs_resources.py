from . import db_session
from .jobs import Jobs
from flask_restful import reqparse, abort, Api, Resource
import flask
from flask import jsonify, request, render_template
from .reqparse1 import parser


def abort_if_jobs_not_found(jobs_id):
    if not type(jobs_id) == int:
        abort(404, message=f"Wrong arg type")
        return
    session = db_session.create_session()
    jobs = session.query(Jobs).get(jobs_id)
    if not jobs:
        abort(404, message=f"jobs {jobs_id} not found")


class JobsResource(Resource):
    def get(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        return jsonify(
        {
            'jobs': jobs.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'hazard', 'is_finished'))
        }
    )

    def delete(self, jobs_id):
        abort_if_jobs_not_found(jobs_id)
        session = db_session.create_session()
        jobs = session.query(Jobs).get(jobs_id)
        session.delete(jobs)
        session.commit()
        return jsonify({'success': 'OK'})


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify(
        {
            'jobs':
                [item.to_dict(only=('id', 'team_leader', 'job', 'work_size', 'collaborators', 'hazard', 'is_finished'))
                 for item in jobs]
        }
    )


    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            id=args['id'],
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            hazard=args['hazard'],
            is_finished=args['is_finished']
        )
        session.add(jobs)
        session.commit()
        return jsonify({'success': 'OK'})