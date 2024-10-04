# Spotify-stats
A simple Spotify stats viewer to see info about your account. Build using Python and Flask.
Uses Spotify web API to fetch user data and display the info. Uses OAuth authentication.

# Features
- See your Favourite songs
- Create playlist with your favourite songs
- See recently played songs
- Find the availability of songs in different countries
    - The id of the song should be used to search for the availability
    - Enter country code to see if it is available in the country
    - Not entering any country code will show all available zones

# Usage 
- Initialize the .env file with you client_id and client_secret
- Change the Redirect Url to the url you have given while creating Spotify API
- Download the packages
- Run main.py  
