from pyramid.view import (
    view_config,
    view_defaults
    )

from baby_tracker.models import User


@view_defaults(route_name='login', renderer='json')
class AuthView(object):

    def __init__(self, request):
        self.request = request

    @view_config(request_method='POST')
    def post(self):
        user_id = self.authenticate()
        if user_id:
            return {
                'result': 'ok',
                'token': self.request.create_jwt_token(user_id)
            }
        return {'result': 'error'}

    def authenticate(self):
        email = self.request.json['email']
        password = self.request.json['password']
        user = self.request.dbsession.query(User).filter_by(email=email).first()
        if user and user.check_password(password):
            return user.id
        return None
