# MyPass

Very simple password manager for my python projects.

I often forgot the passwords in my scripts and committed them to the repository. So I created a simple password manager so that it doesn't happen to me anymore.

## Usage

Create file `mypwd.json` with passwords in your home directory. For example `C:\Users\jarberan\mypwd.json`

```json
{
  "postgres": {
    "password": "myPa$$w0rd"
  },
  "mongo": {
    "password": "mongopass"
  }
}
```

Now you can access your passwords from python code and you will never commit password anymore.

```python
from mypwd import getpwd

login = "jarberan"
password = getpwd("mongo")
uri = f"mongodb://{login}:{password}@myserver.com/admin?retryWrites=true&w=majority"
```

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
