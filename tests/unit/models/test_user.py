from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test','pass')
        
        self.assertEqual(user.username, 'test',
                        "The name of the user after creation does not equal the constructor argument.")
        self.assertEqual(user.password, 'pass',
                        "The password of the user after creation does not equal the constructor argument.")
    