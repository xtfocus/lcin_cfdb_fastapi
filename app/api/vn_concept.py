from app import crud
from app.db.db_setup import engine
from app.pydantic_schemas.concept import ViConceptModel
from fastapi import APIRouter, HTTPException, Path

router = APIRouter()

# The path parameter to be used in following routes
vi_term_path = Path(
    default=..., description="any possible Vietnamese clinical finding term"
)


@router.get("/concept/vi/{vi_term}", response_model=ViConceptModel)
async def discover_vi_term(vi_term: str = vi_term_path):
    """
    If Vietnamese term vi_term is not a known vn_main or vn_synonym, return error
    else, return the details of the concept

    """
    vn_main, en_main, vn_synonyms, en_synonyms, en_main_vsrc = crud.locate_vn_term(
        vi_term
    )

    if vn_main is None:
        raise HTTPException(status_code=404, detail=f"{vi_term} not found in database")
    return {
        "vn_main": vn_main,
        "en_main": en_main,
        "vn_synonyms": vn_synonyms,
        "en_synonyms": en_synonyms,
        "en_main_vsrc": en_main_vsrc,
    }


@router.get("/term/vi/{vi_term}", response_model=bool)
async def check_vn_term_exist(vi_term: str = vi_term_path) -> bool:
    """
    Check if Vietnamese term vn_term exists in the database
    """

    found = False
    with engine.connect() as conn:
        if crud.vn_synonym_to_vn_main(conn, vi_term) or crud.vn_main_in_dictionary(
            conn, vi_term
        ):
            found = True

    return found
