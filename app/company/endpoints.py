import fastapi

router = fastapi.APIRouter()

@router.get("/", tags=["", ""], status_code=201)
async def get_all_companies():
    return {}