# app
This folder contains all logic behind OmegaPoint system. The logic is divided into separate components (folders). Most of the components here were defined in the specification document, however there are some extra ones (like `JWT_auth`, `db_connection.py`) that do some separate logical task and help all the other components.

## Recommend Component Structure
All of the predefined components: company, users, items, services, orders, payments - are similar in the sense that they need to have some endpoints defined, do some database operations and return some output. Therefore it is highly recommended that each of these components follow this structure:

### `endpoints.py`
You should define all of your endpoints in here. Also your endpoints must return according to these rules:
* `{"data" : data}` - when returning some data.
* `{"info" : success_message}` - when some operation was successful.
* `raise fastapi.HTTPException` - when something is wrong, provide detail.
* `{"token" : token}` - after succesful login.
* All messages should start with non-capital letter and end without a dot.

Here is an example:
```python
import fastapi
import app.company.db as db
from mysql.connector import Error as DBError

router = fastapi.APIRouter() # This router object must be included in my_app.py for your endpoints to start working

# An endpoint that is accessible to anyone, even to the users who haven't logged in
@router.get("/cinematic/company", tags=["company"], status_code=200)
async def get_all_companies():
    try:
        return {"data" : db.get_all_companies()}
    except DBError:
        raise fastapi.HTTPException(status_code=500, detail="database error")

# Other endpoints go here...
```

#### Note
For steps on how to use autorization, refer to `JWT_auth` component README.md.

### `db.py`
Functions that send queries to database should be only here. Additionally I highly recommend leaving the logic out of this module and only defining basic database operations here. I also recommend not handling the mysql.connector.Error in here, instead handle these errors in your endpoints or other modules that use `db.py`. 

Here is an example:
```python
from app.db_connection import mysql_connection
from app.company.model import CompanyModel
from typing import List, Optional

connection = mysql_connection() # Create a connection object by using db_connection.py module


def get_all_companies() -> List[CompanyModel]:
    query = "SELECT id, email, name, created_at FROM company"
    cursor = connection.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    companies = []
    for row in rows:
        company = CompanyModel(id=row[0], email=row[1], name=row[2], created_at=row[3])
        companies.append(company)
    return companies
```

### `model.py`
Here you should define your classes for data transfer. FastAPI uses `Pydantic.BaseModel` to automatically parse incoming JSON into an object.

Here is an example:
```python
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class CompanyModel(BaseModel):
    id: int = Field(default=None)
    email: EmailStr
    name: str
    created_at: datetime = Field(default=None)

    # This is optional, but is used by fastAPI docs, it automatically apears as an example JSON message
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "UAB gpt technologies"
            }
        }
```

### Extra
If you need, you can always define additional modules in your package. If your package has a lot of logic going on it is very natural to separate that logic into another file. If your component is fairly big, you should also consider splitting your component into a few sub components. For example in `users` there is a sub component `roles`.

### Notes
Don't forget to add your database initialization files to `database_init` folder. For more information about users and authorization refer to `users` and `JWT_auth` README.md files.
