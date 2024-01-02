# Roles Module Documentation

## Overview
This module handles everything related to roles within a company, including creating, updating, retrieving, and deleting roles, as well as assigning roles to users.

## Files in the Module

### `endpoints.py`
This file contains the FastAPI endpoints for the roles management system. The endpoints allow for operations such as:

- **Retrieving company roles**: Fetch all roles defined within a company.
- **Getting a specific role by ID**: Obtain details of a particular role.
- **Creating a new role**: Add a new role to the system.
- **Updating an existing role**: Modify the details of an existing role.
- **Deleting a role**: Remove a role from the system.
- **Role assignments**: Managing the assignment of roles to users, including fetching roles assigned to a specific user or roles associated with a certain role ID, and assigning roles to users.

### `db.py`
This file provides the database operations associated with roles management, using `mysql.connector`. Operations include:

- **Role assignment queries**: Fetching roles assigned to a user, roles by role ID, and checking if a role is assigned.
- **Role management queries**: Functions for inserting, retrieving, updating, and deleting roles in the database.

### `model.py`
Contains Pydantic models used in the roles module. Models include:

- **RoleModel**: Represents a role with attributes like ID, company ID, created by ID, and various permissions.
- **RoleCreateModel**: Used for creating a new role, including attributes like name, description, and permissions.
- **RoleUpdateModel**: For updating existing roles, similar to `RoleCreateModel`.
- **AssignedRole**: A simple model representing an assignment of a role to a user.

### `access_handler.py`
This file contains logic for determining the access rights of users based on their roles. It includes:

- **AccessModel**: A model representing various access permissions.
- **get_user_access**: A function to determine the access rights of a user based on their roles.

### `check.py`
Includes various checks and validations such as:

- **role_is_same_company**: Ensures a role belongs to the same company as the user.
- **role_is_not_assigned**: Checks if a role is already assigned to a user.

## Usage
The roles module is integrated into the broader POS system and interacts with other modules such as user management. It utilizes FastAPI for endpoint definitions, Pydantic for data validation, and `mysql.connector` for database interactions.

## Error Handling
Errors in the database operations are handled outside the `db.py` functions, ensuring a clear separation of concerns.
