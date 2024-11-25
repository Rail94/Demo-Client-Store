from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from werkzeug.utils import secure_filename
import os
import re
import sqlite3
import bcrypt

app = Flask(__name__)
app.config.from_object('config.Config')
app.secret_key = "super secret key"

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 #MAX IMAGE SIZE 16MB
UPLOAD_FOLDER = 'static/upload'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {
    'jpeg', 'jpg', 'png', 'gif', 'bmp', 'tiff', 'tif',
    'webp', 'heif', 'heic', 'svg', 'eps', 'ai', 'avif'
}

@app.template_filter('nl2br')
def nl2br(value):
    return re.sub(r'\n', '<br>\n', value)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(directory, filename):
    name, ext = os.path.splitext(filename)
    counter = 1
    unique_filename = filename

    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{name}({counter}){ext}"
        counter +=1

    return unique_filename

def create_db_connection():
    db_config = {
        'host': app.config['MYSQL_HOST'],
        'user': app.config['MYSQL_USER'],
        'password': app.config['MYSQL_PASSWORD'],
        'database': app.config['MYSQL_DB']
    }
    return mysql.connector.connect(**db_config)

def execute_query(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

def inserisci_dati(query, params=None):
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()

connection = mysql.connector.connect(host='localhost',
                                        database='forge_of_rathalos',
                                        user='root',
                                        password='root')
cursor = connection.cursor()

def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def verify_password(conn, username, password):
    sql = """SELECT hashed_password FROM users WHERE username = ?;"""
    try:
        cursor = conn.cursor()
        cursor.execute(sql, (username,))
        row = cursor.fetchone()
        if row:
            stored_hashed_password = row[0]
            return bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8'))
        else:
            return False
    except sqlite3.Error as e:
        print(e)
        return False

# HOME ROUTES

@app.route("/")
def home():
    items = execute_query("""
    SELECT i.*, im.*, c.category
    FROM insertions i
    JOIN categories c ON i.category_id = c.category_id
    JOIN images im ON im.insertion_id = i.insertion_id
    WHERE im.image_id IN (
    SELECT MIN(image_id)
    FROM images
    GROUP BY insertion_id
    )
    ORDER BY i.insertion_id DESC;

    """)

    categories = execute_query("SELECT * FROM categories")

    return render_template('home.html', items=items, categories=categories, session=session)

@app.route('/search_article', methods=['GET'])
def search_article():
    categories = execute_query("SELECT * FROM categories")
    connection = create_db_connection()
    cursor = connection.cursor(dictionary=True)

    category = request.args.get('category')
    item = request.args.get('item')

    query = """
        SELECT i.*, im.*, c.category
        FROM insertions i
        JOIN categories c ON i.category_id = c.category_id
        JOIN images im ON im.insertion_id = i.insertion_id
        WHERE i.quantity > 0  -- Mostra solo articoli con quantità maggiore di 0 di default
        AND im.image_id IN (
            SELECT MIN(image_id)
            FROM images
            GROUP BY insertion_id
        )
    """

    filters = []
    params = []

    if category == "out_of_stock":
        query = """
            SELECT i.*, im.*, c.category
            FROM insertions i
            JOIN categories c ON i.category_id = c.category_id
            JOIN images im ON im.insertion_id = i.insertion_id
            WHERE i.quantity = 0  -- Mostra solo articoli con quantità pari a 0 per Out of Stock
            AND im.image_id IN (
                SELECT MIN(image_id)
                FROM images
                GROUP BY insertion_id
            )
        """
    elif category:
        filters.append("c.category LIKE %s")
        params.append(f"%{category}%")

    if item:
        filters.append("i.item LIKE %s")
        params.append(f"%{item}%")

    if filters:
        query += " AND " + " AND ".join(filters)

    query += " ORDER BY i.insertion_id DESC"

    cursor.execute(query, tuple(params))
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('home.html', items=result, categories=categories, session=session)


# ABOUT US ROUTES

@app.route("/about_us")
def about_us():
    return render_template('about-us.html', session=session)

# ARTICLE ROUTES

@app.route("/article/<int:id>")
def article(id):
    categories = execute_query("SELECT * FROM categories")
    error = request.args.get('error')
    category_err = request.args.get('category_err')
    items = execute_query("SELECT i.*, c.* FROM insertions i JOIN categories c ON i.category_id = c.category_id WHERE insertion_id = %s", (id,))
    images = execute_query("SELECT * FROM images WHERE insertion_id = %s", (id,))
    variants = execute_query("SELECT * FROM variants WHERE insertion_id = %s", (id,))

    return render_template('article.html', items=items[0], images=images, variants=variants, error=error, category_err=category_err, session=session, categories=categories)

@app.route("/upload_image", methods=['POST'])
def upload_file():
    insertion_id = request.form['item-id']
    if 'file' not in request.files:
        error = "No file part"
        return redirect(url_for('article', id=insertion_id, error=error, session=session))
    file = request.files['file']
    if file.filename == '':
        error = "No selected file"
        return redirect(url_for('article', id=insertion_id, error=error, session=session))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        unique_filename = get_unique_filename(app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(unique_filename)))

        connection = create_db_connection()
        cursor = connection.cursor()
        image_url = "INSERT INTO images(image_url, insertion_id) VALUES (%s,%s)"
        cursor.execute(image_url, (str(unique_filename), insertion_id))
        connection.commit()
        cursor.close()
        connection.close()
        error = "Image Uploaded!"

        return redirect(url_for('article', id=insertion_id, session=session, error=error))
    else:
        error = "File type not allowed"
        return redirect(url_for('article', id=insertion_id, error=error, session=session))

