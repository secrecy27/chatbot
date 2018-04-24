import unittest

from programy.security.authenticate.clientidauth import ClientIdAuthenticationService
from programy.config.brain.security import BrainSecurityConfiguration
from programy.bot import Bot
from programy.brain import Brain
from programy.config.bot.bot import BotConfiguration
from programy.config.brain.brain import BrainConfiguration
from programy.context import ClientContext

from programytest.aiml_tests.client import TestClient

class MockClientIdAuthenticationService(ClientIdAuthenticationService):

    def __init__(self, brain_config):
        ClientIdAuthenticationService.__init__(self, brain_config)
        self.should_authorised = False
        self.raise_exception = False

    def user_auth_service(self, context):
        if self.raise_exception is True:
            raise Exception("Bad thing happen!")
        return self.should_authorised

class ClientIdAuthenticationServiceTests(unittest.TestCase):

    def setUp(self):
        self._client_context = ClientContext(TestClient(), "unknown")
        self._client_context.bot = Bot(BotConfiguration())
        self._client_context.bot.configuration.conversations._max_histories = 3
        self._client_context.brain = self._client_context.bot.brain

    def test_init(self):
        service = ClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        self.assertIsNotNone(service)
        self._client_context._userid = "console"
        self.assertTrue(service.authenticate(self._client_context))
        self._client_context._userid = "anyone"
        self.assertFalse(service.authenticate(self._client_context))

    def test_authorise_success(self):
        service = MockClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        service.should_authorised = True
        self.assertTrue("console" in service.authorised)
        self._client_context._userid = "console"
        self.assertTrue(service.authenticate(self._client_context))
        self.assertFalse("unknown" in service.authorised)
        self._client_context._userid = "unknown"
        self.assertTrue(service.authenticate(self._client_context))
        self.assertTrue("unknown" in service.authorised)

    def test_authorise_failure(self):
        service = MockClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        service.should_authorised = False
        self.assertFalse("unknown" in service.authorised)
        self.assertFalse(service.authenticate(self._client_context))

    def test_authorise_exception(self):
        service = MockClientIdAuthenticationService(BrainSecurityConfiguration("authentication"))
        service.should_authorised = True
        service.raise_exception = True
        self.assertFalse(service.authenticate(self._client_context._userid))
