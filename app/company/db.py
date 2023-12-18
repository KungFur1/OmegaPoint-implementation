from app.db_connection import mysql_connection
from app.company.model import CompanyModel, CompanyCreateModel, CompanyUpdateModel
from typing import List, Optional

connection = mysql_connection()


def post_company(company: CompanyCreateModel):
    query = "INSERT INTO company (email, name) VALUES (%s, %s)"
    values = (company.email, company.name)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()


def put_company(company_id: int, company: CompanyUpdateModel) -> bool:
    updates = []
    values = []
    if company.email is not None:
        updates.append("email = %s")
        values.append(company.email)
    if company.name is not None:
        updates.append("name = %s")
        values.append(company.name)
    if not updates:
        return False
    query = "UPDATE company SET " + ", ".join(updates) + " WHERE id = %s"
    values.append(company_id)
    cursor = connection.cursor()
    cursor.execute(query, tuple(values))
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0


def delete_company(company_id: int) -> bool:
    query = "DELETE FROM company WHERE id = %s"
    values = (company_id,)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    affected_rows = cursor.rowcount
    cursor.close()
    return affected_rows > 0


def get_all_companies() -> List[CompanyModel]:
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


def get_company_by_id(company_id: int) -> Optional[CompanyModel]:
    query = "SELECT id, email, `name`, created_at FROM company WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (company_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        result_dict = {
            "id": result[0],
            "email": result[1],
            "name": result[2],
            "created_at": result[3]
        }
        return CompanyModel(**result_dict)
    else:
        return None
