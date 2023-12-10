# Authentication and Authorization Package Documentation
The goal of this package is to provide authentication and authorization functionality to the application.

## How To Authorize? (for developers who will only use this package to authorize)

### Steps
* Import modules: `authorization.py` and `user_identification.py`
* In your endpoint function parameters add: `user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)`.
* Behind the scenes `authorization_wrapper` function will extract the JWT from the HTTP header, then verify and decode it into user id and email. It will then return the data in the form of `UserIdentification` object and put it in the user_identification variable, which you can use inside your endpoint function.
* This user identification information is a source of truth, that the user with that ID and Email, has logged in and is authorized to use the resources that he should have access to.
* Finally you can use the user id from `UserIdentification`, to get access to all of the user's information.
* Use `get_complete_user_information(user_id: int) -> CompleteUserInformation`.
* If the user is not a company user `CompleteUserInformation` will have these fields set to None: company_id, position, access.

### Example
```python
from app.JWT_auth.authorization import authorization_wrapper, get_complete_user_information
from app.JWT_auth.user_identification import UserIdentification, CompleteUserInformation

@router.get("/example", tags=["example"], status_code=201)
def test(user_identification : UserIdentification = fastapi.Depends(authorization_wrapper)):
    logged_in_user_info = get_complete_user_information(user_identification.id)
    return {"Hello" : logged_in_user_info.email}
```

### Important
The `authorization_wrapper` function will automatically throw an error if there is something wrong with user authentication: JWT expired, JWT invalid, etc...
You do not need to handle these errors, these errors are integrated with fastapi and will return an HTTPException to the user automaticaly (The front-end will then ask the user to re-login).
But the point of this section is: **do not use `authorization_wrapper` in endpoints that don't need authorization**, because the users who haven't logged in won't be able to access those endpoints.

## Modules Overview (for developers who will be working on this package)

### `authentication.py`
This module is responsible for handling user authentication. It provides functionality for password hashing and verification.

#### Functions:
- `get_password_hash(password: str) -> str`: Encrypts a password.
- `verify_password(plain_password: str, hashed_password: str) -> bool`: Verifies if a plain password matches its hashed version.

### `authorization.py`
Handles user authorization, ensuring that requests to the server are made by authenticated users.

#### Functions:
- `authorization_wrapper(auth: HTTPAuthorizationCredentials) -> UserIdentification`: Authorizes a user and returns their identification information.
- `get_complete_user_information(user_id: int) -> CompleteUserInformation`: Retrieves complete information about the user. If the user is not a company user, the company related fields will be set to None.

### `jwt_handler.py`
Manages JSON Web Tokens (JWTs) for secure transmission of user information.

#### Functions:
- `signJWT(user_identification: UserIdentification) -> str`: Encodes the user identification information into JWT.
- `decodeJWT(token: str) -> UserIdentification`: Decodes a JWT to extract user information, also throws HTTPException errors, if the token is expired or invalid.

### `user_identification.py`
Defines models for user identification and complete user information.

#### Classes:
- `UserIdentification`: Model for basic user identification, returned by `authorization_wrapper`.
- `CompleteUserInformation`: Model for detailed user information including company and access details.
