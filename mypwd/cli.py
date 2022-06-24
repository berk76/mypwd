import argparse
import mypwd.impl as impl


def decrypt(args) -> None:
    impl.decrypt_vault()


def encrypt(args) -> None:
    impl.encrypt_vault(args.email)


def list(args):
    v = impl.load_vault()
    for k in v.keys():
        print(k)


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

    # list
    parser_l = subparsers.add_parser('list', help='List entries.')
    parser_l.set_defaults(func=list)

    args = parser.parse_args()
    if "func" in args:
        args.func(args)
    else:
        parser.print_usage()
