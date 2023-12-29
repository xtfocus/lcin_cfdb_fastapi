from app import crud
from fastapi import APIRouter

router = APIRouter()


@router.get("/summary/editor_contribution")
async def editor_row_counts():
    """
    Show the number of rows contributed per editor
    """
    result = crud.rows_per_editors()
    return result
