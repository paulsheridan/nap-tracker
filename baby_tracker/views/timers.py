import pyramid.httpexceptions as exc

from pyramid.view import (
    view_config,
    view_defaults
)

@view_defaults(renderer='baby_tracker:templates/timers.jinja2')
class TimerView(object):

    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='timers')
    def get(self):
        """Retrieve the timers HTML page"""
        if not self.logged_in:
            raise exc.HTTPFound(self.request.route_url("index"))
        return {}
