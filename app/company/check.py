from fastapi import HTTPException
import app.company.db as db


def company_exists(company_id: int):
    if db.get_company_by_id(company_id) is None:
        raise HTTPException(status_code=400, detail="company_exists CHECK: failed")
