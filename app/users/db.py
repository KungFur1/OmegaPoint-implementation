from app.db_connection import mysql_connection
from app.users.model import UserRegisterModel, UserLoginModel, CompanyPositions, UserAuthenticationDataModel, AdminDataModel
from app.users.model import UserRegularDataModel, UserCompanyDataModel


connection = mysql_connection()


def post_user(user_data: UserRegisterModel):
    query = (
        "INSERT INTO users (email, password_hash, phone_number, first_name, last_name, address) "
        "VALUES (%s, %s, %s, %s, %s, %s)"
    )
    user_data_values = (user_data.email, user_data.password, user_data.phone_number, user_data.first_name, user_data.last_name, user_data.address)
    cursor = connection.cursor()
    cursor.execute(query, user_data_values)
    connection.commit()
    cursor.close()


def get_user_authentication_data_by_email(email : str) -> UserAuthenticationDataModel | None:
    query = "SELECT id, email, password_hash AS password FROM users WHERE email = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return UserAuthenticationDataModel(**result)
    else:
        return None


def get_admin_information_by_id(user_id: int) -> AdminDataModel | None:
    query = "SELECT user_id, created_at FROM admins WHERE user_id = %s"
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return AdminDataModel(**result)
    else:
        return None


def get_user_regular_data(user_id: int) -> UserRegularDataModel:
    query = "SELECT id, email, created_at, phone_number, first_name, last_name, address FROM users WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result:
        return UserRegularDataModel(id=result[0], email=result[1], created_at=result[2], phone_number=result[3], first_name=result[4], 
                                    last_name=result[5], address=result[6])
    else:
        return None


def get_user_company_data(user_id: int) -> UserCompanyDataModel:
    query = "SELECT user_id, company_id, position FROM company_users_data WHERE user_id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    if result:
        position_enum = CompanyPositions(result[2])
        return UserCompanyDataModel(user_id=result[0], company_id=result[1], position=position_enum)
    else:
        return None


# When inserting company user, multiple database operations happen, 
# there MUST NOT be a situation where one operation is succesful and other is not - we use transaction to fix that.
def post_company_user(user_data: UserRegisterModel):
    cursor = connection.cursor()
    try:
        user_query = (
            "INSERT INTO users (email, password_hash, phone_number, first_name, last_name, address) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        user_data_values = (user_data.email, user_data.password, user_data.phone_number, user_data.first_name, user_data.last_name, user_data.address)
        cursor.execute(user_query, user_data_values)

        select_query = "SELECT id FROM users WHERE email = %s"
        cursor.execute(select_query, (user_data.email,))
        user_id = cursor.fetchone()[0]

        company_user_query = (
            "INSERT INTO company_users_data (user_id, company_id, position) "
            "VALUES (%s, %s, %s)"
        )
        company_user_data_values = (user_id, user_data.company_id, user_data.position.value)
        cursor.execute(company_user_query, company_user_data_values)

        connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
