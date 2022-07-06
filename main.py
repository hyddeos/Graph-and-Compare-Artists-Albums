import os
import spotipy

from spotipy.oauth2 import SpotifyClientCredentials

import spotipy.util as util
import sqlite3
import matplotlib.pyplot as plt
import numpy as np

from dotenv import load_dotenv
import os


# SETUP up database
db = sqlite3.connect('music.db')


def main():

    # SETUP To get spotify API working

    load_dotenv()
    os.environ['SPOTIPY_CLIENT_ID'] = os.environ.get('cid')
    os.environ['SPOTIPY_CLIENT_SECRET'] = os.environ.get('secret')
    os.environ['SPOTIPY_REDIRECT_URI'] = 'http://localhost:8888/callback'

    username = os.environ.get('username')
    client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
    scope = 'user-top-read'
    token = util.prompt_for_user_token(username, scope)

    if token:

        # Main program starts here

        sp = spotipy.Spotify(auth=token)

        # Function for selecting artist
        artist_id = choose_artist()

        # Function for bringing Spotify data into own database
        get_albums(sp, artist_id)

        # Plotting
        plot_datahandle(artist_id)

    else:
        print("Can't get token for", username)

    # Close DB after using
    db.close()


def choose_analysis():

    print("What do you what to analyze ")
    print("1. Danceability \n2. Valence\n3. Energy\n4. Intrumentalness\n5. Tempo")

    answer = input("Choose number: ")
    answer = int(answer)
    print("\n")

    # Converts to right number for database
    analysis_type = ""
    checked_input = False
    while checked_input is False:
        if answer == 1:
            nr = 6
            analysis_type = "Danceability"
            checked_input = True
        elif answer == 2:
            nr = 10
            analysis_type = "Valence"
            checked_input = True
        elif answer == 3:
            nr = 7
            analysis_type = "Energy"
            checked_input = True
        elif answer == 4:
            nr = 8
            analysis_type = "Intrumentalness"
            checked_input = True
        elif answer == 5:
            nr = 9
            analysis_type = "Tempo"
            checked_input = True
        else:
            print("Wrong input try again")

    return nr, analysis_type


def choose_artist():

    artist_id = input("Enter the artist id: ")
    return artist_id


