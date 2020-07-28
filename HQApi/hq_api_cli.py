import argparse

from HQApi import HQApi


def fetch(args):
    api = HQApi(login_token=args.login_token, token=args.token)
    print(api.fetch(method=args.method, func=args.function, data=args.data))


def main(args=None):
    parser = argparse.ArgumentParser(prog='HQApi', description='Command line interface for HQApi')
    parser.add_argument(
        '--token', help='JWT token'
    )
    parser.add_argument(
        '--login_token', help='Login token'
    )
    parser.add_argument(
        '--method', help='Method', default="GET"
    )
    parser.add_argument(
        '--function', help='Function', default="shows/now"
    )
    parser.add_argument(
        '--data', help='POST data', default=None
    )
    args = parser.parse_args(args)
    fetch(args)
