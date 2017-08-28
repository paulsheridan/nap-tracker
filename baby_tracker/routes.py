def includeme(config):
    config.add_route('login', '/login')
    config.add_route('users', '/users')
    config.add_route('naps', '/naps/{id}')
    config.add_route('meals', '/meals/{id}')
    config.add_route('naps_today', '/naps/today')
    config.add_route('meals_today', '/meals/today')
