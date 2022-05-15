# Very simple password vault for Python projects.

I often forgot the passwords in my scripts and committed them to the repository. So I created a simple password vault so that it doesn't happen to me anymore.

## 1. Usage

### 1.1 Basic setup and usage

Install `mypwd` module.

```
pip install mypwd
```

Now you can use `mypwd` your project:

```python
import mypwd

login, password, server = mypwd.get_values("mongo-dev", ["login", "password", "server"])

uri = f"mongodb://{login}:{password}@{server}/admin?retryWrites=true&w=majority"
```

When you run it first time `mypwd` creates vault in your `$HOME` directory and will ask you for login, password and server of your mongo-dev entry and store it in your vault `$HOME/mypwd.json`.

Here is an example of vault content:

```json
{
  "mongo-uat": {
    "login": "appl",
    "password": "hS78#pbTgc#J.CQL",
    "server": "myserver-uat.com"
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

### 1.2 Keep your passwords safe and encrypt mypwd.json with GPG

You should store your passwords in encrypted file `mypwd.json.gpg` instead of in plain text file `mypwd.json`.

1. install GPG (if you are using GitBash probably you already have gpg installed)
1. create key-pair `gpg --gen-key` and assign it to your e-mail

Now you can encrypt your `mypwd.json` with your gpg key:
```
mypwd encrypt -e your.email@something.com
```

and later on you can decrypt it back for some manual modification:
```
mypwd decrypt
```

## 2. Installation

Installation is simple:

```
pip install mypwd
```

or

```
python setup.py install
```

## 3. Contribution

Feel free create issue or pull request.
