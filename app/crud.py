from itertools import chain
from typing import List

from sqlalchemy import MetaData, Table
from sqlalchemy.engine import Engine
from sqlalchemy.engine.base import Connection
from sqlalchemy.engine.row import Row
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session

from app.pydantic_schemas.table import TableModel


def get_count(db: Session, table: Table) -> int:
    """
    Count the number of rows in table
    """
    return db.query(table).count()


def get_table(table_name: str, metadata: MetaData, engine: Engine) -> Table:
    """
    Given the table_name, return the Table object

    """
    return Table(table_name, metadata, autoload_with=engine)


def get_table_summary(db: Session, table: Table, engine: Engine) -> TableModel:
    """
    Given the table_name, return the TableModel object
    """
    name = table.name
    n_rows = get_count(db, table)
    columns = list(table.columns.keys())

    inspector = inspect(engine)

    primary_key = [key.name for key in table.primary_key]

    foreign_key = inspector.get_foreign_keys(table.name)
    columns = inspector.get_columns(table.name)

    return {
        "name": name,
        "n_rows": n_rows,
        "columns": columns,
        "primary_key": primary_key,
        "foreign_key": foreign_key,
        "columns": columns,
    }


def locate_vn_term(term: str, metadata: MetaData, engine: Engine):
    """ """
    dictionary_table = Table("tungdev_DICTIONARY", metadata, autoload_with=engine)
    vn_synonym_table = Table("tungdev_VN_SYNONYM", metadata, autoload_with=engine)

    en_vsrc_tables = (
        Table(f"tungdev_EN_{src}", metadata, autoload_with=engine)
        for src in [
            "DO",
        ]
    )
    en_vsrc_synonym_tables = (
        Table(f"tungdev_{src}_SYNONYM", metadata, autoload_with=engine)
        for src in [
            "DO",
        ]
    )

    with engine.connect() as conn:
        # Search in tungdev_DICTIONARY for a match
        dictionary_match = vn_main_in_dictionary(conn, dictionary_table, term)

        if dictionary_match:
            vn_main = dictionary_match.VN_main
            en_main = dictionary_match.EN_main
        else:
            # If not found in tungdev_DICTIONARY, search in tungdev_VN_SYNONYM
            query_synonym = select(vn_synonym_table.c.VN_main).where(
                vn_synonym_table.c.VN_synonym == term
            )
            result_synonym = conn.execute(query_synonym).fetchone()

            if result_synonym:
                vn_main = result_synonym.VN_main
                en_main = vn_main_in_dictionary(conn, dictionary_table, vn_main).EN_main

        vn_synonyms = vn_main_to_synonyms(conn, vn_synonym_table, vn_main)
        en_synonyms = en_main_to_synonyms(
            conn, en_vsrc_tables, en_vsrc_synonym_tables, en_main
        )
        return vn_main, en_main, vn_synonyms, en_synonyms

    return None, None, [None], [None]


def vn_main_in_dictionary(
    conn: Connection, dictionary_table: Table, vn_main: str
) -> Row:
    """
    Assuming vn_main 1:1 en_main. Find rows in
    dictionary_table where vn_main lies
    """
    match = conn.execute(
        select(dictionary_table).where(dictionary_table.c.VN_main == vn_main)
    ).fetchone()
    return match


def vn_main_to_synonyms(
    conn: Connection, vn_synonym_table: Table, vn_main: str
) -> List[str]:
    """
    Assuming vn_main 1:1 en_main. Find rows in
    dictionary_table where vn_main lies
    """

    match = conn.execute(
        select(vn_synonym_table.c.VN_synonym).where(
            vn_synonym_table.c.VN_main == vn_main
        )
    ).fetchall()
    match = [i.VN_synonym for i in match]
    return match


def en_main_to_vsource_id(conn: Connection, en_vsrc_table: Table, en_main: str) -> str:
    primary_key = [i.name for i in en_vsrc_table.primary_key.columns.values()][0]

    en_vsrc_match = conn.execute(
        select(en_vsrc_table.c[primary_key]).where(en_vsrc_table.c.EN_main == en_main)
    ).fetchone()[0]

    return en_vsrc_match


def en_main_to_synonyms(
    conn, en_vsrc_tables: List[Table], en_vsrc_synonym_tables: List[Table], en_main: str
) -> List[str]:
    return_list = []

    for src, src_synonym in zip(en_vsrc_tables, en_vsrc_synonym_tables):
        primary_key = [i.name for i in src.primary_key.columns.values()][0]
        src_match = en_main_to_vsource_id(conn, src, en_main)

        synonym_match = conn.execute(
            select(src_synonym.c.EN_synonym).where(
                src_synonym.c[primary_key] == src_match
            )
        ).fetchall()
        synonym_match = [i[0] for i in synonym_match]
        return_list += synonym_match

    return return_list
