import json
import re
import unittest
import urllib2
import webbrowser

import sys
import time

import os


class DeezerAuthenticate:
    cache_path = '.cache-'

    def __init__(self):
        pass

    def deezer_authentication(self):
        client_id = '270982'
        client_secret = '949d142d1898a98f40bd63d1a3eb04ae'
        redirect_uri = 'http://localhost:8080'
        permissions = 'basic_access,manage_library,offline access'
        url = 'https://connect.deezer.com/oauth/auth.php?app_id=%s&redirect_uri=%s&perms=%s' \
              % (client_id, redirect_uri, permissions)
        webbrowser.open(url)
        sys.stdout.write("Please paste your url into the command line")
        print
        code = self.get_access_code()
        url2 = 'https://connect.deezer.com/oauth/access_token.php?app_id=%s&secret=%s&code=%s' \
               % (client_id, client_secret, code)
        access_code = urllib2.urlopen(url2).read()
        return self.get_access_code_from_string(access_code)

    def get_access_code(self):
        text = raw_input()
        if isinstance(text, basestring):
            try:  # playlist/ is nine chars long
                i = text.rfind('/?code=')
                if i == -1:
                    return None
                code = text[i + 7:]
            except AttributeError:
                code = None
            return code
        else:
            return None

    def get_access_code_from_string(self, text):
        if isinstance(text, basestring):
            try:
                token = re.search('token=(.+?)&expires', text).group(1)
                i = text.rfind('expires=')
                expiry = text[i + 8:]
                if expiry == '0':
                    expiry = 2628000
                token_info = self.build_token(token, expiry)
                self.save_token(token_info)
                return token_info
            except AttributeError:
                return None
        else:
            print 'error getting access code'

    def build_token(self, token, expiry):
        token_info = {"access_token": token, "expires_in": expiry, "expires_at": int(time.time()) + int(expiry)}
        return token_info

    def save_token(self, token_info):
        response = urllib2.urlopen('https://api.deezer.com/user/me?access_token=%s' % token_info['access_token'])
        username = json.loads(response.read())['name']
        with open(self.cache_path + username, 'w') as outfile:
            json.dump(token_info, outfile)

    def load_token(self, deezer_username):
        path = self.cache_path + deezer_username
        token_info = None
        if os.path.isfile(path):
            try:
                token_info = self.load_json_file(path)
                if self.is_expired(token_info):
                    self.deezer_authentication()
            except IOError:
                pass
            return token_info
        token_info = self.deezer_authentication()
        return token_info

    def load_json_file(self, path):
        try:
            json_file = open(path)
            file_info = json_file.read()
            json_file.close()
            token_info = json.loads(file_info)
            return token_info
        except IOError:
            print "Error: File not Found"
            return None
        except ValueError:
            print "Decoding JSON failure"
            return None

    def is_expired(self, token_info):
        now = int(time.time())
        expires = int(token_info['expires_at'])
        if expires < now:
            return True
        else:
            return False


class TestDeezerAuthenticate(unittest.TestCase):

    def test_is_expired(self):
        token_info = DeezerAuthenticate.load_token(DeezerAuthenticate(), 'TESTING_AUTHENTICATION_FALSE')
        self.assertIs(DeezerAuthenticate.is_expired(DeezerAuthenticate(), token_info), False)
        # Will launch authentication start because token is expired
        token_info = DeezerAuthenticate.load_token(DeezerAuthenticate(), 'TESTING_AUTHENTICATION_TRUE')
        self.assertIs(DeezerAuthenticate.is_expired(DeezerAuthenticate(), token_info), True)

    def test_load_json_file(self):
        loaded_content = DeezerAuthenticate.load_json_file(DeezerAuthenticate(), '.cache-TESTING_LOADING_ONE')
        self.assertIsNone(loaded_content)
        loaded_content = DeezerAuthenticate.load_json_file(DeezerAuthenticate(), '.cache-TESTING_LOADING_TWO')
        self.assertIsNone(loaded_content)
        loaded_content = DeezerAuthenticate.load_json_file(DeezerAuthenticate(), '.cache-TESTING_LOADING_THREE')
        self.assertEqual(loaded_content['access_token'], "LOADING_WORKED")
