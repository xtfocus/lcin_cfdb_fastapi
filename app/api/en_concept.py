from app import crud
from app.db.db_setup import engine
from app.pydantic_schemas.concept import ViConceptModel
from fastapi import APIRouter, HTTPException

router = APIRouter()


# @router.get("/concept/en/{en_term}", response_model=ViConceptModel)
@router.get("/concept/en/{en_term}", response_model=ViConceptModel)
async def discover_en_term(en_term: str):
    """
    If term not mapped to any source (CUI, DO), return error
    Else, return  the corresponding ViConceptModel of the corresponding
    """
    vn_main, en_main, vn_synonyms, en_synonyms = crud.locate_en_term(en_term)
    if en_main is None:
        raise HTTPException(status_code=404, detail=f"{en_term} not found in database")

    return {
        "vn_main": vn_main,
        "en_main": en_main,
        "vn_synonyms": vn_synonyms,
        "en_synonyms": en_synonyms,
    }


@router.get("/term/en/{en_term}")
async def check_en_term_exist(en_term: str) -> bool:
    """
    Check if English term en_term exists in the database
    """

    found = False
    with engine.connect() as conn:
        if crud.en_term_to_en_main(conn, en_term) or crud.en_synonym_to_en_main(
            conn, en_term
        ):
            found = True

    return found
