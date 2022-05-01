import argparse
import mypwd.impl as impl
import os
import subprocess
from mypwd.mypwd_error import MyPwdError


def decrypt(args) -> None:
    print("decrypting...")
    pwd_file = impl.get_vault_path()
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


def encrypt(args) -> None:
    print("encrypting...")
    pwd_file = impl.get_vault_path()
    gpg_file = "%s.gpg" % pwd_file
    bak_file = "%s.gpg.bak" % pwd_file

    if not os.path.exists(pwd_file):
        print("Error: File %s doesn't exist." % pwd_file)
        exit(1)

    impl.validate_vault_file(pwd_file)

    # remove and backup old vault
    if os.path.exists(gpg_file):
        if os.path.exists(bak_file):
            os.remove(bak_file)
        os.rename(gpg_file, bak_file)

    result = subprocess.run(
        ['gpg', '--quiet', '--armor', '--output', gpg_file, '--encrypt', "--recipient", args.email, pwd_file],
        stdout=subprocess.PIPE
    )
    if result.returncode == 0:
        print("Encrypted: %s" % gpg_file)
        os.remove(pwd_file)
    else:
        raise MyPwdError('Unable to encrypt file "%s".' % pwd_file)


def main():
    impl.check_if_gpg_is_installed()

    parser = argparse.ArgumentParser(description="MyPwd - Python password manager")
    subparsers = parser.add_subparsers(title="Subcommands")

    # decrypt
    parser_d = subparsers.add_parser('decrypt', help='Decrypt vault file.')
    parser_d.set_defaults(func=decrypt)

    # encrypt
    parser_e = subparsers.add_parser('encrypt', help='Encrypt vault file.')
    parser_e.add_argument(
        '-e', '--email', type=str, required=True,
        help='Encrypt vault file with public key identified by e-mail.'
    )
    parser_e.set_defaults(func=encrypt)

    args = parser.parse_args()
    if "func" in args:
        args.func(args)
    else:
        parser.print_usage()
