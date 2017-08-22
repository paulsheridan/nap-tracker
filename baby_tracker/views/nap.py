import datetime
import pyramid.httpexceptions as exc

from cornice.resource import resource
from baby_tracker.models import Nap

@resource(collection_path='/naps', path='/naps/{id}')
class NapView(object):

    def __init__(self, request):
        self.request = request

    def collection_get(self):
        """Returns list of todays naps"""
        naps = self.request.dbsession.query(Nap).all()
        naps_json = [nap.to_json() for nap in naps]
        return {'naps': naps_json}

    def get(self):
        """Return single nap"""
        nap_id = int(self.request.matchdict['id'])
        nap = self.request.dbsession.query(Nap).get(nap_id)
        if nap is not None:
            nap_json = nap.to_json()
            return {'nap': nap_json}
        raise exc.HTTPNotFound()

    def collection_post(self):
        """Add single nap"""
        nap = self.request.json['nap']
        self.request.dbsession.add(Nap.from_json(nap))
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
