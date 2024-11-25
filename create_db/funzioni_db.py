import mysql.connector
from mysql.connector import Error
import bcrypt

def create_server_connection(host_name, user_name, user_password):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def create_database(connection, name):
    cursor = connection.cursor()
    try:
        query = f"CREATE DATABASE IF NOT EXISTS {name}"
        cursor.execute(query)
        print("Database created successfully")
    except Error as err:
        print(f"Error: '{err}'")

def create_db_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print(f"MySQL Database connection successful to {db_name} ")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def read_query(connection, query, /,*, dictionary = False):
    if dictionary:
        cursor = connection.cursor(dictionary=True)
    else:
        cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

def execute_list_query(connection, sql, val):
    cursor = connection.cursor()
    try:
        cursor.executemany(sql, val)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

def insert_admin(connection):
    cursor = connection.cursor()
    query = f"INSERT INTO users(name,surname,password,email,admin) VALUES (%s,%s,%s,%s,%s)"

    admin = {
        'name': 'Admin',
        'surname': 'Admin',
        'password': 'ForgeOfAdmin!',
        'email': 'superadmin@for.com',
        'admin': True
    }

    hashed_password = bcrypt.hashpw(admin['password'].encode('utf-8'), bcrypt.gensalt())

    cursor.execute(query, (admin['name'], admin['surname'], hashed_password.decode('utf-8'), admin['email'], admin['admin']))
    connection.commit()
    cursor.close()

def insert_values(connection):
    cursor = connection.cursor()
    categories = [('Armor',),('Weapons',),('Accessories',),('Pre-Order',),('Dog Armor',)]
    insertion1 = ('Saiyan Suit Sailor', 'Saiyan Suit in Eva Foam from DBZ', 500.00, 10, 1)
    insertion2 = ('Iron Man Armor', 'Iron Man Armor in Eva Foam from Marvel', 800.00, 5, 1)
    insertion3 = ('Kayn Scythe', 'Kayn Scythe in Eva Foam from League of Legends', 699.99, 5, 2)
    image1 = [('article.webp', 1)]
    image2 = [('article2.avif', 2)]
    image3 = [('article3.webp', 3)]

    query = "INSERT INTO categories(category) VALUES (%s)"
    cursor.executemany(query, categories)

    query = "INSERT INTO insertions(item, description, price, quantity, category_id) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(query, insertion1)
    query = "INSERT INTO insertions(item, description, price, quantity, category_id) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(query, insertion2)
    query = "INSERT INTO insertions(item, description, price, quantity, category_id) VALUES (%s,%s,%s,%s,%s)"
    cursor.execute(query, insertion3)

    query = "INSERT INTO images(image_url, insertion_id) VALUES (%s, %s)"
    cursor.executemany(query, image1)
    query = "INSERT INTO images(image_url, insertion_id) VALUES (%s, %s)"
    cursor.executemany(query, image2)
    query = "INSERT INTO images(image_url, insertion_id) VALUES (%s, %s)"
    cursor.executemany(query, image3)

    connection.commit()
    cursor.close()

def insert_articles(connection):
    cursor = connection.cursor()

    categories = [('Armor',), ('Weapons',), ('Accessories',), ('Pre-Order',), ('Dog Armor',)]
    query = "INSERT INTO categories(category) VALUES (%s)"
    cursor.executemany(query, categories)