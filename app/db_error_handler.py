from fastapi import HTTPException
from mysql.connector import Error as DBError
from functools import wraps


def handle_db_error(func):

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except DBError as e:
            print(f"Database Error: {e}") # For testing
            raise HTTPException(status_code=500, detail="database error")
        
    return wrapper