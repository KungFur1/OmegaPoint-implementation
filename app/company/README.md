# Company Package Documentation

Company package manages all company, stores CRUD operations.

## Modules Overview

### `endpoints.py`

1. **Get All Companies**
   - **Endpoint**: `/cinematic/company`
   - **Method**: GET
   - **Status Code**: 200 (OK)
   - **Description**: Retrieves information about all companies in the system. This endpoint is unauthorize, which means anyone can access it.

2. **Get Company by ID**
   - **Endpoint**: `/cinematic/company/{company_id}`
   - **Method**: GET
   - **Status Code**: 200 (OK)
   - **Description**: Retrieves information about a specific company by its ID. This endpoint is unauthorize, which means anyone can access it.

3. **Create Company**
   - **Endpoint**: `/cinematic/company`
   - **Method**: POST
   - **Status Code**: 201 (Created)
   - **Description**: Creates a new company in the system. Restricted to admin users.

4. **Edit Company**
   - **Endpoint**: `/cinematic/company`
   - **Method**: PUT
   - **Status Code**: 201 (Created)
   - **Description**: Updates the information of the company associated with the authenticated owner.

5. **Delete Company**
   - **Endpoint**: `/cinematic/company`
   - **Method**: DELETE
   - **Status Code**: 204 (No Content)
   - **Description**: Deletes the company associated with the authenticated owner.


### `db.py`
- `post_company`: Inserts a new company record.
- `put_company`: Updates an existing company record.
- `delete_company`: Deletes a company record.
- `get_all_companies`: Retrieves all company records.
- `get_company_by_id`: Retrieves a specific company record by ID.


### `model.py`
- `CompanyModel`: Model representing a company record.
- `CompanyCreateModel`: Model for creating a new company.
- `CompanyUpdateModel`: Model for updating an existing company.


### `check.py`
- `company_exists`: Checks if a company exists in the database.
