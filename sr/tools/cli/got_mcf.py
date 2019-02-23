from __future__ import print_function

'''Record that we have received a Media Consent Form for a given user.'''

USERMAN_URL = "https://{server}:{port}/userman/"

class UsermanServer(object):

    @classmethod
    def from_config(cls, config):
        username = config.get_user()
        password = config.get_password(user=username)

        base_url = USERMAN_URL.format(server=config['server'],
                                      port=config['https_port'])

        return cls(base_url, username, password)

    def __init__(self, base_url, username, password):
        import requests
        self._session = requests.Session()
        self._session.auth = (username, password)
        self._base_url = base_url

    def __enter__(self):
        self._session.__enter__()
        return self

    def __exit__(self, t, v, tb):
        self._session.__exit__(t, v, tb)

    def _check_response(self, response):
        url = response.url
        if url.startswith(self._base_url):
            # Remove the common part
            url = url[len(self._base_url):]

        if response.status_code == 403:
            auth_errors = response.json().get('authentication_errors')
            if auth_errors:
                exit(', '.join(auth_errors))
            else:
                exit("You are not authorized to access data from '{0}'." \
                        .format(url))

        if response.status_code != 200:
            # Some other fail. Maybe the user doesn't exist?
            error("Failed to fetch data from '{0}' (code: {1})." \
                    .format(url, response.status_code))
            exit(response.text)

    def _get_url(self, args):
        endpoint = '/'.join(args)
        return self._base_url + endpoint

    def get(self, *args):
        url = self._get_url(args)
        response = self._session.get(url)
        self._check_response(response)
        return response.json()

    def post(self, *args, **data):
        url = self._get_url(args)
        response = self._session.post(url, data)
        self._check_response(response)
        return response.json()

def error(msg):
    import sys
    print(msg, file=sys.stderr)

def query(question, yes_opts, no_opts):
    import six

    options = yes_opts + no_opts
    while True:
        answer = six.moves.input(question).lower()
        if answer not in options:
            print('Invalid input!')
        else:
            break

    return answer in yes_opts

def describe_user(user_info, userman):
    colleges = user_info['colleges']
    if not colleges:
        college = '<nowhere>'
    else:
        college_info = userman.get('colleges', colleges[0])
        college = college_info['name']

    description = "'{0} {1}' at '{2}'".format(user_info['first_name'],
                                              user_info['last_name'],
                                              college)
    return description

def command(args):
    from sr.tools.config import Config

    with UsermanServer.from_config(Config()) as userman:
        user_info = userman.get('user', args.username)
        description = describe_user(user_info, userman)

        if user_info['has_media_consent']:
            exit("{0} already granted media-consent!".format(description))

        question = "Confirm media-consent for {0}? [Y/n]: ".format(description)
        confirm = query(question, ('', 'y'), ('n',))

        if not confirm:
            exit()

        # Yes, really, we need to pass 'true' as a string
        userman.post('user', args.username, media_consent='true')


def add_subparser(subparsers):
    parser = subparsers.add_parser('got-mcf', help=__doc__)
    parser.add_argument('username', help='The username to record the consent for.')
    parser.set_defaults(func=command)
