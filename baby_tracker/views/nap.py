import datetime
import transaction
import pyramid.httpexceptions as exc

from sqlalchemy import Date, cast

from baby_tracker.models import Nap, User

from pyramid.view import (
view_config,
view_defaults
)


@view_defaults(renderer='json')
class NapView(object):

    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='naps', request_method='GET')
    def get(self):
        """Returns"""
        if not self.logged_in:
            return exc.HTTPForbidden()
        nap_id = self.request.matchdict['id']
        if nap_id == '*':
            naps = self.request.dbsession.query(User).filter_by(id=self.logged_in).first().naps
            naps_json = [nap.to_json() for nap in naps]
            return {'naps': naps_json}
        else:
            nap = self.request.dbsession.query(User).filter_by(
                id=self.logged_in).first().naps.filter_by(id=nap_id).first()
            if not nap:
                return exc.HTTPNotFound()
            return {'nap': nap.to_json()}

    @view_config(route_name='naps', request_method='POST')
    def post(self):
        """Add single nap"""
        if not self.logged_in:
            return exc.HTTPForbidden()
        nap_json = self.request.json
        nap = Nap.from_json(nap_json)
        nap.user_id = self.logged_in
        self.request.dbsession.add(nap)
        return {'status': 'OK'}

    @view_config(route_name='naps', request_method='PUT')
    def put(self):
        """Update a single nap entry"""
        if not self.logged_in:
            return exc.HTTPForbidden()
        nap_id = int(self.request.matchdict['id'])
        nap = self.request.dbsession.query(User).filter_by(
            id=self.logged_in).first().naps.filter_by(id=nap_id).first()
        if nap is not None:
            args = self.request.json
            for key, value in args.items():
                if args[key] is not None:
                    setattr(nap, key, value)
            transaction.commit()
            return {'nap': nap.to_json()}
        raise exc.HTTPNotFound()

    @view_config(route_name='naps', request_method='DELETE')
    def delete(self):
        """Delete a single nap entry"""
        nap_id = int(self.request.matchdict['id'])
        nap = self.request.dbsession.query(User).filter_by(
            id=self.logged_in).first().naps.filter_by(id=nap_id).delete()
        if not nap:
            return exc.HTTPNotFound()
        return {'status': 'OK'}


    @view_defaults(route_name='naps_today', request_method='GET')
    def get_today(self):
        """Return today's naps by user."""
        if not self.logged_in:
            return exc.HTTPForbidden()
        naps = self.request.dbsession.query(User).filter_by(
            id=self.logged_in).first().naps.filter(
                cast(Nap.start, Date) == datetime.date.today())
        naps_json = [nap.to_json() for nap in naps]
        return {'naps': naps_json}
