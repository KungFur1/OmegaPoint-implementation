# POST PUT DELETE operations return: true if successful, false if not successful
# GET operation returns: the object if succesful, None if not successful
from app.db_connection import mysql_connection
import mysql.connector
from app.company.model import CompanyModel
from app.users.model import AdminInformationModel

connection = mysql_connection()


def get_admin_information(user_id) -> AdminInformationModel:
    try:
        query = "SELECT user_id, created_at FROM admins WHERE user_id = %s"
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        if result:
            return AdminInformationModel(**result)
        else:
            return None
    except mysql.connector.Error as e:
        return None
    finally:
        cursor.close()


def post_company(company: CompanyModel) -> bool:
    try:
        query = "INSERT INTO company (email, name) VALUES (%s, %s)"
        values = (company.email, company.name)
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        return True
    except mysql.connector.Error as e:
        return False
    finally:
        cursor.close()


def get_all_companies():
    try:
        query = "SELECT id, email, name, created_at FROM company"
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        companies = []
        for row in rows:
            company = CompanyModel(id=row[0], email=row[1], name=row[2], created_at=row[3])
            companies.append(company)
        return companies
    except mysql.connector.Error as e:
        return None
    finally:
        cursor.close()
