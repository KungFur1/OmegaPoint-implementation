# Create virtual environment:
# python -m venv MyVirtualEnvironment
# Activate it:
# .\MyVirtualEnvironment\Scripts\activate

# Install packages:
# pip install requests
# Save project configuration:
# pip freeze > requirements.txt
# ALTERNATIVE (Better, only saves packages that are used in the project):
# If you install some package and then stop using it, this method is better:
# pip install pipreqs
# pipreqs
# If requirements.txt already exists:
# pipreqs --force

# All packages are saved in virtual environments, so two virtual environments in the same project can have different packages installed
# install requirements.txt:
# pip install -r requirements.txt

# FastAPI:
# https://fastapi.tiangolo.com/
# pip install "fastapi[all]"
# Start local server:
# uvicorn my_app:app --reload
# Documentation is automatically generated and can be accessed through:
# base_url/docs
# If exception is raised and not handled FastAPI will automatically create an error response.



# Example program to get us started:

import fastapi
from pydantic import BaseModel
from typing import Optional # This is just used for coding to highlight that something is optional.

app = fastapi.FastAPI()

# Inventory will be used as mockup database, dictionary key will be used as ID:
inventory = {}


# Home page:
@app.get('/')
async def root():
    return {"data": "Welcome to main page."}


# Endpoints with parameters:
@app.get("/get-item/{item_id}/{extra_word}")
async def get_item(item_id: int, extra_word: str):
    if item_id not in inventory:
        raise fastapi.HTTPException(status_code=404, detail="Item not found, wrong ID.") # When you want to return error, raise exception.
    return inventory[item_id].name + extra_word


# Documentation of api parameters + value restrictions (gt = 0) - the parameter must be greater than 0:
@app.get("/get-item/{item_id}")
async def get_item(item_id: int = fastapi.Path(description="The ID of the item you would like to view.", gt=0, lt=9000)): # Set the description of item_id.
    if item_id not in inventory:
        raise fastapi.HTTPException(status_code=404, detail="Item not found, wrong ID.")
    return inventory[item_id]


# Example query parameters request: "facebook.com/home?redirect=tim&msg=fail" - two query parameters - redirect and msg
# Query parameters:
@app.get("/get-by-name") # /get-by-name?name=Milk&test=0
async def get_item(*, test:Optional[int] = None, name:str): # Make the query parameter optional by giving it default value, but then you have to add *, for other parameters to work.
    for item_id in inventory:
        if inventory[item_id].name == name:
            return inventory[item_id]
    raise fastapi.HTTPException(status_code=404, detail="Item not found, no item with such name.")
# You can also combine regular api parameters with query parameters!


# Request body (POST request):
class Item(BaseModel): # pydantic will automatically parse incoming json and cast it into this object
    name: str
    price: float
    brand: Optional[str] = None


@app.post("/create-item/{item_id}") # Since this is a POST request, it has to be tested in the docs
async def create_item(item_id:int, item: Item):
    if item_id in inventory:
        raise fastapi.HTTPException(status_code=404, detail="Item with this ID already created.")
    # inventory[item_id] = {"name": item.name, "price": item.price, "brand": item.brand}
    inventory[item_id] = item
    return inventory[item_id]


# PUT request:
class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    brand: Optional[str] = None


@app.put("/update-item/{item_id}")
async def update_item(item_id:int, item: UpdateItem):
    if item_id not in inventory:
        raise fastapi.HTTPException(status_code=404, detail="Item with this ID does not exist.")
    
    if item.name != None:
        inventory[item_id].name = item.name
    if item.price != None:
        inventory[item_id].price = item.price
    if item.brand != None:
        inventory[item_id].brand = item.brand
    return inventory[item_id]


# DELETE request:
@app.delete("/delete-item/{item_id}")
async def delete_item(item_id:int):
    if item_id not in inventory:
        raise fastapi.HTTPException(status_code=404, detail="Item not found, wrong ID")
    del inventory[item_id]
    return {"Success": "Item deleted."}