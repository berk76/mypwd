import mypwd.impl as impl
from mypwd.mypwd_error import MyPwdError


def get_values(entry: str, keys: list) -> list:
    result = []
    vault_modified = False

    vault = impl.load_vault()
    if entry not in vault:
        print("Warning: '%s' entry is missing in vault: %s" % (entry, impl.get_vault_path()))
        answer = input("Would you like to add it into your vault? (y/n): ")
        if answer == "y":
            vault[entry] = dict()
            vault_modified = True
        else:
            raise MyPwdError('Entry "%s" is missing in your "%s" vault.' % (entry, impl.get_vault_path()))

    for key in keys:
        if key not in vault[entry]:
            # raise MyPwdError('Key "%s" is missing in account "%s" in your "%s" file.' % (key, entry, impl.get_vault_path()))
            answer = input("%s -> %s: " % (entry, key))
            vault[entry][key] = answer
            vault_modified = True
        result.append(vault[entry][key])

    if vault_modified:
        print("Saving vault...")
        impl.save_vault(vault)

    return result


def get_login_password(entry: str) -> list:
    return get_values(entry, [impl.LOGIN_KEY, impl.PASSWORD_KEY])


def get_value(entry: str, key: str) -> str:
    return get_values(entry, [key])[0]


def get_login(entry: str) -> str:
    return get_value(entry, impl.LOGIN_KEY)


def get_pwd(entry: str) -> str:
    return get_value(entry, impl.PASSWORD_KEY)
