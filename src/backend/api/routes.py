from fastapi import APIRouter
from services.room_service import fetch_all_rooms

router = APIRouter()

@router.get("/rooms", tags=["Rooms"])
def get_rooms():
    return fetch_all_rooms()
