from funzioni_db import *
from query import *

DB_NAME = "forge_of_rathalos"

connection = create_server_connection("localhost", "root", "root")
execute_query(connection, f"DROP DATABASE IF EXISTS {DB_NAME}")
create_database(connection,DB_NAME)
connection = create_db_connection("localhost", "root","root", DB_NAME)

#CREATE TABLES
execute_query(connection, create_categories)
execute_query(connection, create_images)
execute_query(connection, create_users)
execute_query(connection, create_reviews)
execute_query(connection, create_favorites)
execute_query(connection, create_variants)
execute_query(connection, create_insertions)

#INSERT FOREIGN KEYS
execute_query(connection, alter_images)
execute_query(connection, alter_reviews)
execute_query(connection, alter_favorites)
execute_query(connection, alter_variants)
execute_query(connection, alter_insertions)

#INSERT VALUES
insert_admin(connection)
#insert_values(connection)
#insert_articles(connection)