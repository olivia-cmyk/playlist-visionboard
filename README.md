# playlist-visionboard
HCDE 310 Web Application 

VIDEO: https://uw.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=e675f19f-f3fd-4344-8c56-afc700aaa30c

PYTHONANYWHERE: This IS NOT fully functional yet because one of the APIs I used is not whitelisted by pythonanywhere.
I have submitted a request but it may take time.
The code does work locally. 
http://yaushi20.pythonanywhere.com/

IMPORTANT!
1. Steps 2 and 3 (especially step 3) take a long time to load if there are lots of songs on the album or playlist.
Please be patient.
2. This code makes around 50 requests to the Google API, which has a default limit of 100 requests/day.
I ended up having to make multiple projects with Google to test it :(

To Install:
1. pip install spotipy
2. pip install azapi

Steps in the process:
1. Input playlist or album ID from Spotify.
2. Creates a list of the 50 most repeated words in the playlist, weeding out common words like "you".
    The terminal will print (Lyrics Successfully Scraped) after each song it scrapes.
3. Gets 1 image for each word in the list and randomly places it on the screen for a collage effect.


How to create keys.py:
Included keystemplate.py. Fill in all the blank variables with your own keys.


Spotify Instructions:
1. Log into https://developer.spotify.com/dashboard/login
2. Create a new app and get a client secret and client ID


Google Instructions:
1. Visit https://console.developers.google.com and create a project.
2. Visit https://console.developers.google.com/apis/library/customsearch.googleapis.com and enable "Custom Search API" for your project.
3. Visit https://console.developers.google.com/apis/credentials and generate API key credentials for your project.
4. Visit https://cse.google.com/cse/all and in the web form where you create/edit your custom search engine enable "Image search" option and for "Sites to search" option select "Search the entire web but emphasize included sites".
