import urllib2
import urllib
import json


class BuildDeezerPlaylist:
    def __init__(self):
        pass

    title = ''
    data = None
    user_id = None

    def create_playlist(self, title, deezer_token):
        user_id = self.get_deezer_id(deezer_token)
        if self.check_if_playlist_exists(title, user_id, False):
            print 'A playlist called', title, 'already exists.'
            print 'Please choose a different name'
            while self.check_if_playlist_exists(title, user_id, False):
                title = raw_input()
        else:
            token = deezer_token['access_token']
            url = 'https://api.deezer.com/user/%s/playlists' % user_id
            values = {'title': title,
                      'access_token': token}
            data = urllib.urlencode(values)
            request = urllib2.Request(url, data)
            response = urllib2.urlopen(request)
            playlist_id = json.loads(response.read())['id']
            return playlist_id

    def get_deezer_id(self, deezer_token):
        if self.user_id is None:
            token = deezer_token['access_token']
            user_id_response = urllib2.urlopen('https://api.deezer.com/user/me?access_token=%s' % token)
            user = json.loads(user_id_response.read())
            self.user_id = user['id']
        return self.user_id

    def check_if_playlist_exists(self, title, user_id, return_data):
        try:
            response = urllib2.urlopen('https://api.deezer.com/user/%s/playlists' % user_id)
            playlist_data = json.loads(response.read())
        except urllib2.HTTPError as e:
            print e
            return None
        i = 0
        if self.title == title:
            if return_data:
                return self.data
            return True
        while i < playlist_data['total']:
            if playlist_data['data'][i]['title'] == title:
                self.title = playlist_data['data'][i]['title']
                self.data = playlist_data['data'][i]
                if return_data:
                    return playlist_data['data'][i]
                return True
            i += 1
        return False

    def add_to_playlist(self, title, playlist_id, song_id, deezer_token):
        user_id = self.get_deezer_id(deezer_token)
        data_present = self.check_if_playlist_exists(title, user_id, False)
        if data_present is not None and data_present:
            playlist_data = self.check_if_playlist_exists(title, user_id, True)
        elif not data_present:
            playlist_id = self.create_playlist(title, deezer_token)
        else:
            return False
        token = deezer_token['access_token']
        if playlist_id is not None:
            url = 'https://api.deezer.com/playlist/%s/tracks' % playlist_id
            values = {'songs': song_id,
                      'access_token': token}
            data = urllib.urlencode(values)
            try:
                request = urllib2.Request(url, data)
                urllib2.urlopen(request)
            except urllib2.URLError as e:
                print e
                pass
        elif playlist_data:
            url = 'https://api.deezer.com/playlist/%s/tracks' % playlist_data['id']
            values = {'songs': song_id,
                      'access_token': token}
            data = urllib.urlencode(values)
            try:
                request = urllib2.Request(url, data)
                urllib2.urlopen(request)
            except urllib2.URLError as e:
                print e
                pass
        return True

    def get_song_id(self, title, titles_and_previews):
        track_artist = title.split(" || ")
        for key in titles_and_previews:
            if track_artist[0] == key[0] and titles_and_previews[key] is not None:
                return titles_and_previews[key][0]
        return None
