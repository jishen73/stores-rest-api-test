from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    """
    This resource allows users to register by sending a
    POST request with their username and password
    """
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank.")
    
    def post(self):
        data = UserRegister.parser.parse_args()
        
        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with that username already exists'}, 400
        
        user = UserModel(**data)
        user.save_to_db()
        
        return {'message': 'User created successfully.'}, 201


class UserDelete(Resource):
    def delete(self, username):
        user = UserModel.find_by_username(username)
        
        if user:
            user.delete_from_db()
            return {'message': 'User deleted'}, 200
        return {'message': 'User not found'}, 404
        
        # data = UserRegister.parser.parse_args()
        
        # print("###", data, "###")
        # print(f"### {data['username']} ###")
        
        # if not UserModel.find_by_username(data['username']):
        #     return {'message': 'User not found'}, 404
        
        # user = UserModel(**data)
        # user.delete_from_db()
        
        # return {'message': 'User deleted'}, 200
        