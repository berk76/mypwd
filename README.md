# MyPwd

Very simple password manager for my python projects.

I often forgot the passwords in my scripts and committed them to the repository. So I created a simple password manager so that it doesn't happen to me anymore.

## Usage

Create file `mypwd.json` with passwords in your home directory. For example `C:\Users\jarberan\mypwd.json`

```json
{
  "mongo-uat": {
    "login": "appl",
    "password": "hS78#pbTgc#J.CQL",
    "server": "myserver-uat.com",
  },
  "mongo-dev": {
    "login": "appl",
    "password": "VacK>p3k3~t*c~RX",
    "server": "myserver-dev.com",
    "note": "Valid until end of month"
  }
}
```

Now you can access your secrets from python code and you will never commit secret anymore.

```python
import mypwd

login, password, server = mypwd.get_values("mongo-dev", ["login", "password", "server"])

uri = f"mongodb://{login}:{password}@{server}/admin?retryWrites=true&w=majority"
```

### Keep your passwords safe and encrypt mypwd.json with GPG

You should store your passwords in encrypted file `mypwd.json.gpg` instead of in plain text file `mypwd.json`.

1. install GPG (if you are using GitBash you probably have gpg already installed)
1. create key-pair `gpg --gen-key`
1. encrypt your passwords `gpg --output mypwd.json.gpg --encrypt --recipient your@email.com mypwd.json`
1. try to decrypt it `gpg --decrypt mypwd.json.gpg`
1. finally you can remove plain text file `rm mypwd.json` and mypwd will use `mypwd.json.gpg`


## Installation

Installation is simple:

```
pip install mypwd
```

or

```
python setup.py install
```

## Contribution

Feel free create issue or pull request.
