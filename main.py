import sys
from datetime import datetime

from authenticate import Authenticate
from build_deezer_playlist import BuildDeezerPlaylist
from deezer_autenticate import DeezerAuthenticate
from get_spotify_playlists_tracks import GetPlaylistTracks
from search_deezer import SearchDeezer


def main():
    songs_not_found = set()
    # Check arguments are passed to Convertify
    if len(sys.argv) > 1:
        if len(sys.argv) > 3:
            spotify_username = sys.argv[1]
            playlist_url = sys.argv[2]
            deezer_username = sys.argv[3]
        else:
            print 'Please provide your spotify username, a spotify playlist url, and ' \
                  'deezer username'
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


# Add songs matched to given Deezer playlist
def non_fingerprinting_method(deezer_titles_and_previews, songs_not_found, playlist_title, deezer_token):
    build_deezer_playlist = BuildDeezerPlaylist()
    for song in deezer_titles_and_previews:
        track = song[0] + ' || ' + song[1]
        song_id = build_deezer_playlist.get_song_id(track, deezer_titles_and_previews)
        if song_id is not None:
            build_deezer_playlist.add_to_playlist(playlist_title, None, song_id, deezer_token)
            print track, 'Successfully added to Deezer'
        else:
            songs_not_found.add(track)


if __name__ == "__main__":
    start_time = datetime.now()
    main()
    print datetime.now() - start_time
