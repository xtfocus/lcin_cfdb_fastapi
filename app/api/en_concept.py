from app import crud
from app.db.db_setup import engine
from app.db.dictionary import metadata
from app.pydantic_schemas.concept import ViConceptModel
from fastapi import APIRouter

router = APIRouter()


@router.get("/concept/en/{en_term}")
def discover_en_term(en_term: str):
    return "route not available"
