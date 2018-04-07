import unittest

import spotipy
from authenticate import Authenticate


class SearchSpotify:

    def __init__(self):
        pass

    def search_for_track(self, title, token):
        sp = spotipy.Spotify(auth=token)
        track = title[0]
        artist = title[1]
        if isinstance(track,  basestring) and isinstance(artist, basestring):
            try:
                results = sp.search(q=track, type='track')
            except spotipy.SpotifyException, e:
                print str(e)
                return None
            return self.loop_over_results(track, artist, results)
        return None

    def loop_over_results(self, track, artist, results):
        for i, data in enumerate(results['tracks']['items']):
            answer = results['tracks']['items'][i]
            if answer['name'] == track and answer['album']['artists'][0]['name'] == artist:
                if answer['preview_url'] is not None:
                    return answer['preview_url']


class TestSearchSpotify(unittest.TestCase):

    def test_search_for_track(self):
        authenticate = getattr(Authenticate, 'token_authentication')
        token = authenticate(Authenticate(), 'swttyjm9q7591l77ngrnrxqyp')
        search_spotify = getattr(SearchSpotify, 'search_for_track')
        track = search_spotify(SearchSpotify(), '', token)
        self.assertIsNone(track)
        track_two = search_spotify(SearchSpotify(), 'Fast Car ||', token)
        self.assertIsNone(track_two)
        track_three = search_spotify(SearchSpotify(), '|| Tracy Chapman', token)
        self.assertIsNone(track_three)
        track_four = search_spotify(SearchSpotify(), '||', token)
        self.assertIsNone(track_four)
        track_five = search_spotify(SearchSpotify(), '%\||/%', token)
        self.assertIsNone(track_five)
        track_six = search_spotify(SearchSpotify(), '||Tracy Chapman||Fast Car', token)
        self.assertIsNone(track_six)

    def test_correct_track_found(self):
        authenticate = getattr(Authenticate, 'token_authentication')
        token = authenticate(Authenticate(), 'swttyjm9q7591l77ngrnrxqyp')
        search_spotify = getattr(SearchSpotify, 'search_for_track')
        track = search_spotify(SearchSpotify(), 'Fast Car || Tracy Chapman', token)
        self.assertIsNotNone(track)

