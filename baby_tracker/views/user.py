import datetime
import transaction
import pyramid.httpexceptions as exc

from pyramid.view import (
    view_config,
    view_defaults
    )

from baby_tracker.models import User


@view_defaults(route_name='users', renderer='json')
class UserView(object):

    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(request_method='GET')
    def get(self):
        """Return single user"""
        user_id = int(self.request.matchdict['id'])
        if not self.logged_in or user_id != self.logged_in:
            return exc.HTTPForbidden()
        user = self.request.dbsession.query(User).get(user_id)
        if user is not None:
            return {'user': user.to_json()}
        raise exc.HTTPNotFound()

    @view_config(request_method='POST')
    def collection_post(self):
        """Add single user"""
        user_json = self.request.json
        user = User.from_json(user_json)
        user.hash_password(user_json['password'])
        self.request.dbsession.add(user)
        return {'status': 'OK'}

    @view_config(request_method='PUT')
    def put(self):
        """Update a single user entry"""
        user_id = int(self.request.matchdict['id'])
        if not self.logged_in or user_id != self.logged_in:
            return exc.HTTPForbidden()
        user = self.request.dbsession.query(User).get(user_id)
        if user is not None:
            args = self.request.json
            for key, value in args.items():
                if args[key] is not None:
                    setattr(user, key, value)
            transaction.commit()
            return {'user': user.to_json()}
        raise exc.HTTPNotFound()

    @view_config(request_method='DELETE')
    def delete(self):
        """Delete a single user entry"""
        user_id = int(self.request.matchdict['id'])
        if not self.logged_in or user_id != self.logged_in:
            return exc.HTTPForbidden()
        self.request.dbsession.query(User).filter_by(id=user_id).delete()
        return {'status': 'OK'}
