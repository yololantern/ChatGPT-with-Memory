import csv
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the 'Countries' table
cursor.execute('''CREATE TABLE IF NOT EXISTS Countries
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  country_name TEXT UNIQUE)''')

# Create the 'Provinces' table
cursor.execute('''CREATE TABLE IF NOT EXISTS Provinces
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  province_name TEXT,
                  country_id INTEGER,
                  UNIQUE(province_name, country_id),
                  FOREIGN KEY (country_id) REFERENCES Countries(id))''')

# Create the 'Cities' table
cursor.execute('''CREATE TABLE IF NOT EXISTS Cities
                  (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  city_name TEXT,
                  coordinate TEXT,
                  province_id INTEGER,
                  FOREIGN KEY (province_id) REFERENCES Provinces(id))''')

# Read the CSV file and process the data
with open('data.csv', 'r') as file:
    reader = csv.reader(file)
    headers = next(reader)  # Skip the header row

    # Get the indices of the columns
    country_idx = headers.index('Country')
    province_idx = headers.index('Province')
    city_idx = headers.index('City')
    coordinate_idx = headers.index('Coordinates')

    # Insert the data into the tables
    for row in reader:
        country = row[country_idx]
        province = row[province_idx]
        city = row[city_idx]
        coordinate = row[coordinate_idx]

        # Check and insert into the 'Countries' table
        cursor.execute("SELECT id FROM Countries WHERE country_name = ?", (country,))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''INSERT INTO Countries (country_name)
                            VALUES (?)''', (country,))        
            country_id = cursor.lastrowid
        else:
            country_id = result[0]

        # Check and insert into the 'Provinces' table
        cursor.execute("SELECT id FROM Provinces WHERE province_name = ? AND country_id = ?", (province, country_id))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''INSERT INTO Provinces (province_name, country_id)
                            VALUES (?, ?)''', (province, country_id))
            province_id = cursor.lastrowid
        else:
            province_id = result[0]

        # Check and insert into the 'Cities' table
        cursor.execute("SELECT id FROM Cities WHERE city_name = ? AND province_id = ?", (city, province_id))
        result = cursor.fetchone()
        if result is None:
            cursor.execute('''INSERT INTO Cities (city_name, coordinate, province_id)
                            VALUES (?, ?, ?)''', (city, coordinate, province_id))


# Commit the changes and close the database connection
conn.commit()
conn.close()
