from pyramid.view import view_config

@view_config(route_name='index_page', renderer='baby_tracker:templates/index.jinja2')
def index_view(request):
    return {}
