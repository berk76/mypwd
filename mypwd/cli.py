import argparse
import subprocess
from mypwd.mypwd_error import MyPwdError


def check_if_gpg_is_installed() -> None:
    result = subprocess.run(["gpg", "--help"], stdout=subprocess.PIPE)
    if result.returncode != 0:
        raise MyPwdError("Error: gpg is not installed.")


def main():
    check_if_gpg_is_installed()
    parser = argparse.ArgumentParser(description="MyPwd: python password manager")
    parser.add_argument("-d", "--decrypt", action='store_true', help="Decrypt vault file")
    parser.add_argument("-e", "--encrypt", action='store_true', help="Encrypt vault file")
    args = parser.parse_args()
