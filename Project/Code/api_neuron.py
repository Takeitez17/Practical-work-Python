from flask import jsonify, request
from flask_restful import Resource, abort, reqparse
from data import db_session
from data.jobs import Jobs
from data.users import User

parser = reqparse.RequestParser()
parser.add_argument('user_request_id', required=True)
parser.add_argument('user_id', required=True)
parser.add_argument('description', required=True)
parser.add_argument('result', required=True)


def abort_if_request_not_found(user_request_id):
    session = db_session.create_session()
    req = session.query(Jobs).get(user_request_id)
    if not req:
        abort(404, message=f"Request {user_request_id} not found")


class Request(Resource):

    def get(self, user_request_id):
        abort_if_request_not_found(user_request_id)
        session = db_session.create_session()
        req = session.query(Jobs).get(user_request_id)
        return jsonify({'user_request_id': req.to_dict(
            only=('description', 'result'))})

    def delete(self, user_request_id):
        abort_if_request_not_found(user_request_id)
        session = db_session.create_session()
        req = session.query(Jobs).get(user_request_id)
        session.delete(req)
        session.commit()
        return jsonify({'success': 'OK'})


class ListRequest(Resource):

    def get(self):
        session = db_session.create_session()
        req = session.query(Jobs).all()
        return jsonify({'user_request_id': [item.to_dict(
            only=('description', 'result')) for item in req]})
