import unittest

import pylib.configuration.configuration as cfg

class TestDbFunctions(unittest.TestCase):
    def setUp(self):
        self.dbname = 'TEST'
        pass


    def tearDown(self):
        pass
        

    def cfg_assert(self, func_get, var, value, error):
        cfg.clear(self.dbname, var)
        cfg.set(self.dbname, var, value)
        ret = func_get(self.dbname, var)
        self.assertEqual(ret, value)
        cfg.clear(self.dbname, var)
        ret = func_get(self.dbname, var)
        self.assertEqual(ret, error)


    def cfg_assert_default(self, func_get, var, value, default):
        cfg.clear(self.dbname, var)
        self.assertEqual(func_get(self.dbname, var, default), default)


    def test_cfg_int(self):
        self.cfg_assert(cfg.get_int, 'I', 567, 0)


    def test_cfg_str(self):
        self.cfg_assert(cfg.get_str, 'S', 'STR_NONE', '')


    def test_cfg_list(self):
        self.cfg_assert(cfg.get_list, 'D', ['3', 'S1', '1', 'S2'], [])


    def test_cfg_dict(self):
        self.cfg_assert(cfg.get_dict, 'I', {'1':'S1', '2': 'S2'}, {})


    def test_cfg_int_default(self):
        self.cfg_assert_default(cfg.get_int, 'ID', 567, 200)


    def test_cfg_str_default(self):
        self.cfg_assert_default(cfg.get_str, 'SD', 'STR_NONE', 'STR')


if __name__ == '__main__':
    import sys
    
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDbFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)
