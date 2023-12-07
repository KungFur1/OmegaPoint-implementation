# All db functions might raise mysql.connector.Error
from app.db_connection import mysql_connection
import mysql.connector
from app.company.model import CompanyModel

connection = mysql_connection()


def post_company(company: CompanyModel):
    query = "INSERT INTO company (email, name) VALUES (%s, %s)"
    values = (company.email, company.name)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


def get_all_companies() -> [CompanyModel] | []:
    query = "SELECT id, email, name, created_at FROM company"
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    companies = []
    for row in rows:
        company = CompanyModel(id=row[0], email=row[1], name=row[2], created_at=row[3])
        companies.append(company)
    return companies
