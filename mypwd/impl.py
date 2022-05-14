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


def check_if_gpg_is_installed() -> None:
    cmd = "gpg"
    try:
        subprocess.run([cmd, "--help"], stdout=subprocess.PIPE)
    except FileNotFoundError:
        print("Error: %s is not installed." % cmd)
        exit(1)


def validate_vault_file(vault_file: str) -> None:
    try:
        with open(vault_file, "r") as f:
            json.load(f)
    except json.decoder.JSONDecodeError as ex:
        print("Error: Content of %s is not valid json:" % vault_file)
        print("%s: line %s" % (ex.msg, ex.lineno))
        exit(1)


def get_vault_path() -> str:
    home_dir = os.getenv("HOME") if os.getenv("HOME") is not None else os.getenv("HOMEPATH")
    vault_file = os.path.join(home_dir, FILENAME)
    return vault_file


def get_vault() -> dict:
    vault_file = get_vault_path()

    if os.path.exists(vault_file):
        with open(vault_file, "r") as f:
            return json.load(f)

    if os.path.exists("%s.gpg" % vault_file):
        import subprocess
        result = subprocess.run(['gpg', '--quiet', '--decrypt', "%s.gpg" % vault_file], stdout=subprocess.PIPE)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            raise MyPwdError('Unable to decrypt file "%s.gpg".' % get_vault_path())

    vault = PWD_TEMPLATE.copy()
    save_vault(vault)
    return vault


def save_vault(vault: dict) -> None:
    vault_file = get_vault_path()
    with open(vault_file, "w") as f:
        json.dump(vault, f, indent=2)
