import pyramid.httpexceptions as exc

from pyramid.view import (
    view_config,
    view_defaults
)

@view_defaults()
class PageView(object):

    def __init__(self, request):
        self.request = request
        self.logged_in = request.authenticated_userid

    @view_config(route_name='timers', renderer='baby_tracker:templates/timers.jinja2')
    def timers_view(self):
        """
        Retrieve the timers page
        or redirect to index if not signed in.
        """
        if not self.logged_in:
            raise exc.HTTPFound(self.request.route_url("index"))
        return {}

    @view_config(route_name='index', renderer='baby_tracker:templates/index.jinja2')
    def index_view(self):
        """Retrieve the index page"""
        return {}

    @view_config(route_name='signup', renderer='baby_tracker:templates/signup.jinja2')
    def signup_view(self):
        """Retrieve the signupå page"""
        return {}
