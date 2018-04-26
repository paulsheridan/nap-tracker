import transaction
import datetime
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
from pyramid_mailer.message import Message


@view_defaults(renderer='json')
class AuthView(object):

    def __init__(self, request):
        self.request = request

    @view_config(route_name='login', request_method='POST')
    def login(self):
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

    @view_config(route_name='send_reset_link', request_method='POST')
    def send_reset_link(self):
        """
        Query user email and if found, send email with secret
        password reset link
        """
        email = self.request.json['email']
        user = self.request.dbsession.query(User).filter_by(email=email).first()
        if user is not None:
            pass_secret = user.generate_secret()
            reset_link = "http://www.naptrack.com/reset/secret/{}".format(pass_secret)
            mailer = self.request.mailer
            message = Message(subject="Password Reset",
                              sender="admin@naptrack.com",
                              recipients=[user.email],
                              body=reset_link,
                             )
            mailer.send(message)
            transaction.commit()
        return {'status': 'OK'}

    @view_config(route_name='reset_password', request_method='POST')
    def reset_password(self):
        """Request user password reset email"""
        reset_secret = self.request.json['reset_secret']
        new_pass = self.request.json['password']
        user = self.request.dbsession.query(User).filter_by(reset_secret=reset_secret).first()
        if user is not None and user.reset_expire > datetime.datetime.utcnow():
            try:
                user.hash_password(new_pass)
            except ValueError:
                return exc.HTTPBadRequest()
            user.clear_secret()
            transaction.commit()
            return {'status': 'OK'}
        return exc.HTTPUnauthorized()
