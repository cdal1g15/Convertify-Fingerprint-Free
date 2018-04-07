import spotipy
import re
import unittest
from itertools import izip
from authenticate import Authenticate


def get_user_id(url):
    if isinstance(url, basestring):
        try:
            user_id = re.search('user/(.+?)/playlist', url).group(1)
        except AttributeError:
            user_id = None
        return user_id
    else:
        return None


def get_playlist_id(url):
    if isinstance(url, basestring):
        try:  # playlist/ is nine chars long
            i = url.rfind('playlist/')
            if i == -1:
                return None
            playlist_id = url[i + 9:]
        except AttributeError:
            playlist_id = None
        return playlist_id
    else:
        return None


class GetPlaylistTracks:
    def __init__(self):
        pass

    def get_all_playlists(self, url, token):
        all_playlists = []
        user_id = get_user_id(url)
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(user_id)
        for i, playlist in izip(xrange(10), playlists['items']):
            results = sp.user_playlist(user_id, playlist['id'],
                                       fields="name,tracks,next")
            all_playlists.append(results)
        if not playlists:
            all_playlists = None
            print("No playlists found")
        return all_playlists

    def get_playlist(self, url, token):
        user_id = get_user_id(url)
        playlist_id = get_playlist_id(url)
        sp = spotipy.Spotify(auth=token)
        if user_id and playlist_id is not None:
            required_playlist = sp.user_playlist(user_id, playlist_id, fields="name,tracks,next")
            return required_playlist
        else:
            return None

    def get_tracks(self, playlists):
        title_and_urls = dict()
        print
        print 'Playlist', playlists['name']
        print
        for word in playlists['tracks']['items']:
            preview_url = word['track']['preview_url']
            title = (word['track']['name'], word['track']['album']['artists'][0]['name'])
            title_and_urls[title] = preview_url
        return title_and_urls


class TestGetPlaylistTracks(unittest.TestCase):

    def test_get_user_id(self):
        assert (get_user_id('ThisShouldFail') is None)
        assert (get_user_id("google.com/user//playlist") is None)
        assert (get_user_id("open.spotify/user/spotify/playlist") == 'spotify')
        assert (get_user_id(123) is None)

    def test_get_playlist_id(self):
        assert (get_playlist_id('playlist//playlist/last') == 'last')
        assert (get_playlist_id('https://open.spotify.com/browse/featured') is None)
        assert (get_playlist_id('https://open.spotify.com/user/spotify/playlist/37i9dQZF1DX5uokaTN4FTR')
                == '37i9dQZF1DX5uokaTN4FTR')

    def test_get_playlists(self):
        authenticate = getattr(Authenticate, 'token_authentication')
        token = authenticate(Authenticate(), 'swttyjm9q7591l77ngrnrxqyp')
        get_playlist = getattr(GetPlaylistTracks, 'get_playlist')
        self.assertIsNone(get_playlist(GetPlaylistTracks(), 'https://open.spotify.com/user', token))
        self.assertIsNone(get_playlist(GetPlaylistTracks(), 123, token))
        self.assertEquals(get_playlist(
                            GetPlaylistTracks(),
                            'https://open.spotify.com/user/swttyjm9q7591l77ngrnrxqyp/playlist/2SChSLF3kFcy5EDwejSjKO',
                            token)['name'], 'Test Playlist', 'Test Playlist name not returned correctly')

    def test_get_all_playlists(self):
        authenticate = getattr(Authenticate, 'token_authentication')
        token = authenticate(Authenticate(), 'swttyjm9q7591l77ngrnrxqyp')
        get_all_playlists = getattr(GetPlaylistTracks, 'get_all_playlists')
        self.assertEquals(len(get_all_playlists(
            GetPlaylistTracks(),
            'https://open.spotify.com/user/swttyjm9q7591l77ngrnrxqyp/playlist/2SChSLF3kFcy5EDwejSjKO', token)), 1)
