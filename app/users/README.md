# Users Package Documentation
This package contains all logic related to user. This is a crucial package for OmegaPoint system as all of the other packages rely on users package. However, this package is not meant to be directly used by other packages, as the user authorization is handled in the `JWT_auth` package.

## Users Definition
There are 3 types of users in the system:
1. **Regular user** - this is a customer of the point of sale system. It is the most common type of user. This user should not have access to any of the company logic.
2. **Company user** - a user that is linked to some company. This type of user is always created directly under the company and is split into 3 sub types:
    1. **Owner** - can create managers and employees, can read/manage any company resources.
    2. **Manager** - can create employees, can read/manage any company resources.
    3. **Employee** - is assigned a role or multiple roles and these roles define which company resources employee can read/manage. (read more about roles in `users.roles` package)
3. **Admin user** - can only be created manually by inserting admin data into the database. Is mainly used for creating companies and owners.

### User Data
```python
class UserModel(BaseModel):
    # Authentication data
    id : int
    email : EmailStr
    password : str

    # Company data, this is only relavant to the company users
    company_id : int = Field(default = None)
    position : CompanyPositions = Field(default=None)
    roles : List[int] = Field(default = None)

    # Extra information
    created_at : datetime
    phone_number : str
    first_name : str
    last_name : str
    address : str
```
All 3 types of users have **authentication data** and **extra information**. Company users also have **company data**.


## Modules Overview

### `endpoints.py`

#### Key Endpoints

##### Authentication endpoints:
- User Registration: `/cinematic/users/register`
- User Login: `/cinematic/users/login`
- Owner Registration: `/cinematic/users/company/owner/register`
- Manager Registration: `/cinematic/users/company/manager/register`
- Employee Registration: `/cinematic/users/company/employee/register`
##### Company user management endpoints (only accessible to managers/owners):
- Get All Company Users: `/cinematic/users/company`
- Get User By ID: `/cinematic/users/company/{user_id}`
- Update Company User: `/cinematic/users/company/{user_id}`
- Delete Company User: `/cinematic/users/company/{user_id}`

### `db.py`

Database functions, all functions should be as minimal as possible and only do the sql operation no other logic.

#### Functions

- `post_user`: Insert a new regular user into the database.
- `get_user_authentication_data_by_email`: Retrieve user authentication data by email.
- `get_admin_information_by_id`: Get admin information by user ID.
- `get_user_regular_data`: Retrieve regular user data.
- `get_user_company_data`: Get company user data.
- `post_company_user`: Insert a new company user into the database.
- `get_users_by_company`: Retrieve all users belonging to a specific company.
- `get_company_user_by_id`: Get company user data by user ID.
- `put_user`: Update a user's information.
- `delete_user`: Delete a user from the database.

### `model.py`

#### Models

- `CompanyPositions`: Enum for company positions (Employee, Manager, Owner).
- `UserModel`: Main user model.
- `UserRegisterModel`: Model for user registration.
- `UserLoginModel`: Model for user login.
- `CompleteUserDataModel`: Model for complete user data.
- `UserUpdateModel`: Model for updating user information.
- `UserAuthenticationDataModel`: Model for user authentication data.
- `AdminDataModel`: Model for admin user data.
- `UserCompanyDataModel`: Model for company user data.
- `UserRegularDataModel`: Model for regular user data.

### `logreg.py`

Contains the logic for user registration and login.

### `check.py`

Includes functions for various checks and validations related to user operations, such as verifying if a user is an admin, belongs to a specific company, or checking the relationship between users (like if a manager is trying to modify an employee's data).

#### Key Functions

- `is_admin`: Check if a user is an admin.
- `belongs_to_company`: Verify if a user belongs to a company.
- `is_owner`: Check if a user is a company owner.
- `is_owner_or_manager`: Verify if a user is either a company owner or manager.
- `users_are_same_company`: Check if two users belong to the same company.
- `if_manager_then_employee`: Verify if a manager is modifying an employee's data.
- `is_employee_or_higher`: Check if a user is an employee or has a higher position.
