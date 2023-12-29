from app.db_connection import mysql_connection
from app.users.model import UserRegisterModel, CompanyPositions, UserAuthenticationDataModel, AdminDataModel, CompleteUserDataModel, UserUpdateModel
from app.users.model import UserRegularDataModel, UserCompanyDataModel
from typing import List, Optional

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


def get_users_by_company(company_id: int) -> List[CompleteUserDataModel]:
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT u.id, u.email, cud.company_id, cud.position, 
           u.created_at, u.phone_number, u.first_name, u.last_name, u.address, 
           GROUP_CONCAT(ar.role_id) AS roles
    FROM users u
    LEFT JOIN company_users_data cud ON u.id = cud.user_id
    LEFT JOIN assigned_roles ar ON u.id = ar.user_id
    WHERE cud.company_id = %s
    GROUP BY u.id;
    """
    cursor.execute(query, (company_id,))
    result = cursor.fetchall()
    cursor.close()
    users_data = []
    for row in result:
        roles = [int(role) for role in row['roles'].split(',')] if row['roles'] else []
        user_data = CompleteUserDataModel(
            id=row['id'],
            email=row['email'],
            company_id=row['company_id'],
            position=CompanyPositions(row['position']) if row['position'] else None,
            roles=roles,
            created_at=row['created_at'],
            phone_number=row['phone_number'],
            first_name=row['first_name'],
            last_name=row['last_name'],
            address=row['address']
        )
        users_data.append(user_data)
    return users_data


def get_company_user_by_id(user_id: int) -> CompleteUserDataModel:
    cursor = connection.cursor(dictionary=True)
    query = """
    SELECT u.id, u.email, cud.company_id, cud.position, 
           u.created_at, u.phone_number, u.first_name, u.last_name, u.address, 
           GROUP_CONCAT(ar.role_id) AS roles
    FROM users u
    LEFT JOIN company_users_data cud ON u.id = cud.user_id
    LEFT JOIN assigned_roles ar ON u.id = ar.user_id
    WHERE u.id = %s
    GROUP BY u.id;
    """
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()
    cursor.close()
    if not result:
        return None
    roles = [int(role) for role in result['roles'].split(',')] if result['roles'] else []
    user_data = CompleteUserDataModel(
        id=result['id'],
        email=result['email'],
        company_id=result['company_id'],
        position=CompanyPositions(result['position']) if result['position'] else None,
        roles=roles,
        created_at=result['created_at'],
        phone_number=result['phone_number'],
        first_name=result['first_name'],
        last_name=result['last_name'],
        address=result['address']
    )
    return user_data


def put_user(user_id: int, user_data: UserUpdateModel) -> bool:
    cursor = connection.cursor()
    updates = []
    values = []
    if user_data.phone_number is not None:
        updates.append("phone_number = %s")
        values.append(user_data.phone_number)

    if user_data.first_name is not None:
        updates.append("first_name = %s")
        values.append(user_data.first_name)

    if user_data.last_name is not None:
        updates.append("last_name = %s")
        values.append(user_data.last_name)

    if user_data.address is not None:
        updates.append("address = %s")
        values.append(user_data.address)
    if not updates:
        return False
    query = "UPDATE users SET " + ", ".join(updates) + " WHERE id = %s;"
    values.append(user_id)
    cursor.execute(query, tuple(values))
    affected_rows = cursor.rowcount
    connection.commit()
    cursor.close()
    return affected_rows > 0


def delete_user(user_id: int) -> bool:
    cursor = connection.cursor()
    query = "DELETE FROM users WHERE id = %s;"
    cursor.execute(query, (user_id,))
    affected_rows = cursor.rowcount
    connection.commit()
    cursor.close()
    return affected_rows > 0