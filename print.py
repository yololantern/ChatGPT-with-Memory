import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Example Select Queries

# Retrieve all countries
cursor.execute("SELECT * FROM Countries")
countries = cursor.fetchall()
print("Countries:")
print(countries)

print()

# Retrieve all provinces
cursor.execute("SELECT * FROM Provinces")
provinces = cursor.fetchall()
print("Provinces:")
print(provinces)

print()

# Retrieve all cities
cursor.execute("SELECT * FROM Cities")
cities = cursor.fetchall()
print("Cities:")
print(cities)

print()

# Retrieve cities in a specific country
cursor.execute('''SELECT Cities.city_name, Cities.coordinate
                  FROM Cities
                  JOIN Provinces ON Cities.province_id = Provinces.id
                  JOIN Countries ON Provinces.country_id = Countries.id
                  WHERE Countries.country_name = 'USA' ''')
us_cities = cursor.fetchall()
print("Cities in USA:")
print(us_cities)

# Close the database connection
conn.close()
