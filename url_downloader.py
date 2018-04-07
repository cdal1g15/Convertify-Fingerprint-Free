import urllib2
import string

import os
import errno

import search_spotify


class URLDownloader:

    def __init__(self):
        pass

    # Pass in url with preview mp3 and track title,
    # will store mp3 under track title at given location
    def download_song(self, url, title, storage_path):
        title_artist = ' || '.join(title)
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = response.read()
        title_artist = string.replace(title_artist, "/", "|")
        mp3_name = os.path.join(storage_path, title_artist + '.mp3')
        song = open(mp3_name, "w")
        song.write(data)
        song.close()

    def download_deezer_tracks(self, titles_and_previews, title):
        storage_path = '/home/conor/Documents/Project-Data/Deezer/' + title
        try:
            os.makedirs(storage_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        count = 0
        fail_count = 0
        for key in titles_and_previews:
            if titles_and_previews[key] is not None:
                url = titles_and_previews[key][1]
                count += 1
                self.download_song(url, key, storage_path)
            else:
                fail_count += 1
                print 'No audio matching available for', key[0], "||", key[1]
        print
        print 'Deezer:', count, 'songs downloaded successfully,', fail_count, 'failed to download'
        print

    def download_spotify_playlist(self, titles_and_previews, title, token):
        storage_path = '/home/conor/Documents/Project-Data/Spotify/' + title
        try:
            os.makedirs(storage_path)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
        search = search_spotify.SearchSpotify()
        count = 0
        fail_count = 0
        for key in titles_and_previews:
            url = titles_and_previews[key]
            if url is not None:
                count += 1
                self.download_song(url, key, storage_path)
            else:
                search_answer = search.search_for_track(key, token)
                if search_answer is not None:
                    count += 1
                    self.download_song(search_answer, key, storage_path)
                else:
                    fail_count += 1
                    print 'No audio matching available for', key[0], "||", key[1]
        print
        print 'Spotify:', count, 'songs downloaded successfully,', fail_count, 'failed to download'


class TestUrlDownloader:

    def __init__(self):
        pass

    def test_download_playlist(self):
        print
        # Add download testing
