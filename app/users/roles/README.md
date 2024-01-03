# Roles Package

## Overview
This package handles company roles logic. Roles are used to determine what resources a company user of position **EMPLOYEE** has access to. **MANAGERS** & **OWNERS** have access to all company resources, so they should not be assigned roles. Only **MANAGERS** & **OWNERS** can interact with roles logic and assign roles.

## Modules

### `endpoints.py`

#### Role Management

1. **Get Company Roles**
   - **Endpoint**: `/cinematic/roles/company`
   - **Method**: GET
   - **Description**: Retrieves all roles associated with the company of the authenticated user.

2. **Get Role by ID**
   - **Endpoint**: `/cinematic/roles/company/{role_id}`
   - **Method**: GET
   - **Description**: Retrieves a specific role by its ID for the company of the authenticated user.

3. **Create Role**
   - **Endpoint**: `/cinematic/roles/company`
   - **Method**: POST
   - **Description**: Creates a new role for the company of the authenticated user.

4. **Update Role**
   - **Endpoint**: `/cinematic/roles/company/{role_id}`
   - **Method**: PUT
   - **Description**: Updates an existing role identified by its ID for the company of the authenticated user.

5. **Delete Role**
   - **Endpoint**: `/cinematic/roles/company/{role_id}`
   - **Method**: DELETE
   - **Description**: Deletes a specific role by its ID within the company of the authenticated user.

#### Role Assignment Management

1. **Get Assigned Roles by User**
   - **Endpoint**: `/cinematic/roles/users/byuser/{user_id}`
   - **Method**: GET
   - **Description**: Retrieves all roles assigned to a specific user within the company of the authenticated user.

2. **Get Users with Specific Role**
   - **Endpoint**: `/cinematic/roles/users/byrole/{role_id}`
   - **Method**: GET
   - **Description**: Retrieves all users assigned a specific role within the company of the authenticated user.

3. **Assign Role to User**
   - **Endpoint**: `/cinematic/roles/users/{role_id}/{user_id}`
   - **Method**: POST
   - **Description**: Assigns a role to a user within the company of the authenticated user.

### `db.py`

### Role Management

- **`post_role(role: RoleCreateModel)`**: Creates a new role in the system based on the `RoleCreateModel`.
- **`put_role(role: RoleUpdateModel, role_id: int)`**: Updates an existing role identified by `role_id` with new data provided in `RoleUpdateModel`.
- **`get_role_by_id(role_id: int)`**: Retrieves a specific role by its ID.
- **`get_company_roles(company_id: int)`**: Fetches all roles associated with a specific company.
- **`delete_role_by_id(role_id: int)`**: Deletes a role by its ID.
- **`delete_roles_by_company_id(company_id: int)`**: Deletes all roles associated with a specific company.

### Role Assignment

- **`get_assgined_roles_by_user_id(user_id: int)`**: Retrieves all roles assigned to a specific user.
- **`get_assgined_roles_by_role_id(role_id: int)`**: Retrieves all users assigned to a specific role.
- **`get_assigned_role(user_id: int, role_id: int)`**: Fetches a specific assigned role based on user ID and role ID.
- **`post_assigned_role(assinged_role: AssignedRole)`**: Assigns a role to a user.


### `model.py`

- **RoleModel**: All role entity data.
- **RoleCreateModel**: Used for creating a new role, including attributes like name, description, and permissions.
- **RoleUpdateModel**: For updating existing roles, similar to `RoleCreateModel`.
- **AssignedRole**: A simple model representing an assignment of a role to a user.

### `access_handler.py`
This is used for handling complex role logic, it compiles all roles that are assigned to user into one `AccessModel` which is then used by the `JWT_auth` component to provide `CompleteUserInformation`.

- **AccessModel**: A model representing various access permissions.
- **get_user_access**: A function to determine the access rights of a user based on their roles.

### `check.py`

- **role_is_same_company**: Ensures a role belongs to the same company as the user.
- **role_is_not_assigned**: Checks if a role is already assigned to a user.
