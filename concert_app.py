import sqlite3

# Connecting to the database
conn = sqlite3.connect('concerts.db')
cursor = conn.cursor()

# Creating Bands table
cursor.execute('''CREATE TABLE IF NOT EXISTS bands (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    hometown TEXT
)''')

# Creating Venues table
cursor.execute('''CREATE TABLE IF NOT EXISTS venues (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    city TEXT
)''')

# Creating Concerts table
cursor.execute('''CREATE TABLE IF NOT EXISTS concerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    band_id INTEGER,
    venue_id INTEGER,
    date TEXT,
    FOREIGN KEY(band_id) REFERENCES bands(id),
    FOREIGN KEY(venue_id) REFERENCES venues(id)
)''')

conn.commit()

# Defining the Concert class
class Concert:
    def __init__(self, id, band_id, venue_id, date):
        self.id = id
        self.band_id = band_id
        self.venue_id = venue_id
        self.date = date
    
    @staticmethod
    def band(concert_id):
        query = '''
        SELECT bands.* FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        WHERE concerts.id = ?
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (concert_id,))
            return cursor.fetchone()

    @staticmethod
    def venue(concert_id):
        query = '''
        SELECT venues.* FROM concerts
        JOIN venues ON concerts.venue_id = venues.id
        WHERE concerts.id = ?
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (concert_id,))
            return cursor.fetchone()

    @staticmethod
    def hometown_show(concert_id):
        query = '''
        SELECT bands.hometown, venues.city FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        JOIN venues ON concerts.venue_id = venues.id
        WHERE concerts.id = ?
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (concert_id,))
            band_hometown, venue_city = cursor.fetchone()
            return band_hometown == venue_city

    @staticmethod
    def introduction(concert_id):
        query = '''
        SELECT venues.city, bands.name, bands.hometown FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        JOIN venues ON concerts.venue_id = venues.id
        WHERE concerts.id = ?
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (concert_id,))
            venue_city, band_name, band_hometown = cursor.fetchone()
            return f"Hello {venue_city}!!!!! We are {band_name} and we're from {band_hometown}"

# Defining the Venue class
class Venue:
    def __init__(self, id, title, city):
        self.id = id
        self.title = title
        self.city = city

    @staticmethod
    def concerts(venue_id):
        query = '''
        SELECT * FROM concerts
        WHERE venue_id = ?
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (venue_id,))
            return cursor.fetchall()

    @staticmethod
    def bands(venue_id):
        query = '''
        SELECT DISTINCT bands.* FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        WHERE concerts.venue_id = ?
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (venue_id,))
            return cursor.fetchall()

    @staticmethod
    def concert_on(venue_id, date):
        query = '''
        SELECT * FROM concerts
        WHERE venue_id = ? AND date = ?
        LIMIT 1
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (venue_id, date))
            return cursor.fetchone()

    @staticmethod
    def most_frequent_band(venue_id):
        query = '''
        SELECT bands.*, COUNT(concerts.id) as performances FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        WHERE concerts.venue_id = ?
        GROUP BY bands.id
        ORDER BY performances DESC
        LIMIT 1
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (venue_id,))
            return cursor.fetchone()

# Defining the Band class
class Band:
    def __init__(self, id, name, hometown):
        self.id = id
        self.name = name
        self.hometown = hometown

    @staticmethod
    def concerts(band_id):
        query = '''
        SELECT * FROM concerts
        WHERE band_id = ?
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (band_id,))
            return cursor.fetchall()

    @staticmethod
    def venues(band_id):
        query = '''
        SELECT DISTINCT venues.* FROM concerts
        JOIN venues ON concerts.venue_id = venues.id
        WHERE concerts.band_id = ?
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (band_id,))
            return cursor.fetchall()

    @staticmethod
    def play_in_venue(band_id, venue_id, date):
        query = '''
        INSERT INTO concerts (band_id, venue_id, date)
        VALUES (?, ?, ?)
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (band_id, venue_id, date))
            conn.commit()

    @staticmethod
    def all_introductions(band_id):
        query = '''
        SELECT venues.city, bands.name, bands.hometown FROM concerts
        JOIN venues ON concerts.venue_id = venues.id
        JOIN bands ON concerts.band_id = bands.id
        WHERE concerts.band_id = ?
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query, (band_id,))
            introductions = cursor.fetchall()
            return [f"Hello {city}!!!!! We are {name} and we're from {hometown}" for city, name, hometown in introductions]

    @staticmethod
    def most_performances():
        query = '''
        SELECT bands.*, COUNT(concerts.id) as performances FROM concerts
        JOIN bands ON concerts.band_id = bands.id
        GROUP BY bands.id
        ORDER BY performances DESC
        LIMIT 1
        '''
        with sqlite3.connect('concerts.db') as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchone()

# Creating some bands and venues
with sqlite3.connect('concerts.db') as conn:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO bands (name, hometown) VALUES (?, ?)", ('Sauti Sol', 'Nairobi'))
    cursor.execute("INSERT INTO bands (name, hometown) VALUES (?, ?)", ('Elani', 'Nairobi'))
    cursor.execute("INSERT INTO venues (title, city) VALUES (?, ?)", ('Kenyatta International Convention Centre', 'Nairobi'))
    cursor.execute("INSERT INTO venues (title, city) VALUES (?, ?)", ('Moi Stadium', 'Kisumu'))

    # Adding some concerts
    sauti_sol_id = cursor.execute("SELECT id FROM bands WHERE name = 'Sauti Sol'").fetchone()[0]
    elani_id = cursor.execute("SELECT id FROM bands WHERE name = 'Elani'").fetchone()[0]
    kenyatta_id = cursor.execute("SELECT id FROM venues WHERE title = 'Kenyatta International Convention Centre'").fetchone()[0]
    moi_id = cursor.execute("SELECT id FROM venues WHERE title = 'Moi Stadium'").fetchone()[0]

    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (?, ?, ?)", (sauti_sol_id, kenyatta_id, '2024-09-15'))
    cursor.execute("INSERT INTO concerts (band_id, venue_id, date) VALUES (?, ?, ?)", (elani_id, moi_id, '2024-09-16'))

    conn.commit()
