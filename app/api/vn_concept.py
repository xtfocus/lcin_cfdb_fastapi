from app import crud
from app.db.db_setup import engine
from app.pydantic_schemas.concept import ViConceptModel
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/concept/vi/{vi_term}", response_model=ViConceptModel)
def discover_vi_term(vi_term: str):
    vn_main, en_main, vn_synonyms, en_synonyms = crud.locate_vn_term(vi_term)

    if vn_main is None:
        raise HTTPException(status_code=404, detail=f"{vi_term} not found in database")
    return {
        "vn_main": vn_main,
        "en_main": en_main,
        "vn_synonyms": vn_synonyms,
        "en_synonyms": en_synonyms,
    }


@router.get("/term/vi/{vn_term}")
async def check_vn_term_exist(vn_term: str) -> bool:
    """
    Check if Vietnamese term vn_term exists in the database
    """

    found = False
    with engine.connect() as conn:
        if crud.vn_synonym_to_vn_main(conn, vn_term) or crud.vn_main_in_dictionary(
            conn, vn_term
        ):
            found = True

    return found
