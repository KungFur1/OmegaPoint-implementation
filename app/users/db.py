from app.db_connection import mysql_connection
from app.users.model import UserModel, UserLoginModel, CompanyPositions
import mysql.connector

connection = mysql_connection()
# All database post, put, delete functions will return true if operation was succesful, false if not


# Upload a new user to database
def insert_user_to_database(user_data: UserModel) -> bool:
    try:
        cursor = connection.cursor()
        add_user_query = (
            "INSERT INTO users (email, password_hash, phone_number, first_name, last_name, address) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        user_data_values = (
            user_data.email,
            user_data.password,
            user_data.phone_number,
            user_data.first_name,
            user_data.last_name,
            user_data.address
        )
        cursor.execute(add_user_query, user_data_values)
        connection.commit()
    except mysql.connector.Error as err:
        return False
    finally:
        if connection.is_connected():
            cursor.close()
    return True


# Check if there already is a user with such email
def email_exists(email):
    try:
        cursor = connection.cursor()
        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as e:
        return False
    finally:
        cursor.close()


# Find user by email
def retrieve_user_by_email(email):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT  email, password_hash AS password FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return UserLoginModel(**result)
    else:
        return None

