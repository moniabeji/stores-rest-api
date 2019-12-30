from werkzeug.security import safe_str_cmp
from models.user import UserModel


def authenticate(username, password):
    user = UserModel.find_by_username(username)

    if user and safe_str_cmp(user.password, password):
        return user

def identify(payload):
    print(payload)
    user_id = payload['identity']

    return UserModel.find_by_id(user_id)


#to authenticate an sent you the jwt token u have to use the nale that exist in th database