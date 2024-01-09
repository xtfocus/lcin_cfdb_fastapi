from fastapi import FastAPI

from app.api import (editor_summary, en_concept, en_main_validate,
                     table_summary, vn_concept)
from app.login import login
from app.secure import secure

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


app.include_router(secure.router)
app.include_router(login.router)
app.include_router(table_summary.router)
app.include_router(vn_concept.router)
app.include_router(en_concept.router)
app.include_router(en_main_validate.router)
app.include_router(editor_summary.router)


# ... (other imports and configurations)

# Route to serve the login form HTML
