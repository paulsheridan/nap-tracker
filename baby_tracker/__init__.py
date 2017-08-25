from pyramid.config import Configurator

from pyramid.authorization import ACLAuthorizationPolicy


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

     # Pyramid requires an authorization policy to be active.
    config.set_authorization_policy(ACLAuthorizationPolicy())
    # Enable JWT authentication.
    config.include('pyramid_jwt')
    config.set_jwt_authentication_policy('secret')

    config.include('cornice')
    config.include('.models')
    config.scan()
    return config.make_wsgi_app()
