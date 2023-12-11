# Users Package Documentation
This package contains all logic related to user. This is a crucial package for OmegaPoint system as all of the other packages rely on users package. However, this package is not meant to be directly used by other packages, as the user authorization is handled in the `JWT_auth` package.

## Users Definition
There are 3 types of users in the system:
1. Regular user - this is a customer of the point of sale system. It is the most common type of user. This user should not have access to any of the company logic.
2. Company user - a user that is linked to some company. This type of user is always created directly under the company and is split into 3 sub types:
    1. Owner - can create managers and employees, can read/manage any company resources.
    2. Manager - can create employees, can read/manage any company resources.
    3. Employee - is assigned a role or multiple roles and these roles define which company resources employee can read/manage. (read more about roles in `users.roles` package)
3. Admin user - can only be created manually by inserting admin data into the database. Is mainly used for creating companies and owners.

### User Data
```python
class UserModel(BaseModel):
    # Main authentication data
    id : int = Field(default=None)
    email : EmailStr = Field(default = None)
    password : str = Field(default = None)

    # Company functionality data, this is only relavant to the company users
    company_id : int = Field(default = None)
    position : CompanyPositions = Field(default=CompanyPositions.EMPLOYEE)
    roles : List[int] = Field(default = None)

    # Extra user information
    created_at : datetime = Field(default=None)
    phone_number : str = Field(default = None)
    first_name : str = Field(default = None)
    last_name : str = Field(default = None)
    address : str = Field(default = None)
```
All 3 types of users have **main authentication data** and **extra user information**. Company users also have **company functionality data**.


## Modules Overview

### `endpoints.py`
This module defines the endpoints for user authentication and management.

#### Authentication Endpoints
- **User Registration** (`POST /cinematic/users/register`): Registers a regular user.
- **User Login** (`POST /cinematic/users/login`): Authenticates any type of user and returns a JWT token.
- **Owner Registration** (`POST /cinematic/users/company/owner/register`): Registers a company owner, restricted to system administrators.
- **Manager Registration** (`POST /cinematic/users/company/manager/register`): Registers a company manager, restricted to company owners.
- **Employee Registration** (`POST /cinematic/users/company/employee/register`): Registers a company employee, restricted to company owners and managers.

#### Company User Management Endpoints
- **Get All Company Users** (`GET /cinematic/users/company`): Retrieves all users associated with a company, accessible by managers and owners.
- **Get Specific Company User** (`GET /cinematic/users/company/{user_id}`): Fetches details of a specific user within the company, accessible by managers and owners.
- **Update Company User** (`PUT /cinematic/users/company/{user_id}`): Updates the details of a company user (excluding Owner/Manager). Owners have the privilege to update any user.
- **Delete Company User** (`DELETE /cinematic/users/company/{user_id}`): Deletes a user created by the company (excluding Owner/Manager). Owners can delete any user.

### `db.py`
Database operations related to users, all functions might throw `mysql.connector.Error`.

#### Functions
- **post_user**: Inserts a new regular user into the database.
- **get_user_authentication_data_by_email**: Retrieves authentication data for a user by email.
- **get_admin_information_by_id**: Gets admin information by user ID.
- **get_user_regular_data**: Retrieves regular user data.
- **get_user_company_data**: Fetches company-related data for a user.
- **post_company_user**: Inserts a new company user, ensuring transactional integrity.

### `logreg.py`
Handles the logic for user login and registration.

#### Functions
- **register**: Registers a new user, either regular or company user.
- **login**: Authenticates a user and returns a JWT token if successful.

### `model.py`
Defines the Pydantic models used in the system, including models for different user types and authentication data.

#### Models
- **UserModel**: Main model for user data used for incoming registration requests.
- **UserLoginModel**: Model for login requests.
- **UserAuthenticationDataModel**: Used in the process of login and is retrieved by email.
- **AdminInformationModel**: Model for admin user data.
- **UserCompanyDataModel**: Model for company user data.
- **UserRegularDataModel**: Model for regular user data.
- **CompanyPositions**: Enum for company user positions.
