from argparse import ArgumentParser

from jira.client import JIRA


def read_file(file_path):
    with open(file_path) as f:
        return f.read()


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('--jira-server', required=True, help='jira server in form of http://jira.url/jira')
    parser.add_argument('--token', required=True, help='oauth token')
    parser.add_argument('--token-secret', required=True, help='oauth token secret')
    parser.add_argument('--consumer-key', default='hardcoded-consumer', help='oauth token')
    parser.add_argument('--rsa-path', default="rsa.pem", help='oauth token')
    return parser.parse_args()


def main():
    args = parse_arguments()

    rsa_key = read_file(args.rsa_path)
    jira = JIRA(
        options={
            'server': args.jira_server
        },
        oauth={
            'access_token': args.token,
            'access_token_secret': args.token_secret,
            'consumer_key': args.consumer_key,
            'key_cert': rsa_key
        }
    )

    for project in jira.projects():
        print(project.key)


if __name__ == '__main__':
    main()
