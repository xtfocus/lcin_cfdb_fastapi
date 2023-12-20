from app import crud
from app.db.db_setup import engine
from app.db.dictionary import metadata
from app.pydantic_schemas.concept import ViConceptModel
from fastapi import APIRouter

router = APIRouter()


@router.get("/concept/en/{en_term}")
async def discover_en_term(en_term: str):
    """
    If term not mapped to any source (CUI, DO), return error
    Else, return  the corresponding ViConceptModel of the corresponding
    """

    return crud.locate_en_term(en_term)
