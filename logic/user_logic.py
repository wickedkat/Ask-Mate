from typing import Any, Union

import data_manager as dm
from auth import password_manager as pm


def check_exist_user(username):
    user_exist: object = dm.get_one_user(username)
    if user_exist:
        return user_exist
    return False


def hash_password(password):
    hash_pass = pm.hash_password(password)
    return hash_pass


def add_new_user(user):
    username = user['username']
    if not check_exist_user(username):
        dm.add_one_user(user)
        return True
    return False


def check_pass(login_user):
    username = login_user['username']
    pass_from_form = login_user['password']
    user_from_base = check_exist_user(username)
    if user_from_base:
        pass_from_base = user_from_base['password']
        verify = pm.verify_password(pass_from_form, pass_from_base)
        if verify:
            return True
    return False


def get_user(username):
    if check_exist_user(username):
        return dm.get_one_user(username)
    return []