from app.db import mysql_connection
from app.users.user_model import UserSchema


connection = mysql_connection()

# Returns all users in a dictionary
def get_users():
    query = "SELECT * FROM blogging_system.users;"
    cursor = connection.cursor()
    cursor.execute(query)
    users = cursor.fetchall()

    users_dict = {}
    if users:
        for user in users:
            user_id = user[0]  
            user_data = {
                'fullname': user[1],
                'email': user[2],
                'password': user[3]
            }
            users_dict[user_id] = user_data
    else:
        print("No users found.")
    cursor.close()

    return users_dict


# Returns true if upload was successful, false if not
def insert_user(user: UserSchema) -> bool:
    query = """
    INSERT INTO blogging_system.users (fullname, email, password)
    VALUES (%s, %s, %s);
    """
    values = (user.fullname, user.email, user.password)
    cursor = connection.cursor()
    cursor.execute(query, values)
    connection.commit()
    cursor.close()
    return True