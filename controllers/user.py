from services.security import hash_password
from repositories import user

def create_user(first_name: str, last_name: str, username: str, password: str, is_admin: bool = False):
    hashed_password = hash_password(password)
    return user.create_user(first_name, last_name, username, hashed_password, is_admin)

def list_users():
    return user.list_users()
