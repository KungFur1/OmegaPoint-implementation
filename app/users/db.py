# POST PUT DELETE operations return: true if successful, false if not successful
# GET operation returns: the object if succesful, None if not successful
from app.db_connection import mysql_connection
import mysql.connector
from app.users.model import UserModel, UserLoginModel, CompanyPositions, UserAuthenticationDataModel

connection = mysql_connection()


def post_user(user_data: UserModel) -> bool:
    try:
        query = (
            "INSERT INTO users (email, password_hash, phone_number, first_name, last_name, address) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        user_data_values = (user_data.email, user_data.password, user_data.phone_number, user_data.first_name, user_data.last_name, user_data.address)
        cursor = connection.cursor()
        cursor.execute(query, user_data_values)
        connection.commit()
        return True
    except mysql.connector.Error as err:
        return False
    finally:
        cursor.close()


def get_user_by_email(email) -> UserAuthenticationDataModel | None:
    try:
        query = "SELECT id, email, password_hash AS password FROM users WHERE email = %s"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result:
            return UserAuthenticationDataModel(**result)
        else:
            return None
    except mysql.connector.Error as e:
        return None
    finally:
        cursor.close()
