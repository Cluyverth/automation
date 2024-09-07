import unittest
import os
from config.settings import load_config, get_db_config, get_env_variable

class TestConfigFunctions(unittest.TestCase):
    
    def test_load_config(self):
        config = load_config()
        self.assertIn('db_test', config)
        self.assertIn('server', config['db_test'])
        self.assertIn('database', config['db_test'])
    
    def test_get_db_config(self):
        db_config = get_db_config('db_test')
        self.assertIsNotNone(db_config['server'])
        self.assertIsNotNone(db_config['database'])
        self.assertEqual(db_config['server'], 'server_name_test')
        self.assertEqual(db_config['database'], 'database_name_test')
    
    def test_get_env_variable(self):
        os.environ['TEST_VARIABLE'] = 'test_value'
        self.assertEqual(get_env_variable('TEST_VARIABLE'), 'test_value')
        
if __name__=='__main__':
    unittest.main()