import spotipy.util as util
import os


class Authenticate:

    def __init__(self):
        pass

    # Authenticates user with spotify via token
    def token_authentication(self, username):
        client_id = '444e69bdfa6f48fcbce0e244e7838ace'
        client_secret = 'a2a888aa949c41c89db7fac52ae75648'
        redirect_uri = 'http://localhost:8080'
        scope = 'user-library-read'
        try:
            token = util.prompt_for_user_token(username, scope=scope,
                                               client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri)
        except AttributeError:
            os.remove(".cache-{username}".format(username=username))
            token = util.prompt_for_user_token(username, scope=scope,
                                               client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri)
        return token
