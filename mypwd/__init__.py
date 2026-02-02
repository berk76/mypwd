import mypwd.impl as impl
import importlib.metadata
import tomllib  # Python 3.11+, use tomli for older versions
from mypwd.mypwd_error import MyPwdError


def get_version():
    try:
        return importlib.metadata.metadata('mypwd')['Version']
    except (importlib.metadata.PackageNotFoundError, KeyError):
        try:
            with open("pyproject.toml", "rb") as f:
                pyproject_data = tomllib.load(f)
            return pyproject_data["project"]["version"]
        except Exception:
            return "unknown"


__version__ = get_version()


def get_values(entry: str, keys: list) -> list:
    result = []
    vault_modified = False

    vault = impl.load_vault()
    if entry not in vault:
        print(f"Warning: '{entry}' entry is missing in vault: {impl.get_vault_path()}")
        answer = input("Would you like to add it into your vault? (y/n): ")
        if answer == "y":
            vault[entry] = {}
            vault_modified = True
        else:
            raise MyPwdError(f'Entry "{entry}" is missing in your "{impl.get_vault_path()}" vault.')

    for key in keys:
        if key not in vault[entry]:
            # raise MyPwdError('Key "%s" is missing in account "%s" in your "%s" file.' % (key, entry, impl.get_vault_path()))
            answer = input(f"{entry} -> {key}: ")
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
