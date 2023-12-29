# OmegaPoint Specification
This is where the architecture of OmegaPoint system is defined. These two files were provided to us before implementing the system and act as guidelines for how to implement OmegaPoint:
* **`PSP lab2 OmegaPoint OpenAPI.json`** - is the endpoints specification file.
* **`PSP_Lab2_OmegaPoint.pdf`** - is the general specification document.

However, we made many significant changes, due to errors in specification. The changes made will be reflected in this `README.md` file.

## Changes

### {company_id} and {user_id}
Most endpoints contain company id and user id as endpoint parameters, however there is no reason to pass these parameters as the user will have to be authenticated anyways. You can't just authenticate a user who claims to be of id = 5. Besides there isn't a good way to know which company id to send. Are you going to query all companies and pick one from the list of all? (The omega point team said that each company will have its own unique front end and the company id will be embedded there) - fair, but still no reason to send company id, as it will have to be checked through authorization anyways. So, for these reasons – we will remove company_id and user_id from most of the endpoints (the endpoints where they are used for authorization). Finally, after logging in, the user will receive JWT, which will contain encrypted user identification information. (Authenticated user`s company id and user id will be determined from the JWT. user_id as a parameter should only be used to interact with other users.)

### Some Endpoints Overlap
Some endpoints have overlapping structure. Therefore, they will be structured to start with the component name first.

## Final Endpoints

### User registration/login
* `POST /cinematic/users/register` - Register a regular user.
* `POST /cinematic/users/login` - Login for all users.
* `POST /cinematic/users/company/owner/register` - Register a company owner user, done by the system administrators only.
* `POST /cinematic/users/company/manager/register` - Register a company manager user, done by the company owner users only.
* `POST /cinematic/users/company/employee/register` - Register a company employee user, done by the company manager users and company owner users only.

### Company user management endpoints (accessible to mangers/owners only)
* `GET /cinematic/users/company` - Get all company users.
* `GET /cinematic/users/company/{user_id}` - Get a specific user from the company.
* `PUT /cinematic/users/company/{user_id}` - Update company employee (EXCEPT Owner/Manager), Owner can update any user.
* `DELETE /cinematic/users/company/{user_id}` - Delete user, that was created by that company (EXCEPT Owner/Manager), Owner can delete any user.

### Company role management endpoints (accessible to mangers/owners only)
* `GET /cinematic/roles/company` - Get all company roles.
* `GET /cinematic/roles/company/{role_id}` - Get a specific role.
* `POST /cinematic/roles/company` - Add a role.
* `PUT /cinematic/roles/company/{role_id}` - Edit an existing role.
* `DELETE /cinematic/roles/company/{role_id}` - Delete a role.

### Company role assignement endpoints (accessible to mangers/owners only) [EXTRA]
* `GET /cinematic/roles/users/byuser/{user_id}` - Get all user's roles.
* `GET /cinematic/roles/users/byrole/{role_id}` - Get all users with that role assigned.
* `POST /cinematic/roles/users/{role_id}/{user_id}` - Assign a role.

### Users loyalty endpoints [REDONE] -> Company loyalty endpoints (all company employees can read, only managers/owners can write)
* `GET /cinematic/loyalty` - Get all company loyalty items.
* `GET /cinematic/loyalty/{id}` - Get specific loyalty item.
* `POST /cinematic/loyalty` - Add loyalty item.
* `DELETE /cinematic/loyalty/{id}` - Delete loyalty item.

### Company endpoints
* `GET /cinematic/company` - Get all companies, accessible to anyone.
* `GET /cinematic/company/{company_id}` - Get specific company, accessible to anyone.
* `POST /cinematic/company` - Create a company, only accessible to system administrators.
* `PUT /cinematic/company` - Edit company details, only accessible to company owners.
* `DELETE /cinematic/company` - Delete a company, only accessbile to system administrators only.

### Services endpoints
* `GET /cinematic/services` - Get all company services.
* `GET /cinematic/services/{service_id}` - Get a specific company service.
* `POST /cinematic/services` - Create a service.
* `PUT /cinematic/services/{service_id}` - Edit a specific service.
* `DELETE /cinematic/services/{service_id}` - Delete a specific service.
* `POST /cinematic/services/{service_id}/discounts` - Create a service discount.

### Appointments endpoints
* `GET /cinematic/appointments` - Get all company appointments.
* `GET /cinematic/appointments/{appointment_id}` - Get a specific appointment.
* `POST /cinematic/appointments` - Create an appointment.
* `PUT /cinematic/appointments` - Edit an appointment.
* `DELETE /cinematic/appointments` - Delete an appointment.

### Store endpoints
*  `GET /cinematic/stores` - Get all stores.
* `GET /cinematic/stores/{store_id}` - Get specific company.
* `POST /cinematic/stores` - Create a store, only accesible to owners and managers.
* `PUT /cinematic/stores/{store_id}` - Edit store details, only accesible to owners and managers.
* `DELETE /cinematic/stores/{store_id}` - Delete a store, only accesible to owners and managers.
