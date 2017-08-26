import datetime
import pyramid.httpexceptions as exc

from sqlalchemy import Date, cast

from cornice.resource import resource
from baby_tracker.models import Nap


@resource(collection_path='/naps', path='/naps/today')
class NapView(object):

    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    def collection_get(self):
        """Returns list of all naps by user."""
        user_id = self.request.authenticated_userid
        if not user_id:
            return exc.HTTPForbidden()
        naps = self.request.dbsession.query(Nap).filter_by(user_id=user_id)
        naps_json = [nap.to_json() for nap in naps]
        return {'naps': naps_json}

    def get(self):
        """Return today's naps by user."""
        user_id = self.request.authenticated_userid
        if not user_id:
            return exc.HTTPForbidden()
        today = datetime.date.today()
        # naps = self.request.dbsession.query(Nap).filter_by(user_id=user_id).filter(cast(Nap))
        naps = self.request.dbsession.query(Nap).filter(cast(Nap.start,Date) == today).all()
        naps_json = [nap.to_json() for nap in naps]
        return {'naps': naps_json}

    def collection_post(self):
        """Add single nap"""
        user_id = self.request.authenticated_userid
        nap_json = self.request.json['nap']
        nap = Nap.from_json(nap_json)
        nap.user_id = user_id
        self.request.dbsession.add(nap)
        return {'status': 'OK'}

    def put(self):
        """Update a single nap entry"""
        nap_id = int(self.request.matchdict['id'])
        nap = self.request.dbsession.query(Nap).get(nap_id)
        if nap is not None:
            args = self.request.json['nap']
            for key, value in args.items():
                if args[key] is not None:
                    setattr(nap, key, value)
            self.request.dbsession.commit()
            return {'status': 'OK'}
        raise exc.HTTPNotFound()

    def delete(self):
        """Delete a single nap entry"""
        nap_id = int(self.request.matchdict['id'])
        self.request.dbsession.query(Nap).filter_by(id=nap_id).delete()
        return {'status': 'OK'}
