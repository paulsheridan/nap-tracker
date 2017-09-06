import unittest
import transaction
import datetime

from pyramid import testing


def dummy_request(dbsession):
    return testing.DummyRequest(dbsession=dbsession)


class BaseTest(unittest.TestCase):
    def setUp(self):
        from ..models import get_tm_session
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('..models')
        self.config.include('..routes')

        session_factory = self.config.registry['dbsession_factory']
        self.session = get_tm_session(session_factory, transaction.manager)

        self.init_database()

    def init_database(self):
        from ..models.meta import Base
        session_factory = self.config.registry['dbsession_factory']
        engine = session_factory.kw['bind']
        Base.metadata.create_all(engine)

    def tearDown(self):
        testing.tearDown()
        transaction.abort()

    def makeUser(self, email, password='dummy'):
        from ..models import User
        user = User(email=email)
        user.hash_password(password)
        return user

    def makeNap(self, user):
        from ..models import Nap
        return Nap(end=datetime.datetime.utcnow() + datetime.timedelta(hours=1), user_id=user.id)

    def makeMeal(self):
        from ..models import Meal
        return Meal()



class GetNapTests(BaseTest):
    def test_get(self):
        from ..views import get_naps
        user = self.makeUser(email='dummy@user.com')
        self.session.add(user)
        self.session.flush()
        nap = self.makeNap(user=user)
        self.session.add(nap)
