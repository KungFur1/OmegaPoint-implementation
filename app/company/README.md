# Company Documentation

The Company module is part of a FastAPI application, responsible for managing company-related data and operations. It includes endpoints for CRUD operations on companies and related database interaction logic.

## Files Overview

### `endpoints.py`

This file defines the API endpoints for company-related operations. It includes routes for:

- Retrieving all companies
- Retrieving a specific company by ID
- Creating a new company
- Updating an existing company
- Deleting a company

Authorization checks are performed where necessary, using JWT and user identification.

### `db.py`

Contains functions to interact with the MySQL database. It includes:

- `post_company`: Inserts a new company record.
- `put_company`: Updates an existing company record.
- `delete_company`: Deletes a company record.
- `get_all_companies`: Retrieves all company records.
- `get_company_by_id`: Retrieves a specific company record by ID.

These functions use `mysql.connector` for database operations.

### `model.py`

Defines Pydantic models for company data. It includes:

- `CompanyModel`: Model representing a company record.
- `CompanyCreateModel`: Model for creating a new company.
- `CompanyUpdateModel`: Model for updating an existing company.

Each model includes fields like `id`, `email`, `name`, and `created_at`.

### `check.py`

Contains utility functions for company data validation. It includes:

- `company_exists`: Checks if a company exists in the database.
