from pyramid.view import view_config

@view_config(route_name='index', renderer='baby_tracker:templates/index.jinja2')
def index_view(request):
    return {}

@view_config(route_name='signup', renderer='baby_tracker:templates/signup.jinja2')
def signup_view(request):
    return {}

@view_config(route_name='timers', renderer='baby_tracker:templates/timers.jinja2')
def signup_view(request):
    return {}
