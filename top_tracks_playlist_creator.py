#!/usr/bin/env python

import datetime
from dateutil.relativedelta import relativedelta
import auths

def get_dates():

    # Get the current date and 6 months ago
    now = datetime.datetime.now()
    six_months_ago = datetime.date.today() + relativedelta(months=-6)

    # Make these into string format for ease of reading when making playlist (e.g. Sept 2024)
    now_month_year_string = now.strftime("%b %Y")

    # If we're in the same year, no need to repeat the year.
    same_year = now.year == six_months_ago.year

    if same_year:
        sma_month_year_string = six_months_ago.strftime('%b')
    else:
        sma_month_year_string = six_months_ago.strftime('%b %Y')

    return now_month_year_string, sma_month_year_string

def get_playlist_name(time_range):
    
    # Set up the name of the playlist using the type of playlist we're creating and the dates.
    if time_range == 'short_term':
        playlist_name = 'Top Tracks: {}'.format(get_dates()[0]) 
    elif time_range == 'medium_term':
        playlist_name = 'Top Tracks: {} - {}'.format(get_dates()[1], get_dates()[0])
    elif time_range == 'long_term':
        # todo: figure out how long these top tracks are from.
        playlist_name = 'Top tracks: {}'.format(get_dates()[0])
    else:
        raise ValueError("time_range must == short_term, medium_term or long_term")
    
    return playlist_name
        

def create_playlist(time_range, no_of_playlist_tracks):
    
    # Get the name of the playlist from the earlier function.
    playlist_name = get_playlist_name(time_range)
    
    # Get the top tracks for the date range provided
    top_tracks = auths.sp.current_user_top_tracks(limit=no_of_playlist_tracks, time_range=time_range)

    if top_tracks:
        # Create the playlist on Spotify.
        new_playlist = auths.sp.user_playlist_create(user=auths.SPOTIFY_USER_ID, name=playlist_name)

        # Add each track to the playlist using their URI.
        tracks_to_add = []
        for track in top_tracks['items']:
            tracks_to_add.append(track['uri'])
    
        auths.sp.user_playlist_add_tracks(user=auths.SPOTIFY_USER_ID, playlist_id=new_playlist['id'], tracks=tracks_to_add)
    else:
        print("Top tracks not found. Not creating playlist.")
    

create_playlist(time_range='short_term', no_of_playlist_tracks=20)