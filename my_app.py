# !Python basics:

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

import fastapi

from app.users.endpoints import router as users_router
from app.company.endpoints import router as company_router
from app.users.roles.endpoints import router as roles_router

app = fastapi.FastAPI()


app.include_router(users_router)
app.include_router(company_router)
app.include_router(roles_router)

