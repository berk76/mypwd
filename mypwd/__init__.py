import mypwd.impl as impl
from mypwd.mypwd_error import MyPwdError


def get_values(entry: str, keys: list) -> list:
    result = []
    pwd = impl.get_entry_from_dict(entry)
    for key in keys:
        if key not in pwd:
            raise MyPwdError('Key "%s" is missing in account "%s" in your "%s" file.' % (key, entry, impl.get_vault_path()))
        result.append(pwd[key])
    return result


def get_login_password(entry: str) -> list:
    return get_values(entry, [impl.LOGIN_KEY, impl.PASSWORD_KEY])


def get_value(entry: str, key: str) -> str:
    return get_values(entry, [key])[0]


def get_login(entry: str) -> str:
    return get_value(entry, impl.LOGIN_KEY)


def get_pwd(entry: str) -> str:
    return get_value(entry, impl.PASSWORD_KEY)