def get_album_analyze(sp, album_id):

    # Get current album from Spotify
    album = sp.album_tracks(album_id)

    # Adds current db songs to variable for check of doublets
    album_tracks_in_db = []
    cursor = db.execute("SELECT track_id FROM album")
    for row in cursor:
        album_tracks_in_db.append(row)
    db.commit()

    tracks = len(album['items'])
    total_duration = 0

    # Then writing info about each song to the album db
    for track in range(tracks):

        # If the track is in db skip it, otherwise add it
        if (any(album['items'][track]['id'] in i for i in album_tracks_in_db)) is False:

            # Add song to album db with basic info and get AudioFeatures of that song
            track_data = sp.audio_features(album['items'][track]['id'])

            db.execute("INSERT INTO album (album_id, track_id, track_nr, name, duration, danceability,"
                       " energy, instrumentalness, tempo, valence) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (album_id, album['items'][track]['id'], album['items'][track]['track_number'], album['items'][track]['name'], album['items'][track]['duration_ms'], track_data[0]['danceability'], track_data[0]['energy'], track_data[0]['instrumentalness'], track_data[0]['tempo'], track_data[0]['valence']))

            db.commit()

        total_duration += album['items'][track]['duration_ms']

    # Update the albums db with more data(tot_dur and tracks)
    db.execute("UPDATE albums SET total_tracks = ?, total_duration = ? WHERE album_id = ?",
               (tracks, total_duration, album_id))
    db.commit()

    return 0


def get_albums(sp, artist_id):

    # Get albums from Spotify
    albums_raw = sp.artist_albums(artist_id, album_type='Album', country='SE', limit=20, offset=0)

    # Adds current db albums to variable for check of doublets
    albums_in_db = []
    cursor = db.execute("SELECT album_id FROM albums")
    for row in cursor:
        albums_in_db.append(row)
    db.commit()

    # Checks and add albums to DB if not found already
    for album in range(len(albums_raw['items'])):

        # Check if album is already added to database
        if (any(albums_raw['items'][album]['id'] in i for i in albums_in_db)) is False:

            # Filter function to remove albums to get cleaner data(No live album etc).
            filter_albums = id_filter()

            if not albums_raw['items'][album]['id'] in filter_albums:
                db.execute("INSERT INTO albums (artist_id, artist_name, album_id, album_name) VALUES(?, ?, ?, ?)",
                (artist_id, albums_raw['items'][album]['artists'][0]['name'], albums_raw['items'][album]['id'], albums_raw['items'][album]['name']))
                db.commit()

                # Do a analyze on the album it self and save that every album to the "album"db
                get_album_analyze(sp, albums_raw['items'][album]['id'])

    return 0


def id_filter():

    # Write the id of the album you Don't what to add in your database
    album_ids = ['72jszBHvXGh1gHkTcUEfAN', '0SieXhGy9GFJDjmwkMGsRp', '0khNt8LTr5TMBL8kbKM9vw', '3TsA6xRDYRAm6ju9Y7fBYA']
    return album_ids


def plot_datahandle(artist_id):

    artist_name = ""
    # Get all the albums
    all_albums = []
    # Sort Data about the albums
    album_id = []
    album_name = []
    album_duration = []
    # Get the songs
    all_songs = []

    # Select the albums data for graph
    cursor = db.execute("SELECT album_id, album_name, total_duration, total_tracks, artist_name "
                        "FROM albums WHERE artist_id = ?", (artist_id,))

    for row in cursor:
        all_albums.append(row)
    # placing the data into lists
    for i in range(len(all_albums)):
        album_id.append(all_albums[i][0])
        album_name.append(all_albums[i][1])
        length_to_min = (all_albums[i][2]/1000)/60
        album_duration.append(length_to_min)
        artist_name = all_albums[i][4]

    # Select data about all the song on the albums
    for album in album_id:
        cursor = db.execute("SELECT * FROM album WHERE album_id = ?", (album,))
        for row in cursor:
            all_songs.append(row)

    # Get longest album
    longest_album = max(album_duration)

    # Sends data for making graph
    graph_album(all_songs, all_albums, longest_album, artist_name)


def graph_album(all_songs, all_albums, longest_album, artist_name):

    longest_album = int(longest_album) + 1
    total_nr_albums = len(all_albums)

    # Choose what to analysis in the graph
    analyze = choose_analysis()
    # Getting the type of analyze and its name
    analyze_type = analyze[0]
    analyze_name = analyze[1]

    # Saves a list of the data
    albums_analyzed_data = []

    for album in range(total_nr_albums):
        albums_analyzed_data.append([])

    for nr in range(total_nr_albums):
        for song in range(len(all_songs)):
            if all_albums[nr][0] == all_songs[song][1]:
                albums_analyzed_data[nr].append(all_songs[song][analyze_type])

    # Get max value for Y-axis
    y_data = 0.0
    for analysed_album in range(len(albums_analyzed_data)):
        if y_data > max(albums_analyzed_data[analysed_album]):
            continue
        else:
            y_data = max(albums_analyzed_data[analysed_album])

    # Plot
    # List of colors
    color_list = ['C0', 'C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11',
                  'C12', 'C13', 'C14', 'C15', 'C16', 'C17', 'C18', 'C19', 'C20', 'C21']

    for album in range(len(all_albums)):
        for song in range(all_albums[album][3]):
            # If song is the first on album add the album title to labels, else hide it
            if song == 0:
                x = np.linspace(0, longest_album, all_albums[album][3])
                plt.plot(x, albums_analyzed_data[album], marker='o',
                         color=color_list[album], label=all_albums[album][1])
            else:
                x = np.linspace(0, longest_album, all_albums[album][3])
                plt.plot(x, albums_analyzed_data[album], marker='o', color=color_list[album],
                         label='_Hidden')

    # Decorate
    plt.xlabel('From first to last song')
    plt.ylabel(analyze_name)
    plt.title(artist_name + "´s Albums " + analyze_name + " per song")
    # Limits
    plt.xlim(-2, longest_album+2)
    plt.ylim(0, y_data)
    plt.legend(ncol=2)
    # Discrupt
    plt.show()


if __name__ == "__main__":
    main()
