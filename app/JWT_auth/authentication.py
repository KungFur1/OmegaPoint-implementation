# Authentication - take username and password and authenticate if username and password is correct
from passlib.context import CryptContext

_password_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # Password encrypting object


# Returns an encrypted version of the password
def get_password_hash(password : str) -> str:
    return _password_context.hash(password)

# Returns if the passwords match
def verify_password(plain_password : str, hashed_password : str) -> bool:
    return _password_context.verify(plain_password, hashed_password)

    