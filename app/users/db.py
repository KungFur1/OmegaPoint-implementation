# All db functions might raise mysql.connector.Error
from app.db_connection import mysql_connection
import mysql.connector
from app.users.model import UserModel, UserLoginModel, CompanyPositions, UserAuthenticationDataModel, AdminInformationModel

connection = mysql_connection()


def post_user(user_data: UserModel):
    query = (
        "INSERT INTO users (email, password_hash, phone_number, first_name, last_name, address) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    user_data_values = (user_data.email, user_data.password, user_data.phone_number, user_data.first_name, user_data.last_name, user_data.address)
    cursor = connection.cursor()
    cursor.execute(query, user_data_values)
    connection.commit()
    cursor.close()


def get_user_by_email(email : str) -> UserAuthenticationDataModel | None:
    query = "SELECT id, email, password_hash AS password FROM users WHERE email = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return UserAuthenticationDataModel(**result)
    else:
        return None


def get_admin_information(user_id: int) -> AdminInformationModel | None:
    query = "SELECT user_id, created_at FROM admins WHERE user_id = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return AdminInformationModel(**result)
    else:
        return None
