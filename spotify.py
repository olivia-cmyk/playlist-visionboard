# -----IMPORTS-----
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
# from lyricsgenius import Genius
import keys
import pprint
import time

from azapi_mine import AZlyrics

# -----SETTING UP-----
cid = keys.spotify_client_id
secret = keys.spotify_client_secret
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

# genius = Genius(keys.genius_access_token)

# -----FUNCTIONS-----


def get_user_playlists(username):
    """Parameters: username = users' username as a string
    Outputs: list of tuples of user's playlists (id, name), up to 100 playlists."""
    try:
        playlists = sp.user_playlists(username)
        pl_list = []
        while len(pl_list) < 100 and len(pl_list) < playlists["total"]:
            for playlist in playlists['items']:
                pl_list.append((playlist["id"], playlist["name"]))
        return pl_list
    except Exception as e:
        if e.code == -1: # username not found
            print("HTTP Error: 404, Username not found. Try again.")
            return None


def get_songs_playlist(playlist_id):
    """Parameters: playlist_id = id of the playlist, string
    Outputs: list of tuples of all the songs (artist, song name) in the playlist, up to 50 songs"""
    try:
        songs = sp.playlist_items(playlist_id, fields="items", limit=50)
        song_list = []
        for song in songs["items"]:
            song_name = song["track"]["name"]
            artists = song["track"]["artists"][0]["name"]
            song_list.append((artists, song_name))
        return song_list
    except spotipy.exceptions.SpotifyException as e:
        if e.code == -1:
            print("HTTP Error: 404, Playlist ID not found. Try again.")
            return None


def get_songs_album(album_id):
    """Parameters: album_id = id of the playlist, string
    Outputs: list of tuples of all the songs (artist, song name) in the album, up to 50 songs"""
    try:
        songs = sp.album_tracks(album_id, limit=50)
        song_list = []
        for song in songs["items"]:
            song_name = song["name"]
            artist = song["artists"][0]["name"]
            song_list.append((song_name, artist))
        return song_list
    except spotipy.exceptions.SpotifyException as e:
        if e.code == -1:
            print("HTTP Error: 400, Invalid Album ID. Try Again.")
            return None


def get_playlist_title(id):
    """Parameters: id = playlist id
    Outputs: string that is title of playlist"""
    info = sp.playlist(id)
    name = info["name"]
    return name


def scrape_lyrics(artist, song):
    """Parameters: artist, song = string
    Ouputs: string with lyrics, using azapi"""
    az = AZlyrics("google", accuracy=0.1)
    az.artist = artist
    az.title = song
    lyrics = az.getLyrics()  # save=True if lyrics save in txt file.

    return lyrics


def strip_lyrics(lyrics):
    """Parameters: lyrics = string of lyrics in song.
    Returns: lowercase string of lyrics that are stripped of punctuation"""
    punctuation = [".", ",", '"', "-", "!", "'", "(", ")", "?"]
    for mark in punctuation:
        lyrics = lyrics.replace(mark, "")
    lyrics = lyrics.replace("\n", " ").replace("  ", " ").lower()

    return lyrics


def no_common_words(strippedlyrics):
    """Parameters: stripped lyrics
    Returns: dictionary "word": count """
    lyricdict = {}
    common = []

    for word in strippedlyrics.split(" "):
        if word in lyricdict.keys():
            lyricdict[word] += 1
        else:
            lyricdict[word] = 1

    with open("mostcommonwords.csv", encoding="utf-8") as f:
        for word in f:
            common.append(word.strip("\n"))

    for word in common:
        if word in lyricdict.keys():
            del lyricdict[word]

    return lyricdict


def album_common_words(id):
    """Parameters: id = id of spotify album
    Returns: 50 most common words in album"""
    songslist = get_songs_album(id)
    commonwordsdict = {}

    for song in songslist:
        songname = song[1]
        artist = song[0]
        lyrics = scrape_lyrics(artist, songname)
        lyrics = strip_lyrics(lyrics)
        songworddict = no_common_words(lyrics)
        for word in songworddict.keys():
            if word in commonwordsdict.keys():
                commonwordsdict[word] += songworddict[word]
            else:
                commonwordsdict[word] = songworddict[word]

    return commonwordsdict


def sort_words(commonwordsdict):
    """Parameters: dictionary of common words from playlist/album_common_words()
    Returns: list of tuples (word, count) of the 50 most popular words"""
    new = [(k, v) for k, v in sorted(sorted(commonwordsdict.items(), key=lambda x:x[1], reverse=True), key=len)]
    finaldict = new[:51]
    return finaldict


def main():
    print("===== Testing get_user_playlists function. =====")
    # pprint.pprint(get_user_playlists("yfm6sp0vg1zu31yc1e0s3xffd"))  # testing my username
    pprint.pprint(get_user_playlists("shawnmendes"))  # testing Shawn Mendes' username
    get_user_playlists("risdfrhaasdfaasdfsdfnna")  # testing gibberish username

    print("===== Testing get_songs_playlist function. =====")
    pprint.pprint(get_songs_playlist("7yyTfDGxCtnzy2wwWI6xYn"))  # getting songs from Rihanna's "ANTI World Tour Set List"
    pprint.pprint(get_songs_playlist("gibberish"))  # testing gibberish song id

    print("===== Testing get_songs_album function. =====")
    pprint.pprint(get_songs_album("gibberish"))
    pprint.pprint(get_songs_album("151w1FgRZfnKZA9FEcg9Z3"))


    print("===== Testing scrape_lyrics function. =====")
    x = get_songs_playlist("7yyTfDGxCtnzy2wwWI6xYn")
    # pprint.pprint(scrape_lyrics(x[1][0], x[1][1]))
    # pprint.pprint(scrape_lyrics("unkwown", "gibberasidjfld"))

    print("===== Testing strip_lyrics function. =====")
    lyricsx = scrape_lyrics(x[0][0], x[0][1])
    # pprint.pprint(strip_lyrics(lyricsx))

    print("===== Testing no_common_words function. =====")
    pprint.pprint(no_common_words(strip_lyrics(lyricsx)))



if __name__ == "__main__":
    # main()
    # print(get_playlist_title("7yyTfDGxCtnzy2wwWI6xYn"))
    # 151w1FgRZfnKZA9FEcg9Z3 midnight album
    x = (album_common_words("151w1FgRZfnKZA9FEcg9Z3"))
    pprint.pprint(sort_words(x))
    # x = (scrape_lyrics("Taylor Swift", "Lavendar Haze"))
    # y = (strip_lyrics(x))
    # print(no_common_words(y))
