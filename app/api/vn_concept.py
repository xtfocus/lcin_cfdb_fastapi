from app import crud
from app.db.db_setup import engine
from app.db.dictionary import metadata
from app.pydantic_schemas.concept import ViConceptModel
from fastapi import APIRouter

router = APIRouter()


@router.get("/concept/vi/{vi_term}", response_model=ViConceptModel)
def discover_vi_term(vi_term: str):
    vn_main, en_main, vn_synonyms = crud.locate_vn_term(vi_term, metadata, engine)
    return {"vn_main": vn_main, "en_main": en_main, "vn_synonyms": vn_synonyms}
