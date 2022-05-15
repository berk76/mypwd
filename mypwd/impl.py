import json
import os
import subprocess
from mypwd.mypwd_error import MyPwdError


CONFIG_FILENAME = "mypwd.conf"
CONFIG_EMAIL_KEY = "email"
VAULT_FILENAME = "mypwd.json"
LOGIN_KEY = "login"
PASSWORD_KEY = "password"
PWD_TEMPLATE = dict()
ENCRYPTED = False

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


def get_home_dir() -> str:
    return os.getenv("HOME") if os.getenv("HOME") is not None else os.getenv("HOMEPATH")


def get_vault_path() -> str:
    home_dir = get_home_dir()
    vault_file = os.path.join(home_dir, VAULT_FILENAME)
    return vault_file


def get_config_path() -> str:
    home_dir = get_home_dir()
    vault_file = os.path.join(home_dir, CONFIG_FILENAME)
    return vault_file


def load_config() -> dict:
    config_file = get_config_path()

    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            return json.load(f)
    return dict()


def save_config(config: dict) -> None:
    config_file = get_config_path()
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)


def load_vault() -> dict:
    global ENCRYPTED
    vault_file = get_vault_path()

    if os.path.exists(vault_file):
        ENCRYPTED = False
        with open(vault_file, "r") as f:
            return json.load(f)

    if os.path.exists("%s.gpg" % vault_file):
        ENCRYPTED = True
        import subprocess
        result = subprocess.run(['gpg', '--quiet', '--decrypt', "%s.gpg" % vault_file], stdout=subprocess.PIPE)
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            raise MyPwdError('Unable to decrypt file "%s.gpg".' % get_vault_path())

    ENCRYPTED = False
    vault = PWD_TEMPLATE.copy()
    save_vault(vault)
    return vault


def save_vault(vault: dict) -> None:
    vault_file = get_vault_path()
    with open(vault_file, "w") as f:
        json.dump(vault, f, indent=2)

    if ENCRYPTED:
        config = load_config()

        email = None
        use_saved_mail = None
        if CONFIG_EMAIL_KEY in config:
            email = config[CONFIG_EMAIL_KEY]
            use_saved_mail = input("Do you want to use %s key? (y/n): " % email)

        if email is None or use_saved_mail != "y":
            email = input("Provide e-mail of your private key: ")

        encrypt_vault(email)


def decrypt_vault() -> None:
    print("decrypting vault...")
    pwd_file = get_vault_path()
    gpg_file = "%s.gpg" % pwd_file

    if os.path.exists(pwd_file):
        print("Error: File %s already exists." % pwd_file)
        exit(1)

    if not os.path.exists(gpg_file):
        print("Error: File %s doesn't exist." % gpg_file)
        exit(1)

    result = subprocess.run(
        ['gpg', '--quiet', '--output', pwd_file, '--decrypt', gpg_file],
        stdout=subprocess.PIPE
    )
    if result.returncode == 0:
        print("Decrypted: %s" % pwd_file)
    else:
        raise MyPwdError('Unable to decrypt file "%s".' % gpg_file)


def encrypt_vault(email: str) -> None:
    print("encrypting vault...")
    pwd_file = get_vault_path()
    gpg_file = "%s.gpg" % pwd_file
    bak_file = "%s.gpg.bak" % pwd_file

    if not os.path.exists(pwd_file):
        print("Error: File %s doesn't exist." % pwd_file)
        exit(1)

    validate_vault_file(pwd_file)

    # remove and backup old vault
    if os.path.exists(gpg_file):
        if os.path.exists(bak_file):
            os.remove(bak_file)
        os.rename(gpg_file, bak_file)

    result = subprocess.run(
        ['gpg', '--quiet', '--armor', '--trust-model',
            'always', '--output', gpg_file, '--encrypt',
            "--recipient", email, pwd_file],
        stdout=subprocess.PIPE
    )
    if result.returncode == 0:
        print("Encrypted: %s" % gpg_file)
        os.remove(pwd_file)
    else:
        raise MyPwdError('Unable to encrypt file "%s".' % pwd_file)

    config = load_config()
    config[CONFIG_EMAIL_KEY] = email
    save_config(config)
