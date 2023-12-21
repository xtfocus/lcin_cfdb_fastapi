from app import crud
from app.pydantic_schemas.status import UnchartedStatus, ValidationStatus
from fastapi import APIRouter

router = APIRouter()


@router.get("/status/validate", response_model=ValidationStatus)
async def validation_status():
    """
    Showing validation status of the en_main values in the dictionary table
    """

    return crud.validated_en_main_statistics(crud.en_vsrc_tables)


@router.get("/status/uncharted_en_main", response_model=UnchartedStatus)
async def uncharted_en_main():
    """
    Showing the en_main values in the dictionary that are not mapped to any validation sources
    """
    return {
        "uncharted_en_mains": crud.calculate_non_validated_en_main(crud.en_vsrc_tables)
    }
