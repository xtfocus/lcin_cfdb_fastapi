from app import crud
from app.db.db_setup import engine
from app.pydantic_schemas.concept import ViConceptModel
from fastapi import APIRouter, HTTPException, Path

router = APIRouter()

# The path parameter to be used in following routes
en_term_path = Path(
    default=..., description="any possible English clinical finding term"
)


@router.get("/concept/en/{en_term}", response_model=ViConceptModel)
async def discover_en_term(en_term: str = en_term_path):
    """
    If English term en_term is not a known en_main or en_synonym, return error
    else, return the details of the concept
    """
    vn_main, en_main, vn_synonyms, en_synonyms, en_main_vsrc = crud.locate_en_term(
        en_term
    )
    if en_main is None:
        raise HTTPException(status_code=404, detail=f"{en_term} not found in database")

    return {
        "vn_main": vn_main,
        "en_main": en_main,
        "vn_synonyms": vn_synonyms,
        "en_synonyms": en_synonyms,
        "en_main_vsrc": en_main_vsrc,
    }


@router.get("/term/en/{en_term}", response_model=bool)
async def check_en_term_exist(en_term: str = en_term_path) -> bool:
    """
    Check if English term en_term exists in the database
    """

    found = False
    with engine.connect() as conn:
        if crud.en_main_in_dictionary(conn, en_term) or crud.en_synonym_to_en_main(
            conn, en_term
        ):
            found = True

    return found
