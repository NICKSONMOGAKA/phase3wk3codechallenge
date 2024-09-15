Concerts Database Project
Overview
This project involves managing a database for concerts, bands, and venues. It uses raw SQL queries to handle database operations without using SQLAlchemy or any ORM. The main goal is to practice writing and executing SQL commands directly in Python.

Database Schema
The database consists of three tables:

Bands

name: The name of the band (Primary Key)
hometown: The hometown of the band
Venues

title: The title of the venue (Primary Key)
city: The city where the venue is located
Concerts

id: Auto-incrementing primary key
band_name: Name of the band (Foreign Key referencing bands.name)
venue_title: Title of the venue (Foreign Key referencing venues.title)
date: Date of the concert
Setup
To set up the database and create the required tables, run the following script:

python
Copy code
import sqlite3

def setup_database():
    conn = sqlite3.connect('concerts.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bands (
            name TEXT PRIMARY KEY,
            hometown TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS venues (
            title TEXT PRIMARY KEY,
            city TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS concerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            band_name TEXT,
            venue_title TEXT,
            date TEXT,
            FOREIGN KEY (band_name) REFERENCES bands(name),
            FOREIGN KEY (venue_title) REFERENCES venues(title)
        )
    ''')
    conn.commit()
    conn.close()

setup_database()
Classes and Methods
Concert
band(): Returns the band details for this concert.
venue(): Returns the venue details for this concert.
hometown_show(): Checks if the concert is in the band's hometown.
introduction(): Returns a string introduction for the band and concert venue.
Venue
concerts(): Returns all concerts held at this venue.
bands(): Returns all bands that have performed at this venue.
concert_on(date): Finds the first concert on a specific date at this venue.
most_frequent_band(): Returns the band that has performed the most at this venue.
Band
concerts(): Returns all concerts performed by this band.
venues(): Returns all venues where this band has performed.
play_in_venue(venue_title, date): Creates a new concert entry for this band.
all_introductions(): Returns all introductions for this band's concerts.
most_performances(): Returns the band with the most concerts overall.
Example Usage
Here’s how you can use the classes and methods:

python
Copy code
# Create instances of Band and Venue
band = Band('The Beatles')
venue = Venue('Madison Square Garden')

# Add a concert
band.play_in_venue('Madison Square Garden', '1965-08-15')

# Retrieve concert info
concert = Concert(1)
print(concert.introduction())  # Example usage

# Get all venues where the band has performed
print(band.venues())

# Get the most frequent band at a venue
print(venue.most_frequent_band())
