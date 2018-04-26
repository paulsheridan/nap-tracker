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
        """Retrieve the signup page"""
        return {}

    @view_config(route_name='reset_email_form', renderer='baby_tracker:templates/pw_email.jinja2')
    def reset_email_form(self):
        """
        Retrieve the initial password reset page
        This page will request the user's email
        and if a matching email is found, an email will
        be sent with a password reset link.
        """
        # TODO: Move this into the auth file maybe?
        return {}

    @view_config(route_name='new_password_form', renderer='baby_tracker:templates/pw_reset.jinja2')
    def new_password_form(self):
        """Retrieve the password reset prompt page"""
        # TODO: Move this into the auth file maybe?
        return {}
