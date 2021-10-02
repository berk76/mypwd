import json
import os

filename = "mypwd.json"
pwd = {"mypass":{"password":"myPa$$w0rd"}, "mypass2":{"password":"myPa$$w0rd2"}}


def getpwd(key: str) -> str:
    return pwd[key]["password"]


home_dir = os.getenv("HOME") if os.getenv("HOME") is not None else os.getenv("HOMEPATH")
pwd_file = os.path.join(home_dir, filename)

if os.path.exists(pwd_file):
    with open(pwd_file, "r") as f:
        pwd = json.load(f)
else:
    with open(pwd_file, "w") as f:
        json.dump(pwd, f, indent=2)
