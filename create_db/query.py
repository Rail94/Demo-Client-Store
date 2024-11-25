create_categories = """
CREATE TABLE categories (
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  category VARCHAR(50)
);
"""

create_images = """
CREATE TABLE images (
  image_id INT AUTO_INCREMENT PRIMARY KEY,
  image_url VARCHAR(255),
  insertion_id INT
);
"""

create_users = """
CREATE TABLE users (
  user_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(150),
  surname VARCHAR(150),
  password TEXT,
  email VARCHAR(200) UNIQUE,
  admin BOOLEAN NOT NULL
);
"""

create_messages = """
CREATE TABLE messages (
  message_id INT AUTO_INCREMENT PRIMARY KEY,
  object VARCHAR(255),
  content TEXT,
  broadcast BOOLEAN NOT NULL,
  unread BOOLEAN NOT NULL DEFAULT TRUE,
  user_id INT
);
"""

create_reviews = """
CREATE TABLE reviews (
  review_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(255),
  text TEXT,
  rank FLOAT,
  insertion_id INT,
  user_id INT
);
"""

create_etsy_reviews = """
CREATE TABLE etsy_reviews (
  etsy_review_id INT AUTO_INCREMENT PRIMARY KEY,
  etsy_title VARCHAR(255),
  etsy_text TEXT,
  etsy_rank INT,
  etsy_user INT
);
"""

create_favorites = """
CREATE TABLE favorites (
  favorite_id INT AUTO_INCREMENT PRIMARY KEY,
  insertion_id INT,
  user_id INT
);
"""

create_variants = """
CREATE TABLE variants (
  variant_id INT AUTO_INCREMENT PRIMARY KEY,
  variant VARCHAR(50),
  variant_price FLOAT(7,2),
  insertion_id INT
);
"""

create_insertions = """
CREATE TABLE insertions (
  insertion_id INT AUTO_INCREMENT PRIMARY KEY,
  item VARCHAR(255),
  description TEXT,
  price FLOAT(7,2),
  quantity INT,
  category_id INT
);
"""

#INSERT FOREIGN KEYS

alter_images = """
ALTER TABLE images
ADD FOREIGN KEY(insertion_id)
REFERENCES insertions(insertion_id)
ON DELETE CASCADE;
"""

alter_messages = """
ALTER TABLE messages
ADD FOREIGN KEY(user_id)
REFERENCES users(user_id)
ON DELETE CASCADE;
"""

alter_reviews = """
ALTER TABLE reviews
ADD FOREIGN KEY(insertion_id)
REFERENCES insertions(insertion_id)
ON DELETE SET NULL,
ADD FOREIGN KEY(user_id)
REFERENCES users(user_id)
ON DELETE SET NULL;
"""

alter_favorites = """
ALTER TABLE favorites
ADD FOREIGN KEY(user_id)
REFERENCES users(user_id)
ON DELETE CASCADE,
ADD FOREIGN KEY(insertion_id)
REFERENCES insertions(insertion_id)
ON DELETE CASCADE;
"""

alter_variants = """
ALTER TABLE variants
ADD FOREIGN KEY(insertion_id)
REFERENCES insertions(insertion_id)
ON DELETE CASCADE;
"""

alter_insertions = """
ALTER TABLE insertions
ADD FOREIGN KEY(category_id)
REFERENCES categories(category_id)
ON DELETE RESTRICT;
"""