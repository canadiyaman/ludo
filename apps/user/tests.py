from django.contrib.auth.models import AnonymousUser
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import TestCase, RequestFactory

from apps.user.middleware.login_with_ip import LoginMiddleware


class UserMiddlewareTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')
        self.request.user = AnonymousUser()
        SessionMiddleware().process_request(self.request)

    def test_login_with_ip(self):
        test_ip = '100.1.1.1'
        self.request.META['REMOTE_ADDR'] = test_ip
        middleware = LoginMiddleware()
        process_request = middleware.process_request(self.request)
        self.assertIsNone(process_request)
        self.assertEqual(test_ip, self.request.user.ip)