@app.route('/delete_image', methods=['POST'])
def delete_image():
    connection = create_db_connection()
    cursor = connection.cursor()

    insertion_id = request.form['item-id']
    image_id = request.form['image-id']

    cursor.execute('SELECT image_url FROM images WHERE image_id = %s', (image_id,))
    image_url = cursor.fetchone()

    if image_url:
        cursor.execute('DELETE FROM images WHERE image_id = %s', (image_id,))
        connection.commit()

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_url[0])

        if os.path.exists(file_path):
            os.remove(file_path)

    cursor.close()
    connection.close()

    return redirect(url_for('article', id=insertion_id, session=session))

@app.route('/add_variant', methods=['GET', 'POST'])
def add_variant():
    if 'email' in session:
        connection = create_db_connection()
        cursor = connection.cursor()

        insertion_id = request.form['item-id']
        new_variant = request.form['new-variant']
        variant_price = request.form['variant-price']

        insert_option = "INSERT INTO variants (variant, variant_price, insertion_id) VALUES (%s, %s, %s)"
        cursor.execute(insert_option, (new_variant, variant_price, insertion_id))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('article', id=insertion_id))
    else:
        return redirect('home')


@app.route('/delete_variant/<int:id>', methods=['GET', 'POST'])
def delete_variant(id):
    if 'email' in session and session['admin'] == 1:
        connection = create_db_connection()
        cursor = connection.cursor()

        insertion_id = request.args.get('insertion_id')
        cursor.execute('DELETE FROM variants WHERE variant_id = %s', (id,))
        connection.commit()

        cursor.close()
        connection.close()
    else:
        return redirect(url_for('home'))
    return redirect(url_for('article', id=insertion_id))

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if 'email' in session:
        connection = create_db_connection()
        cursor = connection.cursor()

        insertion_id = request.form['item-id']
        new_category = request.form['new-category']
        insert_category = "INSERT INTO categories (category) VALUES (%s)"

        cursor.execute(insert_category, (new_category,))

        connection.commit()
        cursor.close()
        connection.close()

        return redirect(url_for('article', id=insertion_id))
    else:
        return redirect('home')

