import unittest

import pylib.configuration.configuration as cfg

class TestDbFunctions(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass
        

    def cfg_assert(self, _type, var, value, error):
        cfg.clear('TEST', var, _type)
        cfg.set('TEST', var, value)
        self.assertEqual(cfg.get('TEST', var, _type), value)
        cfg.clear('TEST', var, _type)
        self.assertEqual(cfg.get('TEST', var, _type), error)

    def cfg_assert_default(self, _type, var, value, default):
        cfg.clear('TEST', var, _type)
        self.assertEqual(cfg.get('TEST', var, _type, default), default)


    def test_cfg_int(self):
        self.cfg_assert(cfg.INT, 'I', 567, None)

    def test_cfg_str(self):
        self.cfg_assert(cfg.STR, 'S', 'STR_NONE', None)

    def test_cfg_list(self):
        self.cfg_assert(cfg.LIST, 'D', ['3', 'S1', '1', 'S2'], [])

    def test_cfg_dict(self):
        self.cfg_assert(cfg.DICT, 'I', {'1':'S1', '2': 'S2'}, {})

    def test_cfg_int_default(self):
        self.cfg_assert_default(cfg.INT, 'ID', 567, 200)

    def test_cfg_str_default(self):
        self.cfg_assert_default(cfg.STR, 'SD', 'STR_NONE', 'STR')


if __name__ == '__main__':
    import sys
    
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDbFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)