from models.user import UserModel
from tests.base_test import BaseTest
import json


class UserTest(BaseTest):
    def test_register_user(self):
        with self.app() as client:
            with self.app_context():
                request = client.post('/register', data={'username': 'test', 'password': 'pass'})
                
                self.assertEqual(request.status_code, 201)
                self.assertIsNotNone(UserModel.find_by_username('test'))
                self.assertDictEqual({'message': 'User created successfully.'},
                                    json.loads(request.data))
    
    def test_register_and_login(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': 'pass'})
                auth_request = client.post('/auth',
                                          data=json.dumps({'username': 'test', 'password': 'pass'}),
                                          headers={'Content-Type': 'application/json'})
                
                self.assertIn('access_token', json.loads(auth_request.data).keys()) # ['access_token']
    
    def test_register_duplicate_user(self):
        with self.app() as client:
            with self.app_context():
                client.post('/register', data={'username': 'test', 'password': 'pass'})
                response = client.post('/register', data={'username': 'test', 'password': 'pass'})
                
                self.assertEqual(response.status_code, 400)
                self.assertDictEqual({'message': 'A user with that username already exists'},
                                     json.loads(response.data))
    
    def test_delete_invalid_user(self):
        with self.app() as client:
            with self.app_context():
                # pass
                resp = client.delete('/udel/nobody')
                
                self.assertEqual(resp.status_code, 404)
                self.assertDictEqual({'message': 'User not found'},
                                    json.loads(resp.data))
                
    def test_delete_user(self):
        with self.app() as client:
            with self.app_context():
                UserModel('test', 'pass').save_to_db()
                
                resp = client.delete('/udel/test')
                
                self.assertEqual(resp.status_code, 200)
                self.assertDictEqual({'message': 'User deleted'},
                                    json.loads(resp.data))
                