@app.route('/delete_category', methods=['POST'])
def delete_category():
    connection = create_db_connection()
    cursor = connection.cursor()

    insertion_id = request.form['item-id']
    category_id = request.form['category']

    try:
        cursor.execute('DELETE FROM categories WHERE category_id = %s', (category_id,))
        connection.commit()
        category_err = "Category deleted!"
    except mysql.connector.IntegrityError as e:
        if e.errno == 1451:
            category_err = "Cannot delete, there are articles associated to this category!"
        else:
            category_err = "An error occurred while trying to delete the category."
    finally:
        cursor.close()
        connection.close()

    return redirect(url_for('article', id=insertion_id, category_err=category_err, session=session))

@app.route("/edit_description", methods=['POST'])
def edit_description():
    if 'email' in session:
        connection = create_db_connection()
        cursor = connection.cursor()

        insertion_id = request.form['item-id']
        new_description = request.form['description']

        update_description = "UPDATE insertions SET description = %s WHERE insertion_id = %s"
        cursor.execute(update_description, (new_description, insertion_id))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('article', id=insertion_id))
    else:
        return redirect('home')

@app.route("/edit_item", methods=['POST'])
def edit_item():
    if 'email' in session:
        connection = create_db_connection()
        cursor = connection.cursor()

        insertion_id = request.form['item-id']
        new_description = request.form['item-name']

        update_name = "UPDATE insertions SET item = %s WHERE insertion_id = %s"
        cursor.execute(update_name, (new_description, insertion_id))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('article', id=insertion_id))
    else:
        return redirect('home')

@app.route("/edit_category", methods=['POST'])
def edit_category():
    if 'email' in session:
        connection = create_db_connection()
        cursor = connection.cursor()

        insertion_id = request.form['item-id']
        new_category = request.form['item-category']

        update_name = "UPDATE insertions SET category_id = %s WHERE insertion_id = %s"
        cursor.execute(update_name, (new_category, insertion_id))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('article', id=insertion_id))
    else:
        return redirect('home')

@app.route("/edit_price", methods=['POST'])
def edit_price():
    if 'email' in session:
        connection = create_db_connection()
        cursor = connection.cursor()

        insertion_id = request.form['item-id']
        new_price = request.form['item-price']

        update_price = "UPDATE insertions SET price = %s WHERE insertion_id = %s"
        cursor.execute(update_price, (new_price, insertion_id))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('article', id=insertion_id))
    else:
        return redirect('home')

@app.route("/edit_quantity", methods=['POST'])
def edit_quantity():
    if 'email' in session:
        connection = create_db_connection()
        cursor = connection.cursor()

        insertion_id = request.form['item-id']
        new_quantity = request.form['item-quantity']

        update_quantity = "UPDATE insertions SET quantity = %s WHERE insertion_id = %s"
        cursor.execute(update_quantity, (new_quantity, insertion_id))
        connection.commit()

        cursor.close()
        connection.close()

        return redirect(url_for('article', id=insertion_id))
    else:
        return redirect('home')

@app.route('/delete_article/<int:id>')
def delete_article(id):
    connection = create_db_connection()
    cursor = connection.cursor()

    images = execute_query("SELECT image_id, image_url FROM images WHERE insertion_id = %s", (id,))

    for elem in images:
        cursor.execute('SELECT image_url FROM images WHERE image_id = %s', (elem['image_id'],))
        image_url = cursor.fetchone()

        if image_url:
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_url[0])

            if os.path.exists(file_path):
                os.remove(file_path)

    cursor.execute('DELETE FROM insertions WHERE insertion_id = %s', (id,))

    connection.commit()
    cursor.close()
    connection.close()

    return redirect(url_for('home', session=session))

@app.route('/add_article')
def add_article():
    if 'email' in session and session['admin'] == 1:
        categories = execute_query("SELECT * FROM categories")
        reg = request.args.get('reg')
        return render_template('add-article.html', reg=reg, categories=categories)
    else:
        return redirect('home')


