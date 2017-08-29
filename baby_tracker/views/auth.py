import pyramid.httpexceptions as exc

from pyramid.view import (
    view_config,
    view_defaults
    )
from pyramid.security import (
    remember,
    forget,
    )
from pyramid.response import Response
from baby_tracker.models import User


@view_defaults(renderer='json')
class AuthView(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='login', request_method='POST')
    def post(self):
        user_id = self.authenticate()
        if not user_id:
            return exc.HTTPUnauthorized()
        headers = remember(self.request, user_id)
        return Response(headers=headers)

    @view_config(route_name='logout', request_method='POST')
    def logout(self):
        headers = forget(self.request)
        return Response(headers=headers)

    def authenticate(self):
        email = self.request.json['email']
        password = self.request.json['password']
        user = self.request.dbsession.query(User).filter_by(email=email).first()
        if user and user.check_password(password):
            return user.id
        return None
