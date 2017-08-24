from pyramid.config import Configurator

from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    authn_policy = AuthTktAuthenticationPolicy(
        settings['tutorial.secret'], hashalg='sha512')
    config.set_authentication_policy(authn_policy)

    config.include('cornice')
    config.include('.models')
    config.scan()
    return config.make_wsgi_app()
