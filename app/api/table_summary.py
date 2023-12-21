from app import crud
from app.db.db_setup import get_db
from app.db.dictionary import TableName
from app.pydantic_schemas.table import TableModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/table/summary/{table_name}", response_model=TableModel)
async def table_summary(table_name: TableName, db: Session = Depends(get_db)):
    """
    Showing table information including number of rows, columns, PK, FK, etc.
    """
    db_table = crud.get_table(table_name.value)
    return_dict = crud.get_table_summary(db, db_table)

    return return_dict
