from fastapi import APIRouter

router = APIRouter()


@router.get("/", response_description="List all cars")
async def list_cars():
    return {"data": "All cars will go here."}
