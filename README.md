# Bloodstock Reviser

Every year, knowing which bands to watch at Bloodstock requires studious, meticulous revision, taking hours of time and planning. 

In order to speed this process up, to create a shortlist for deeper revision, this project provides a pipeline of tools that: 

* Mine the Bloodstock website for all bands performing in the current line up
* Decorate that data with Spotify-based preview audio clips and genres
* Present the final data as a web UI allowing browsing of the artists and listening to the previews

# Pipeline

## Artists performing

Scrapy has been used to create a custom spider to crawl the https://www.bloodstock.uk.com/events/boa-2022/stages. 
This can be run as follows:

    scrapy crawl bands -O bands.json

This will output `bands.json`

## Spotify previews

The Spotify genres/previews is run as follows and assumes `bands.json` as input:

    python spotify.py

This will output `bands_final.json`. A client ID and secret is required at Spotify to run this, using the Client Credentials auth flow.

## Web page

The HTML file is created as follows and assumes `bands_final.json` as input:

    python html.py

This will output `boa-revision.html` which can be opened in a local web browser. Strap in for a truly 1999 UI experience, this was not the point at this stage.

# Improvements

* Structure the data into stages and order by date
* Enhance the UI (React + Bootstrap or Material or Tailwind) to provide a better experience e.g. filtering, type-down search, inline audio preview and a nicer look
* Create a script that runs the entire pipeline end to end for a given year, possibly deploying out to public web for others to use