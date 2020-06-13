import unittest

from database.dbelasticsearch import DbElasticsearch

class TestDbFunctions(unittest.TestCase):
    def setUp(self):
        self.db = DbElasticsearch()
        self.db.create('dbtest')
        
        self.id = 0
        pass

    def tearDown(self):
        ret = self.db.query_all('dbtest')
        for r in ret:
            self.db.delete('dbtest', r['_id'])

        pass
        
        
    def test_insert_delete(self):
        id = self.db.insert('dbtest', {'ID': 1})
        ret = self.db.query_id('dbtest', id)
        self.assertEqual(ret['ID'], 1)
        
        self.db.delete('dbtest', id)
        ret = self.db.query_id('dbtest', id)
        self.assertTrue(ret is None)

    def test_update(self):

        self.id = self.db.insert('dbtest', {'ID': 1, 'ID2': 2}, self.id)
        ret = self.db.query_id('dbtest', self.id)
        self.assertEqual(ret['ID'], 1)
        self.assertEqual(ret['ID2'], 2)        
        
        ret = self.db.update('dbtest', self.id, {'ID': 2})
        ret = self.db.query_id('dbtest', self.id)
        self.assertEqual(ret['ID'], 2)
        self.assertEqual(ret['ID2'], 2)
        
        self.db.delete('dbtest', self.id)

    def test_delete(self):
        self.id = self.db.insert('dbtest', {'ID': 1, 'ID2': 2}, self.id)
        
        self.assertTrue(self.db.delete('dbtest', self.id))
        self.assertFalse(self.db.delete('dbtest', self.id))

    def test_query_all(self):
        ret = self.db.query_all('dbtest')

        count = len(ret)
        self.db.insert('dbtest', {'ID': 1, 'ID2': 3})
        self.db.insert('dbtest', {'ID': 1, 'ID2': 3})
        ret = self.db.query_all('dbtest')
        self.assertEqual(len(ret), count + 2)

    def test_query(self):
        ret = self.db.query('dbtest', {'ID2': 3})

        count = len(ret)
        self.db.insert('dbtest', {'ID': 1, 'ID2': 3})
        self.db.insert('dbtest', {'ID': 1, 'ID2': 3})
        ret = self.db.query('dbtest', {'ID2': 3})
        self.assertEqual(len(ret), count + 2)

    def test_delete_all(self):
        ret = self.db.query_all('dbtest')
        for r in ret:
            self.db.delete('dbtest', r['_id'])
            
        ret = self.db.query_all('dbtest')
        self.assertEqual(len(ret), 0)


if __name__ == '__main__':
    import sys
    
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDbFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)