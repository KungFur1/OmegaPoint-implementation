from fastapi import APIRouter, Depends, HTTPException, Body
import fastapi
from app.services.model import ServiceModel,ServicePostModel,ServiceUpdateModel
from app.services.db import get_all_services_for_company,get_service_by_id, create_service,update_service,delete_service
from app.JWT_auth.authorization import authorization_wrapper, get_complete_user_information
from app.JWT_auth.user_identification import UserIdentification
from app.db_error_handler import handle_db_error
import app.users.check as users_check
import app.services.check as check


router = fastapi.APIRouter()
