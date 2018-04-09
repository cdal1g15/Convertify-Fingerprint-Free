import unittest
import urllib2
import json
from fuzzywuzzy import fuzz


class SearchDeezer:
    def __init__(self):
        pass

    def search_all(self, tracks):
        title_and_previews = dict()
        not_found = set()
        for key, value in tracks.iteritems():
            self.search_for_track(key, title_and_previews, not_found)
        if len(title_and_previews) > 0:
            print
            return title_and_previews, not_found
        else:
            print
            return None

    def search_for_track(self, title, title_and_previews, not_found):
        track = title[0]
        artist = title[1]
        if isinstance(track, basestring) and isinstance(artist, basestring):
            track = track.encode("ascii", errors="ignore").decode()
            artist = artist.encode("ascii", errors="ignore").decode()
            quoted_artist = urllib2.quote(artist)
            quoted_track = urllib2.quote(track)
            url = 'https://api.deezer.com/search?q="track:"%s"artist:"%s' % (quoted_track, quoted_artist)
            response = urllib2.urlopen(url)
            results = json.loads(response.read())
            if results['total'] is not 0:
                url = self.loop_over_results(track, artist, results)
                title_and_previews[title] = url
            else:
                print "Not Found:", track, "by", artist
                track = ' || '.join(title) + '.mp3'
                not_found.add(track)

    def loop_over_results(self, track, artist, results):
        data = results['data']
        i = 0
        loop_count = 25
        if results['total'] < 25:
            loop_count = results['total']
        while i < loop_count:
            answer = data[i]
            ratio = fuzz.ratio(answer['title'], track)
            if ratio > 80 and answer['artist']['name'].lower() == artist.lower():
                if answer['preview'] is not None:
                    id_and_url = (answer['id'], answer['preview'])
                    return id_and_url
            i += 1
        print 'No deezer preview found for ', track
        return None


class TestSearchDeezer(unittest.TestCase):

    def test_search_for_track(self):
        data_set = dict()
        search_deezer = getattr(SearchDeezer, 'search_for_track')
        track = search_deezer(SearchDeezer(), '', data_set)
        self.assertIsNone(track)
        track_two = search_deezer(SearchDeezer(), 'Fast Car ||', data_set)
        self.assertIsNone(track_two)
        track_three = search_deezer(SearchDeezer(), '|| Tracy Chapman', data_set)
        self.assertIsNone(track_three)
        track_four = search_deezer(SearchDeezer(), '||', data_set)
        self.assertIsNone(track_four)
        track_five = search_deezer(SearchDeezer(), '%\||/%', data_set)
        self.assertIsNone(track_five)
        track_six = search_deezer(SearchDeezer(), '||Tracy Chapman||Fast Car', data_set)
        self.assertIsNone(track_six)
