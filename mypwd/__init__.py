import json
import os


filename = "mypwd.json"
login_key = "login"
password_key = "password"
pwd_template = {"mypass":{login_key:"john", password_key:"myPa$$w0rd", "note":"Valid until end of month"}, "mypass2":{login_key:"admin", password_key:"myPa$$w0rd2"}}
pwd = {}


def get_login(entry: str) -> str:
    global login_key 
    global pwd
    return pwd[entry][login_key]


def get_pwd(entry: str) -> str:
    global login_password
    global pwd
    return pwd[entry][password_key]


def get_value(entry: str, key: str) -> str:
    global pwd
    return pwd[entry][key]


def __get_path__() -> str:
    home_dir = os.getenv("HOME") if os.getenv("HOME") is not None else os.getenv("HOMEPATH")
    pwd_file = os.path.join(home_dir, filename)
    return pwd_file


def set_filename(name: str) -> None:
    global filename
    global pwd 
    filename = name
    pwd_file = __get_path__()

    if os.path.exists(pwd_file):
        with open(pwd_file, "r") as f:
            pwd = json.load(f)
    else:
        pwd = pwd_template.copy()
        with open(pwd_file, "w") as f:
            json.dump(pwd, f, indent=2)


set_filename(filename)
