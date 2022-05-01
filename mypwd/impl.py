import json
import os
import subprocess
from mypwd.mypwd_error import MyPwdError


FILENAME = "mypwd.json"
LOGIN_KEY = "login"
PASSWORD_KEY = "password"
PWD_TEMPLATE = {
                    "postgres": {
                        LOGIN_KEY: "john",
                        PASSWORD_KEY: "myPa$$w0rd",
                        "note": "Valid until end of month"
                    },
                    "mongo": {
                        LOGIN_KEY: "admin",
                        PASSWORD_KEY: "myPa$$w0rd2"
                    }
                }


def check_if_gpg_is_installed(args) -> None:
    result = subprocess.run(["gpg", "--help"], stdout=subprocess.PIPE)
    if result.returncode != 0:
        raise MyPwdError("Error: gpg is not installed.")


def get_vault_path() -> str:
    home_dir = os.getenv("HOME") if os.getenv("HOME") is not None else os.getenv("HOMEPATH")
    pwd_file = os.path.join(home_dir, FILENAME)
    return pwd_file


def get_entry(d: dict, entry: str) -> dict:
    if entry not in d:
        raise MyPwdError('Account "%s" is missing in your "%s" file.' % (entry, get_vault_path()))
    return d[entry]


def get_entry_from_dict(entry: str) -> dict:
    pwd_file = get_vault_path()

    if os.path.exists(pwd_file):
        with open(pwd_file, "r") as f:
            pwd = json.load(f)
        return get_entry(pwd, entry)

    if os.path.exists("%s.gpg" % pwd_file):
        import subprocess
        result = subprocess.run(['gpg', '--quiet', '--decrypt', "%s.gpg" % pwd_file], stdout=subprocess.PIPE)
        if result.returncode == 0:
            pwd = json.loads(result.stdout)
        else:
            raise MyPwdError('Unable to decrypt file "%s.gpg".' % get_vault_path())
        return get_entry(pwd, entry)

    pwd = PWD_TEMPLATE.copy()
    with open(pwd_file, "w") as f:
        json.dump(pwd, f, indent=2)
    return get_entry(pwd, entry)
