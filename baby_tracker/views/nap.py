import datetime
import transaction
import pyramid.httpexceptions as exc

from sqlalchemy import Date, cast

from cornice.resource import resource
from baby_tracker.models import Nap


@resource(collection_path='/naps', path='/naps/{id}')
class NapView(object):

    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    def collection_get(self):
        """Returns list of all naps by user"""
        if not self.logged_in:
            return exc.HTTPForbidden()
        naps = self.request.dbsession.query(Nap).filter_by(user_id=self.logged_in)
        naps_json = [nap.to_json() for nap in naps]
        return {'naps': naps_json}

    def get(self):
        """Return a single nap."""
        if not self.logged_in:
            return exc.HTTPForbidden()
        nap_id = int(self.request.matchdict['id'])
        nap = self.request.dbsession.query(Nap).filter_by(
            user_id=self.logged_in).filter_by(id=nap_id).first()
        return {'nap': nap.to_json()}

    def collection_post(self):
        """Add single nap"""
        if not self.logged_in:
            return exc.HTTPForbidden()
        nap_json = self.request.json
        nap = Nap.from_json(nap_json)
        nap.user_id = self.logged_in
        self.request.dbsession.add(nap)
        return {'status': 'OK'}

    def put(self):
        """Update a single nap entry"""
        if not self.logged_in:
            return exc.HTTPForbidden()
        nap_id = int(self.request.matchdict['id'])
        nap = self.request.dbsession.query(Nap).filter_by(
            user_id=self.logged_in).filter_by(id=nap_id).first()
        if nap is not None:
            args = self.request.json
            for key, value in args.items():
                if args[key] is not None:
                    setattr(nap, key, value)
            transaction.commit()
            return {'status': 'OK'}
        raise exc.HTTPNotFound()

    def delete(self):
        """Delete a single nap entry"""
        nap_id = int(self.request.matchdict['id'])
        self.request.dbsession.query(Nap).filter_by(
            user_id=self.logged_in).filter_by(id=nap_id).delete()
        return {'status': 'OK'}


@resource(path='/naps/today')
class TodayView(object):

    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    def get(self):
        """Return today's naps by user."""
        if not self.logged_in:
            return exc.HTTPForbidden()
        naps = self.request.dbsession.query(Nap).filter(cast(
            Nap.start, Date) == datetime.date.today()).filter_by(user_id=self.logged_in)
        naps_json = [nap.to_json() for nap in naps]
        return {'naps': naps_json}
