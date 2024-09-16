# Concerts Database

## Overview

This project manages a database for concerts, including bands, venues, and concerts. It supports various operations using raw SQL queries with Python's sqlite3.

## Schema

- *bands*: id, name, hometown
- *venues*: id, title, city
- *concerts*: id, band_id, venue_id, date

## Setup

1. *Clone the Repository*

   ```sh
   git clone this repo
   cd concerts-database
2. *Install Dependencies*

Ensure you have Python 3 and sqlite3.

 3. *Run Setup Script*
 python setup_database.py

## Usage
*Create a Concert*

Concert.play_in_venue(band_id, venue_id, date)

*Retrieve Concerts for a Venue*
Venue.concerts(venue_id)

*Retrieve Bands for a Venue*
Venue.bands(venue_id)

*Retrieve Concerts for a Band*
Band.concerts(band_id)

*check Hometown Show*
Concert.hometown_show(concert_id)

*Get Band's Introduction*
Concert.introduction(concert_id)

*Get Most Frequent Band at Venue*
Venue.most_frequent_band(venue_id)

*Get Band with Most Performances*

Band.most_performances()

## License
MIT License.