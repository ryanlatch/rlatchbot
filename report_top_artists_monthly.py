#!/usr/bin/env python

import auths
import requests
import os
from datetime import datetime, timedelta

def get_month():

    # Get the current date 
    now = datetime.now()
    # Make into string format for ease of reading (e.g. Sept 2024)
    now_month_year_string = now.strftime("%b %Y")

    return now_month_year_string


def get_top_artists_dict():
    
    # Set up the empty dict and the number to tell the order of most listened to 
    num = 0
    top_artists_dict = {}
    
    # Query LastFM to got the top 5 most listened to artists. We use LastFM rather than spotify as spotify's 'top artists' call 
    # doesn't provide plays data, and using 'recently played' only gives last 50 played tracks. 
    top_artists_last = auths.pylast.User.get_top_artists(self=auths.LASTFM_USER_ID, period='1month', limit=5)

    # Loop through the top artists and create a dict entry in the format {1: {'artist': Joni Mitchell, 'streams': 102}}
    for last_artist in top_artists_last:
        num += 1
        top_artists_dict[num] = {'artist': last_artist.item.name, 'streams': last_artist.weight}

    return top_artists_dict

# def get_recently_played():

    # This only gets the last 50 tracks so isn't exactly useful

    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    results = auths.sp.current_user_recently_played(limit=50)
    tracks = []

    while results:
        for track in results['items']:
            # only get tracks that have been played in the last month
            track_played_at = datetime.strptime(track['played_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
            if track_played_at < start_date:
                results = None
                break
            tracks.append(track)

        if results and results['next']:
            results = auths.sp.next(results)
        else:
            results = None
    
    # count the amount of times an artist's name appears
    artist_counter = {}

    for track in tracks:
        artists = track['track']['artists']
        for artist in artists:
            artist_name = artist['name']
            if artist_name in artist_counter:
                artist_counter[artist_name] += 1
            else:
                artist_counter[artist_name] = 1

    top_artists = sorted(artist_counter.items(), key=lambda x: x[1], reverse=True)

    print(top_artists)



def create_tweet_string():

    # Use the dict to create a structured string to use in the tweet.
    top_artists = get_top_artists_dict()
    tweet_string = (f'My top 5 artists on Spotify {get_month()}:\n'
                    f'1. {top_artists[1]["artist"]} - {top_artists[1]["streams"]} plays,\n'
                    f'2. {top_artists[2]["artist"]} - {top_artists[2]["streams"]} plays,\n'
                    f'3. {top_artists[3]["artist"]} - {top_artists[3]["streams"]} plays,\n'
                    f'4. {top_artists[4]["artist"]} - {top_artists[4]["streams"]} plays,\n'
                    f'5. {top_artists[5]["artist"]} - {top_artists[5]["streams"]} plays.\n')
    
    return tweet_string

def get_top_artist_pic():

    # To increase engagement, we get the top listened to artist's picture.
    top_artists = get_top_artists_dict()

    # Search spotify for the top artist, then retrieve and return the image url.
    no_1_artist = top_artists[1]['artist']
    spotify_search = auths.sp.search(q=f'artist: {no_1_artist}', type='artist')
    image_url = spotify_search['artists']['items'][0]['images'][0]['url']

    return image_url

def download_image():

    # We must store this image locally, to upload it to twitter.

    response = requests.get(url=get_top_artist_pic(), stream=True)
    # Status code 200 means successful request.
    if response.status_code == 200:
        # Write the file to a known filepath
        with open(auths.keys.images_filepath, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
        return True
    # If there was an issue downloading the image the function returns False,
    # therefore when constructing the tweet we won't try to upload an image that doesn't exist.
    return False


def tweet(): 

    # Using all of the gathered data, we are ready to tweet.

    # First try to download the image, then check that the image downloaded ok.
    if download_image(): 
        # Upload the image to twitter using their v1.1 API, v2.0 doesn't allow image upload
        media = auths.twmedia_api.media_upload(auths.keys.images_filepath)
        # Then tweet using twitters v2.0 API, their v1.1 doesn't allow tweet creation... smart...
        tweet = auths.tweet_api.create_tweet(media_ids=[media.media_id], 
                                     text=create_tweet_string()
                                     )
        
        # Get the posted tweet URL to print to me, so I can check the tweet out easily.
        tweet_url = f"https://twitter.com/i/web/status/{tweet.data['id']}"
        print(f"Successfully tweeted with image, check it out: {tweet_url}")

        # Delete the local image to save space 
        os.remove(auths.keys.images_filepath)

    # If there was an issue downloading the image, just do a normal text tweet.
    else:
        print("Media upload issues, tweeting just string.")
        tweet = auths.tweet_api.create_tweet(text=create_tweet_string())
        tweet_url = f"https://twitter.com/i/web/status/{tweet.data['id']}"
        print(f"Successfully tweeted without image, check it out: {tweet_url}.")

# Run the function to create a tweet, this handles the running of other functions too.
tweet()