from meniscus.app import bootstrap_api
#import meniscus.app
from mock import MagicMock
from mock import patch
import unittest


class TestingApIBootstrap(unittest.TestCase):
    def setUp(self):
        self.cache = MagicMock()
        self.cache.cache_exists.return_value = True
        self.cache.cache_get.return_value = \
            {'personality_module': 'meniscus.personas.worker.pairing'}
        self.no_cache = MagicMock()
        self.no_cache.cache_exists.return_value = False

    def test_should_return_personality_from_cache(self):
        with patch('meniscus.app.cache', self.cache):
            application = bootstrap_api()

    def test_should_return_default_personality_module_when_no_cache(self):
        with patch('meniscus.app.cache', self.cache):
            application = bootstrap_api()


if __name__ == '__main__':
    unittest.main()
