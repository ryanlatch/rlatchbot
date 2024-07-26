#!/usr/bin/env python

"""
Authorisations here 
"""
import spotipy
import pylast
import keys
import tweepy


from spotipy.oauth2 import SpotifyOAuth

# Setup SpotiPy API for interacting with spotify data
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=keys.spotify_client_id,
                                               client_secret=keys.spotify_client_secret,
                                               redirect_uri=keys.redirect_url,
                                               scope=keys.spotify_scope
                                               ))

SPOTIFY_USER_ID = sp.me()['id']


# Setup PyLast API for interacting with Last.fm data

lastfm = pylast.LastFMNetwork(api_key=keys.lastfm_api_key, 
                              api_secret=keys.lastfm_secret, 
                              username=keys.lastfm_username,
                              password_hash=pylast.md5(keys.lastfm_pass),
                              ) 

LASTFM_USER_ID = lastfm.get_user(keys.lastfm_username)

# Setup Tweepy

tweet_api = tweepy.Client(bearer_token=keys.twitter_bearer_token,
                      consumer_key=keys.twitter_api_key,
                      consumer_secret=keys.twitter_api_secret,
                      access_token=keys.twitter_access_token,
                      access_token_secret=keys.twitter_access_token_secret
                      )

twmedia_auth = tweepy.OAuth1UserHandler(consumer_key=keys.twitter_api_key,
                                        consumer_secret=keys.twitter_api_secret,
                                        access_token=keys.twitter_access_token,
                                        access_token_secret=keys.twitter_access_token_secret
                                        )
twmedia_api = tweepy.API(twmedia_auth)
