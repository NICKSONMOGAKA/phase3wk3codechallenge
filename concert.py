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

class Concert:
    def __init__(self, id):
        self.id = id

    def band(self):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM bands
            JOIN concerts ON bands.name = concerts.band_name
            WHERE concerts.id = ?
        ''', (self.id,))
        band = cursor.fetchone()
        conn.close()
        return {'name': band[0], 'hometown': band[1]} if band else None

    def venue(self):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM venues
            JOIN concerts ON venues.title = concerts.venue_title
            WHERE concerts.id = ?
        ''', (self.id,))
        venue = cursor.fetchone()
        conn.close()
        return {'title': venue[0], 'city': venue[1]} if venue else None

    def hometown_show(self):
        band = self.band()
        venue = self.venue()
        return band and venue and band['hometown'] == venue['city']

    def introduction(self):
        band = self.band()
        venue = self.venue()
        return f"Hello {venue['city']}!!!!! We are {band['name']} and we're from {band['hometown']}" if band and venue else None

class Venue:
    def __init__(self, title):
        self.title = title

    def concerts(self):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts
            WHERE venue_title = ?
        ''', (self.title,))
        concerts = cursor.fetchall()
        conn.close()
        return concerts

    def bands(self):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT bands.name, bands.hometown FROM bands
            JOIN concerts ON bands.name = concerts.band_name
            WHERE concerts.venue_title = ?
        ''', (self.title,))
        bands = cursor.fetchall()
        conn.close()
        return [{'name': b[0], 'hometown': b[1]} for b in bands]

    def concert_on(self, date):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts
            WHERE venue_title = ? AND date = ?
        ''', (self.title, date))
        concert = cursor.fetchone()
        conn.close()
        return concert

    def most_frequent_band(self):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT band_name, COUNT(*) as num_performances FROM concerts
            WHERE venue_title = ?
            GROUP BY band_name
            ORDER BY num_performances DESC
            LIMIT 1
        ''', (self.title,))
        band = cursor.fetchone()
        conn.close()
        return {'name': band[0], 'performances': band[1]} if band else None

class Band:
    def __init__(self, name):
        self.name = name

    def concerts(self):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM concerts
            WHERE band_name = ?
        ''', (self.name,))
        concerts = cursor.fetchall()
        conn.close()
        return concerts

    def venues(self):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT venues.title, venues.city FROM venues
            JOIN concerts ON venues.title = concerts.venue_title
            WHERE concerts.band_name = ?
        ''', (self.name,))
        venues = cursor.fetchall()
        conn.close()
        return [{'title': v[0], 'city': v[1]} for v in venues]

    def play_in_venue(self, venue_title, date):
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO concerts (band_name, venue_title, date)
            VALUES (?, ?, ?)
        ''', (self.name, venue_title, date))
        conn.commit()
        conn.close()

    def all_introductions(self):
        intros = []
        for concert in self.concerts():
            venue = Venue(concert[2])
            intros.append(Concert(concert[0]).introduction())
        return intros

    @staticmethod
    def most_performances():
        conn = sqlite3.connect('concerts.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT band_name, COUNT(*) as num_performances FROM concerts
            GROUP BY band_name
            ORDER BY num_performances DESC
            LIMIT 1
        ''')
        band = cursor.fetchone()
        conn.close()
        return {'name': band[0], 'performances': band[1]} if band else None

setup_database()
