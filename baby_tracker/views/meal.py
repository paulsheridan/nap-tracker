# import datetime
# import transaction
# import pyramid.httpexceptions as exc
#
# from sqlalchemy import Date, cast
#
# from baby_tracker.models import Meal, User
#
# from pyramid.view import (
# view_config,
# view_defaults
# )
#
#
# @view_defaults(renderer='json')
# class MealView(object):
#
#     def __init__(self, request):
#         self.request = request
#         self.logged_in = request.authenticated_userid
#
#     @view_config(route_name='meals_wildcard', request_method='GET')
#     def get_meals(self):
#         """Returns list of all meals by user"""
#         if not self.logged_in:
#             return exc.HTTPForbidden()
#         meals = self.request.dbsession.query(User).filter_by(id=self.logged_in).first().meals
#         meals_json = [meal.to_json() for meal in meals]
#         return meals_json
#
#     @view_config(route_name='meals_wildcard', request_method='POST')
#     def post_meal(self):
#         """Add single meal"""
#         if not self.logged_in:
#             return exc.HTTPForbidden()
#         meal_json = self.request.json
#         meal = Meal.from_json(meal_json)
#         meal.user_id = self.logged_in
#         self.request.dbsession.add(meal)
#         self.request.dbsession.flush()
#         return {'id': meal.id}
#
#     @view_config(route_name='meals', request_method='GET')
#     def get_meal(self):
#         """Return a single meal."""
#         if not self.logged_in:
#             return exc.HTTPForbidden()
#         meal_id = int(self.request.matchdict['id'])
#         meal = self.request.dbsession.query(User).filter_by(
#             id=self.logged_in).first().meals.filter_by(id=meal_id).first()
#         if not meal:
#             return exc.HTTPNotFound()
#         return meal.to_json()
#
#     @view_config(route_name='meals', request_method='PUT')
#     def put_meal(self):
#         """Update a single meal entry"""
#         if not self.logged_in:
#             return exc.HTTPForbidden()
#         meal_id = int(self.request.matchdict['id'])
#         meal = self.request.dbsession.query(User).filter_by(
#             id=self.logged_in).first().meals.filter_by(id=meal_id).first()
#         if meal is not None:
#             args = self.request.json
#             for key, value in args.items():
#                 if args[key] is not None:
#                     setattr(meal, key, value)
#             transaction.commit()
#             return meal.to_json()
#         raise exc.HTTPNotFound()
#
#     @view_config(route_name='meals', request_method='DELETE')
#     def delete_meal(self):
#         """Delete a single meal entry"""
#         meal_id = int(self.request.matchdict['id'])
#         meal = self.request.dbsession.query(User).filter_by(
#             id=self.logged_in).first().meals.filter_by(id=meal_id).delete()
#         if not meal:
#             return exc.HTTPNotFound()
#         return {'status': 'OK'}
#
#     @view_config(route_name='meals_today', request_method='GET')
#     def meals_today(self):
#         """Return today's meals by user."""
#         if not self.logged_in:
#             return exc.HTTPForbidden()
#         meals = self.request.dbsession.query(User).filter_by(
#             id=self.logged_in).first().meals.filter(cast(Meal.time, Date) == datetime.datetime.utcnow().date())
#         meals_json = [meal.to_json() for meal in meals]
#         return meals_json
