from unittest import skip

from models.user import UserModel
from models.item import ItemModel
from models.store import StoreModel
from tests.base_test import BaseTest
import json

class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', 'pass').save_to_db()
                auth_request = client.post('/auth',
                                          data=json.dumps({'username': 'test', 'password': 'pass'}),
                                          headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = 'JWT {}'.format(auth_token)


    # @skip("Not yet implemented")
    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                # auth_request = client.post('/auth',
                #                           data=json.dumps({'username': 'test', 'password': '1234'}),
                #                           headers={'Content-Type': 'application/json'})
                # print("###",auth_request.status_code,"###")
                # print("###",auth_request.data,"###")
                # # auth_token = json.loads(auth_request.data)['access_token']
                # print("###",auth_request.data,"###")
                # self.access_token = 'JWT {}'.format(auth_token)
                # auth_request = client.post('/auth')
                
                resp = client.get('/item/TestItem')
                # print("###",resp.data,"###")
                # print("###",resp.status_code,"###")
                # print("###",resp.headers,"###")
                self.assertEqual(resp.status_code, 401)
                

    # @skip("Not yet implemented")
    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                resp = client.get('/item/TestItem', headers={'Authorization': self.access_token})
                self.assertEqual(resp.status_code, 404)
                
    
    # @skip("Not yet implemented")
    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('TestStore').save_to_db()
                ItemModel('TestItem', 19.99, 1).save_to_db()
                resp = client.get('/item/TestItem', headers={'Authorization': self.access_token})
                
                self.assertEqual(resp.status_code, 200)
    
    # @skip("Not yet implemented")
    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('TestStore').save_to_db()
                ItemModel('TestItem', 19.99, 1).save_to_db()
                resp = client.delete('/item/TestItem', headers={'Authorization': self.access_token})
                
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'Item deleted'},
                                    json.loads(resp.data))
    
    # @skip("Not yet implemented")
    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.post('/item/TestItem', data={'price': 19.99, 'store_id': 1})
                
                self.assertEqual(resp.status_code, 201)
                self.assertDictEqual({'name': 'TestItem', 'price': 19.99},
                                    json.loads(resp.data))

    # @skip("Not yet implemented")
    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('TestItem', 19.99, 1).save_to_db()
                
                resp = client.post('/item/TestItem', data={'price': 19.99, 'store_id': 1})
                
                self.assertEqual(resp.status_code, 400)
                self.assertDictEqual({'message': "An item with name 'TestItem' already exists."},
                                    json.loads(resp.data))    
    # @skip("Not yet implemented")
    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                resp = client.put('/item/TestItem', data={'price': 17.99, 'store_id': 1})
                
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('TestItem').price, 17.99)
                self.assertDictEqual({'name': 'TestItem', 'price': 17.99},
                                    json.loads(resp.data))
    
    # @skip("Not yet implemented")
    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('TestItem', 17.99, 1).save_to_db()
                
                self.assertEqual(ItemModel.find_by_name('TestItem').price, 17.99)
                
                resp = client.put('/item/TestItem', data={'price': 27.99, 'store_id': 1})
                
                self.assertEqual(resp.status_code, 200)
                self.assertEqual(ItemModel.find_by_name('TestItem').price, 27.99)
                self.assertDictEqual({'name': 'TestItem', 'price': 27.99},
                                    json.loads(resp.data))

    # @skip("Not yet implemented")
    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('TestItem', 17.99, 1).save_to_db()
                
                resp = client.get('/items')
                
                self.assertEqual(resp.status_code, 200)
                
                expected = {'items': [{'name': 'TestItem', 'price': 17.99}]}
                
                self.assertDictEqual(expected, json.loads(resp.data))
    
