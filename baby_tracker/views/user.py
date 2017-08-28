import datetime
import pyramid.httpexceptions as exc

from cornice.resource import resource, view
from baby_tracker.models import User


@resource(collection_path='/users', path='/users/{id}')
class UserView(object):

    def __init__(self, request):
        self.request = request

    def get(self):
        """Return single user"""
        user_id = int(self.request.matchdict['id'])
        user = self.request.dbsession.query(User).get(user_id)
        if user is not None:
            user_json = user.to_json()
            return {'user': user_json}
        raise exc.HTTPNotFound()

    def collection_post(self):
        """Add single user"""
        user_json = self.request.json
        user = User.from_json(user_json)
        user.hash_password(user_json['password'])
        self.request.dbsession.add(user)
        return {'status': 'OK'}

    def put(self):
        """Update a single user entry"""
        user_id = int(self.request.matchdict['id'])
        user = self.request.dbsession.query(User).get(user_id)
        if user is not None:
            args = self.request.json
            for key, value in args.items():
                if args[key] is not None:
                    setattr(user, key, value)
            self.request.dbsession.commit()
            return {'status': 'OK'}
        raise exc.HTTPNotFound()

    def delete(self):
        """Delete a single user entry"""
        user_id = int(self.request.matchdict['id'])
        self.request.dbsession.query(User).filter_by(id=user_id).delete()
        return {'status': 'OK'}