@app.route('/insert_article', methods=['POST'])
def insert_article():
    if 'email' in session and session['admin'] == 1:
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            quantity = request.form['quantity']
            category_id = int(request.form['category'])

            try:
                connection = create_db_connection()
                cursor = connection.cursor()
                cursor.execute(
                    'INSERT INTO insertions (item, description, price, quantity, category_id) VALUES (%s, %s, %s, %s, %s)',
                    (name, description, price, quantity, category_id)
                )
                insertion_id = cursor.lastrowid

                if 'image' in request.files:
                    file = request.files['image']
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        unique_filename = get_unique_filename(app.config['UPLOAD_FOLDER'], filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], str(unique_filename)))

                        image_url = "INSERT INTO images(image_url, insertion_id) VALUES (%s, %s)"
                        cursor.execute(image_url, (str(unique_filename), insertion_id))
                    else:
                        connection.rollback()
                        reg = "Format not allowed!"
                        return redirect(url_for('add_article', reg=reg, session=session))

                connection.commit()

                reg = 'New Article registered!'
                return redirect(url_for('add_article', reg=reg, session=session))

            except Exception as e:
                connection.rollback()
                reg = "Error occurred during the article registration!"
                return redirect(url_for('add_article', reg=reg, session=session))

            finally:
                cursor.close()
                connection.close()

    else:
        return redirect('home')

# USERS ROUTES

@app.route("/index")
def index():
    return render_template('login.html', session=session)

@app.route("/login", methods=['GET', 'POST'])
def login():
    msg = ''
    session.clear()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')

        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        record = cursor.fetchone()

        if record and bcrypt.checkpw(password, record[3].encode('utf-8')):
            session['logged'] = True
            session['id'] = record[0]
            session['name'] = record[1]
            session['surname'] = record[2]
            session['email'] = record[4]
            session['admin'] = record[5]
            return redirect(url_for('home'))
        else:
            msg = "Email/Password not correct. Try again!"

    return render_template('login.html', msg=msg, session=session)

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('email', None)
    session.clear()
    return redirect(url_for('home'))

@app.route("/users")
def users():
    if 'email' in session and session['admin'] == 1:
        users = execute_query("SELECT * FROM users")

        return render_template('users.html', session=session, users=users)
    else:
        return redirect('/')

@app.route('/search_users', methods=['GET'])
def search_users():
    if 'email' in session and session['admin'] == 1:
        search_query = request.args.get('search-users')
        search_users = []

        if search_query:
            search_users = execute_query("""
                SELECT *
                FROM users
                WHERE users.email LIKE %s
                """, ("%" + search_query + "%",))

            if search_users:
                results = ''
            else:
                results = 'No Results'
        else:
            results = 'No Results'

        return render_template('users.html', users=search_users, results=results)
    else:
        return redirect('home')

@app.route('/add_users')
def add_users():
    if 'email' in session and session['admin'] == 1:
        reg = request.args.get('reg')
        return render_template('add_user.html', reg=reg)
    else:
        return redirect('home')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'email' in session and session['admin'] == 1:
        if request.method == 'POST':
            name = request.form['name']
            surname = request.form['surname']
            email = request.form['email']
            password = request.form['password']
            role = int(request.form['role'])

            hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            try:
                cursor.execute('INSERT INTO users (name, surname, password, email, admin) VALUES (%s, %s, %s, %s, %s)',
                               (name, surname, hashed_pwd, email, role))
                connection.commit()
                reg = 'New user registered!'
                return redirect(url_for('add_users', reg=reg))
            except mysql.connector.IntegrityError as err:
                if err.errno == 1062:
                    reg = 'Email already exists!'
                else:
                    reg = 'An error occurred. Please try again.'

                return render_template('add_user.html', reg=reg)

        return render_template('add_user.html')
    else:
        return redirect('home')

@app.route('/profile/<int:id>')
def profile(id):
    if 'email' in session and session['admin'] == 1:
        user = execute_query('SELECT * FROM users WHERE user_id = %s', (id,))

        return render_template('profile.html', user=user[0])
    else:
        return redirect('home')

@app.route('/delete_user/<int:id>', methods=['POST'])
def delete_user(id):
    if 'email' in session and session['admin'] == 1:
        connection = create_db_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM users WHERE users.user_id = %s', (id,))
        connection.commit()
        cursor.close()
        connection.close()
    else:
        return redirect(url_for('home'))
    return redirect(url_for('users'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)