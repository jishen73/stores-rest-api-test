import json
from unittest import skip

from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                resp = client.post('/store/TestStore')
                
                self.assertEqual(resp.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('TestStore'))
                self.assertDictEqual({'id': 1, 'name': 'TestStore', 'items': []},
                                     json.loads(resp.data))
        
    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/TestStore')
                resp = client.post('/store/TestStore')
                
                self.assertEqual(resp.status_code, 400)
    
    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                # resp = client.post('/store/TestStore')
                StoreModel('TestStore').save_to_db()
                resp = client.delete('/store/TestStore')
                
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Store deleted'},
                                    json.loads(resp.data))
                self.assertIsNone(StoreModel.find_by_name('TestStore'))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('TestStore').save_to_db()
                resp = client.get('/store/TestStore')
                
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': 'TestStore', 'items': []},
                                    json.loads(resp.data))

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/store/TestStore')
                
                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual({'message': 'Store not found'},
                                    json.loads(resp.data))
    
    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('TestStore').save_to_db()
                ItemModel('TestItem', 19.99, 1).save_to_db()
                
                resp = client.get('/store/TestStore')
                
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'id': 1, 'name': 'TestStore', 'items': [{'name': 'TestItem', 'price': 19.99}]},
                                    json.loads(resp.data))

    # @skip('not yet implemented')
    def test_store_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('TestStore').save_to_db()
                resp = client.get('/stores')
                
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'TestStore', 'items': []}]},
                                    json.loads(resp.data))

    # @skip('not yet implemented')
    def test_store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('TestStore').save_to_db()
                ItemModel('TestItem', 19.99, 1).save_to_db()
                resp = client.get('/stores')
                
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'stores': [{'id': 1, 'name': 'TestStore', 'items': [{'name': 'TestItem', 'price': 19.99}]}]},
                                    json.loads(resp.data))
            resp = client.post('/store/TestStore')
