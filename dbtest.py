import unittest

from pylib.database.dbelasticsearch import DbElasticsearch
from pylib.database.dbdummy import DbDummy

class TestDbFunctions(unittest.TestCase):
    def setUp(self):
        #self.db = DbElasticsearch()
        self.db = DbDummy()
        self.db.create('dbtest')
        
        
        pass

    def tearDown(self):
        ret = self.db.query('dbtest')
        for r in ret:
            self.db.delete('dbtest', r['_id'])

        pass
        

    def test_insert_by_id(self):
        tid = 'DB0000001'
        id = self.db.insert('dbtest', {'ID': 1}, tid)
        self.assertEqual(id, tid)
        


    def test_insert(self):
        id = self.db.insert('dbtest', {'ID': 1})
        ret = self.db.query_id('dbtest', id)
        self.assertEqual(ret['ID'], 1)
        

    def test_update(self):

        id = self.db.insert('dbtest', {'ID': 1, 'ID2': 2})
        ret = self.db.query_id('dbtest', id)
        self.assertEqual(ret['ID'], 1)
        self.assertEqual(ret['ID2'], 2)        
        
        ret = self.db.update('dbtest', id, {'ID': 2})
        ret = self.db.query_id('dbtest', id)
        self.assertEqual(ret['ID'], 2)
        self.assertEqual(ret['ID2'], 2)

        ret = self.db.update('dbtest', id, {'ID3': 3})
        ret = self.db.query_id('dbtest', id)
        self.assertEqual(ret['ID'], 2)
        self.assertEqual(ret['ID2'], 2)
        self.assertEqual(ret['ID3'], 3)


    def test_delete(self):
        id = self.db.insert('dbtest', {'ID': 1, 'ID2': 2})
        
        self.assertTrue(self.db.delete('dbtest', id))
        self.assertFalse(self.db.delete('dbtest', id))


    def test_query_all(self):
        ret = self.db.query('dbtest')

        count = len(ret)
        self.db.insert('dbtest', {'ID': 1, 'ID2': 3})
        self.db.insert('dbtest', {'ID': 1, 'ID2': 3})
        ret = self.db.query('dbtest')
        self.assertEqual(len(ret), count + 2)

    def test_query(self):
        ret = self.db.query('dbtest', {'ID2': 3})

        count = len(ret)
        self.db.insert('dbtest', {'ID': 1, 'ID2': 3})
        self.db.insert('dbtest', {'ID': 1, 'ID2': 3})
        ret = self.db.query('dbtest', {'ID2': 3})
        self.assertEqual(len(ret), count + 2)

    def test_query2(self):
        self.db.insert('dbtest', {'ID': 520, 'ID_list': {'ID2': 2, 'ID3': 3}})
        
        ret = self.db.query('dbtest', {'ID_list.ID2': 2})
        
        self.assertEqual(ret[0]['ID'], 520)
        

    def test_delete_all(self):
        ret = self.db.query('dbtest')
        for r in ret:
            self.db.delete('dbtest', r['_id'])
            
        ret = self.db.query('dbtest')
        self.assertEqual(len(ret), 0)


if __name__ == '__main__':
    import sys
    
    suite = unittest.TestSuite()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDbFunctions)
    unittest.TextTestRunner(verbosity=2).run(suite)