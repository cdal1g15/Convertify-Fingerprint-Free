import sys
import json


from dejavu import Dejavu
from datetime import datetime

from authenticate import Authenticate
from deezer_autenticate import DeezerAuthenticate
from get_spotify_playlists_tracks import GetPlaylistTracks
from search_deezer import SearchDeezer
from build_deezer_playlist import BuildDeezerPlaylist


def main():
    songs_not_found = set()
    if len(sys.argv) > 1:
        try:
            with open('config.json') as f:
                config = json.load(f)
            djv = Dejavu(config)
        except IOError:
            print "Error: File not Found"
            sys.exit()
        if len(sys.argv) > 4:
            spotify_username = sys.argv[1]
            playlist_url = sys.argv[2]
            deezer_username = sys.argv[3]
            if sys.argv[4] == 'Yes' or sys.argv[4] == 'yes':
                fingerprint = True
            else:
                fingerprint = False
        else:
            print 'Please provide your spotify username, a spotify playlist url, ' \
                  'deezer username and if you want to confirm songs with fingerprinting'
            sys.exit()

        # Initialise
        deezer_auth = DeezerAuthenticate()
        authenticate = Authenticate()
        get_playlist_tracks = GetPlaylistTracks()
        search_deezer = SearchDeezer()

        # Get both tokens
        deezer_token = deezer_auth.load_token(deezer_username)
        spotify_token = authenticate.token_authentication(spotify_username)

        # Check spotify token exists
        if spotify_token:
            results = get_playlist_tracks.get_playlist(playlist_url, spotify_token)
            title = results['name']
            spotify_tracks_and_previews = get_playlist_tracks.get_tracks(results)
            deezer_titles_and_previews, songs_not_found = search_deezer.search_all(spotify_tracks_and_previews)
            print

            # Check if new playlist title has been given, else use spotify title
            if len(sys.argv) > 5:
                playlist_title = sys.argv[5]
            else:
                playlist_title = title

            non_fingerprinting_method(deezer_titles_and_previews, songs_not_found, playlist_title, deezer_token)
    else:
        print 'Please provide your spotify username, a spotify playlist url and deezer username'


def non_fingerprinting_method(deezer_titles_and_previews, songs_not_found, playlist_title, deezer_token):
    build_deezer_playlist = BuildDeezerPlaylist()
    for song in deezer_titles_and_previews:
        track = song[0] + ' || ' + song[1]
        print track
        song_id = build_deezer_playlist.get_song_id(track, deezer_titles_and_previews)
        if song_id is not None:
            build_deezer_playlist.add_to_playlist(playlist_title, None, song_id, deezer_token)
            print track, 'Successfully added to Deezer'
        else:
            songs_not_found.add(track)
    print len(songs_not_found)


if __name__ == "__main__":
    start_time = datetime.now()
    main()
    print datetime.now() - start_time
