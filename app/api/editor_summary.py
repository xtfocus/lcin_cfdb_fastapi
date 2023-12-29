from app import crud
from fastapi import APIRouter

router = APIRouter()


@router.get("/summary/editor/insert_count")
async def editor_insert_counts():
    """
    Show the number of inserted rows contributed per editor
    """
    result = crud.rows_per_editors(mode="insert")
    return result


@router.get("/summary/editor/update_count")
async def editor_update_counts():
    """
    Show the number of updated rows contributed per editor
    """
    result = crud.rows_per_editors(mode="update")
    return result
