from argparse import ArgumentParser

from oauthlib.oauth1 import SIGNATURE_RSA
from requests_oauthlib import OAuth1Session

ACCESS_TOKEN_PATH = 'plugins/servlet/oauth/access-token'
AUTHORIZE_PATH = 'plugins/servlet/oauth/authorize'
REQUEST_TOKEN_PATH = 'plugins/servlet/oauth/request-token'
VERIFIER = 'jira_verifier'


def read_file(file_path):
    with open(file_path) as f:
        return f.read()


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('--jira-server', required=True, help='jira server in form of http://jira.url/jira')
    parser.add_argument('--consumer-key', default='hardcoded-consumer', help='oauth token')
    parser.add_argument('--rsa-path', default="rsa.pem", help='oauth token')
    return parser.parse_args()


def main():
    args = parse_arguments()

    rsa_key = read_file(args.rsa_path)

    oauth = OAuth1Session(
        args.consumer_key,
        rsa_key=rsa_key,
        signature_type='auth_header',
        signature_method=SIGNATURE_RSA,
        verifier=VERIFIER
    )

    try:
        request_token = oauth.fetch_request_token("{}/{}".format(args.jira_server, REQUEST_TOKEN_PATH))

        print("Visit link below to approve oauth")
        print("{}/{}?oauth_token={}".format(args.jira_server, AUTHORIZE_PATH, request_token['oauth_token']))

        while raw_input("Press any key to continue after access has been approved..."):
            pass

        access_token = oauth.fetch_access_token("{}/{}".format(args.jira_server, ACCESS_TOKEN_PATH))
        print("The tokens below can be used to make requests to the Jira Rest API")
        print("oauth_token={}".format(access_token['oauth_token']))
        print("oauth_token_secret={}".format(access_token['oauth_token_secret']))
    except:
        print("Token Request Denied. Please ensure you have configured Jira.")


if __name__ == '__main__':
    main()
