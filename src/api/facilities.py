from datetime import date
from fastapi import Query, Body, APIRouter
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException
from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd


router = APIRouter(prefix="/facilities", tags=["Удобства"])


@router.get("")
async def get_all_facilities(db: DBDep):
    return await db.facilities.get_all()


@router.post("")
async def create_facility(db: DBDep,
                          facility_data: FacilityAdd = Body(openapi_examples={
        "1": {
            "summary": "Удобство",
            "value": {
                "title": "Чайник"
            }
        },
    })
    ):
    await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility_data}