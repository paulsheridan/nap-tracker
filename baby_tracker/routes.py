def includeme(config):
    config.add_route('index', '/')
    config.add_route('timers', '/timers')

    config.add_route('signup', '/signup')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')

    config.add_route('users', '/users')

    config.add_route('start_nap', '/nap/start')
    config.add_route('end_nap', '/nap/end')
    config.add_route('naps_today', '/today/naps')
    # config.add_route('naps', '/naps/{id}')
    # config.add_route('naps_wildcard', '/naps')

    # config.add_route('meals', '/meals/{id}')
    # config.add_route('meals_wildcard', '/meals')
    # config.add_route('meals_today', '/today/meals')

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('js', 'baby_tracker:static/js')
    config.add_static_view('css', 'baby_tracker:static/css')
    config.add_static_view('img', 'baby_tracker:static/img')
    config.add_static_view('vendor', 'baby_tracker:static/vendor')
