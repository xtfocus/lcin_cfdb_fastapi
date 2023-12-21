from fastapi import FastAPI

from app.api import en_concept, en_main_validate, table_summary, vn_concept

app = FastAPI(
    title="LCIN Dictionary Fast API",
    description="Dictionary API for clinical finding terminology",
    version="0.0.1",
    contact={
        "name": "Tung",
        "email": "tungxuan0111@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
)

app.include_router(table_summary.router)
app.include_router(vn_concept.router)
app.include_router(en_concept.router)
app.include_router(en_main_validate.router)
