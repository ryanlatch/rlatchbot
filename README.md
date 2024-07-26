# rlatchbot

https://twitter.com/rlatchbot

This bot was created to regularly tweet about my listening insights.

Dependencies: 
- pylast
- spotipy
- tweepy

### top_tracks_playlist_creator.py

When run, this gathers a list of my top tracks for the last month using Spotify's API, then uses that to create a new playlist with a name corresponding to the time frame the playlist was made for. 

![top_tracks_jul_2024](https://github.com/ryanlatch/rlatchbot/blob/main/example_images/top_monthly_tracks_example.png)

### report_top_artists_monthly.py

This gathers the top artists for the last month using Last.fm's API. I do this so I can also get the play count, where Spotify doesn't have this information. 

It uses Spotify's API to search for the top artist to get their picture, then puts those top artists in a formated string to tweet along with a image of the top artist.

![top_5_artists_tweet_example]()
