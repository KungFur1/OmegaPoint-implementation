from app.db_connection import mysql_connection
from app.users.roles.model import RoleModel
from typing import List, Optional

connection = mysql_connection()


def post_role(role: RoleModel):
    query = """
    INSERT INTO roles (company_id, name, description, users_read, users_manage, inventory_read, inventory_manage, 
                       services_read, services_manage, items_read, items_manage, payments_read, payments_manage, 
                       created_at, created_by)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    data = (
        role.company_id, role.name, role.description, role.users_read, role.users_manage, 
        role.inventory_read, role.inventory_manage, role.services_read, role.services_manage, 
        role.items_read, role.items_manage, role.payments_read, role.payments_manage, 
        role.created_at, role.created_by_id
    )
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()


def get_company_roles(company_id: int) -> List[RoleModel]:
    query = "SELECT * FROM roles WHERE company_id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (company_id,))
    rows = cursor.fetchall()
    roles = [RoleModel(
        id=row[0],
        company_id=row[1],
        created_by_id=row[2],
        name=row[3],
        description=row[4],
        created_at=row[5],
        users_read=row[6],
        users_manage=row[7],
        inventory_read=row[8],
        inventory_manage=row[9],
        services_read=row[10],
        services_manage=row[11],
        items_read=row[12],
        items_manage=row[13],
        payments_read=row[14],
        payments_manage=row[15]
    ) for row in rows]
    return roles


def get_role_by_id(role_id: int) -> Optional[RoleModel]:
    query = "SELECT * FROM roles WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (role_id,))
    row = cursor.fetchone()
    if row is not None:
        role = RoleModel(
            id=row[0],
            company_id=row[1],
            created_by_id=row[2],
            name=row[3],
            description=row[4],
            created_at=row[5],
            users_read=row[6],
            users_manage=row[7],
            inventory_read=row[8],
            inventory_manage=row[9],
            services_read=row[10],
            services_manage=row[11],
            items_read=row[12],
            items_manage=row[13],
            payments_read=row[14],
            payments_manage=row[15]
        )
        return role
    return None


def put_role(role: RoleModel):
    query = """
    UPDATE roles SET company_id = %s, created_by_id = %s, name = %s, description = %s, created_at = %s, 
    users_read = %s, users_manage = %s, inventory_read = %s, inventory_manage = %s, services_read = %s, 
    services_manage = %s, items_read = %s, items_manage = %s, payments_read = %s, payments_manage = %s WHERE id = %s
    """
    data = (role.company_id, role.created_by_id, role.name, role.description, role.created_at, role.users_read,
            role.users_manage, role.inventory_read, role.inventory_manage, role.services_read, role.services_manage,
            role.items_read, role.items_manage, role.payments_read, role.payments_manage, role.id)
    cursor = connection.cursor()
    cursor.execute(query, data)
    connection.commit()


def delete_role_by_id(role_id: int):
    query = "DELETE FROM roles WHERE id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (role_id,))
    connection.commit()


def delete_roles_by_company_id(company_id: int):
    query = "DELETE FROM roles WHERE company_id = %s"
    cursor = connection.cursor()
    cursor.execute(query, (company_id,))
    connection.commit()
