# Loyalty Module

## Overview

The `loyalty` module is designed to manage loyalty programs within the application. It includes endpoints for creating, retrieving, updating, and deleting loyalty information, tied to specific companies. This module is part of a larger point of sale system and is built using Python with FastAPI, Pydantic, and MySQL.

## Structure

The module is divided into several key files:

- `endpoints.py`: Contains all the API endpoints related to loyalty operations.
- `db.py`: Houses the database interaction functions for loyalty-related operations.
- `model.py`: Defines the Pydantic models for loyalty data validation and serialization.
- `check.py`: Provides functions for additional checks and validations, particularly for loyalty and company data consistency.

## Endpoints

### GET `/cinematic/loyalty`
- Retrieves all loyalty programs associated with the authenticated user's company.
- Requires user identification and authorization.

### GET `/cinematic/loyalty/{id}`
- Retrieves a specific loyalty program by its ID.
- Ensures that the requested loyalty program belongs to the user's company.

### POST `/cinematic/loyalty`
- Creates a new loyalty program.
- Requires details of the loyalty program and user authentication.
- Access restricted to users with owner or manager roles.

### DELETE `/cinematic/loyalty/{id}`
- Deletes a loyalty program by its ID.
- Checks if the loyalty program belongs to the user's company.
- Access restricted to users with owner or manager roles.

## Database Operations (`db.py`)

The database functions include:

- `get_loyalty_by_company_id`: Fetches all loyalty programs for a given company.
- `get_loyalty_by_id`: Retrieves a specific loyalty program by its ID.
- `post_loyalty`: Inserts a new loyalty program into the database.
- `delete_loyalty_by_id`: Removes a loyalty program from the database.

## Models (`model.py`)

This file defines the following models:

- `LoyaltyModel`: The main model for a loyalty program.
- `LoyaltyCreateModel`: Model for creating a new loyalty program.

## Validation Checks (`check.py`)

Contains functions to validate:

- `loyalty_matches_company`: Ensures the loyalty program is associated with the correct company based on the user's company data.
