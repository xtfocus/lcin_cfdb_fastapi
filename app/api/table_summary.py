from app import crud
from app.db.db_setup import get_db
from app.db.dictionary import TableName
from app.pydantic_schemas.table import TableModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

router = APIRouter()


# @router.get("/table/info/{table_name}", response_model=int)
# def table_info(table_name: TableName, db: Session = Depends(get_db)):
#    db_table = crud.get_table(table_name.value, metadata, engine)
#    nrows = crud.get_count(db, db_table)
#
#    return nrows


@router.get("/table/summary/{table_name}", response_model=TableModel)
async def table_summary(table_name: TableName, db: Session = Depends(get_db)):
    db_table = crud.get_table(table_name.value)
    return_dict = crud.get_table_summary(db, db_table)

    return return_dict
