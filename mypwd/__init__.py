import json
import os
from mypwd.mypwd_error import MyPwdError


filename = "mypwd.json"
login_key = "login"
password_key = "password"
pwd_template = {
                    "postgres": {
                        login_key: "john",
                        password_key: "myPa$$w0rd",
                        "note": "Valid until end of month"
                    },
                    "mongo": {
                        login_key: "admin",
                        password_key: "myPa$$w0rd2"
                    }
                }


def get_values(entry: str, keys: list) -> list:
    result = []
    pwd = __get_entry_from_dict__(entry)
    for key in keys:
        if key not in pwd:
            raise MyPwdError('Key "%s" is missing in account "%s" in your "%s" file.' % (key, entry, __get_path__()))
        result.append(pwd[key])
    return result


def get_login_password(entry: str) -> list:
    return get_values(entry, [login_key, password_key])


def get_value(entry: str, key: str) -> str:
    return get_values(entry, [key])[0]


def get_login(entry: str) -> str:
    return get_value(entry, login_key)


def get_pwd(entry: str) -> str:
    return get_value(entry, password_key)


def __get_path__() -> str:
    home_dir = os.getenv("HOME") if os.getenv("HOME") is not None else os.getenv("HOMEPATH")
    pwd_file = os.path.join(home_dir, filename)
    return pwd_file


def __get_entry__(d: dict, entry: str) -> dict:
    if entry not in d:
        raise MyPwdError('Account "%s" is missing in your "%s" file.' % (entry, __get_path__()))
    return d[entry]


def __get_entry_from_dict__(entry: str) -> dict:
    pwd_file = __get_path__()

    if os.path.exists(pwd_file):
        with open(pwd_file, "r") as f:
            pwd = json.load(f)
        return __get_entry__(pwd, entry)

    if os.path.exists("%s.gpg" % pwd_file):
        import subprocess
        result = subprocess.run(['gpg', '--quiet', '--decrypt', "%s.gpg" % pwd_file], stdout=subprocess.PIPE)
        if result.returncode == 0:
            pwd = json.loads(result.stdout)
        else:
            raise MyPwdError('Unable to decrypt file "%s.gpg".' % __get_path__())
        return __get_entry__(pwd, entry)

    pwd = pwd_template.copy()
    with open(pwd_file, "w") as f:
        json.dump(pwd, f, indent=2)
    return __get_entry__(pwd, entry)
