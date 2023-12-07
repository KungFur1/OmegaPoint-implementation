from app.db_connection import mysql_connection
import mysql.connector
from app.company.model import CompanyModel

connection = mysql_connection()
# All database post, put, delete functions will return true if operation was succesful, false if not


def user_is_admin(user_id) -> bool:
    try:
        query = "SELECT * FROM admins WHERE user_id = %s"
        cursor = connection.cursor()
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result is not None
    except mysql.connector.Error as e:
        return False
    finally:
        if connection.is_connected():
            cursor.close()


def insert_company(company: CompanyModel) -> bool:
    try:
        query = "INSERT INTO company (id, email, name) VALUES (%s, %s, %s)"
        values = (company.id, company.email, company.name)
        cursor = connection.cursor()
        cursor.execute(query, values)
        connection.commit()
        return True
    except mysql.connector.Error as e:
        return False
    finally:
        if connection.is_connected():
            cursor.close()


def retrieve_all_companies():
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
        if connection.is_connected():
            cursor.close()
