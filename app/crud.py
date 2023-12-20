from itertools import chain
from typing import List, Union

from sqlalchemy import MetaData, Table
from sqlalchemy.engine import Engine
from sqlalchemy.engine.base import Connection
from sqlalchemy.engine.row import Row
# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import Session

from app.db.db_setup import engine
from app.db.dictionary import metadata
from app.pydantic_schemas.table import TableModel

dictionary_table = Table("tungdev_DICTIONARY", metadata, autoload_with=engine)
vn_synonym_table = Table("tungdev_VN_SYNONYM", metadata, autoload_with=engine)

en_vsrc_tables = [
    Table(f"tungdev_EN_{src}", metadata, autoload_with=engine) for src in ["DO"]
]
en_vsrc_synonym_tables = [
    Table(f"tungdev_{src}_SYNONYM", metadata, autoload_with=engine) for src in ["DO"]
]


def get_count(db: Session, table: Table) -> int:
    """
    Count the number of rows in the given table.

    Parameters
    ----------
    db : Session
        SQLAlchemy Session.
    table : Table
        SQLAlchemy Table object.

    Returns
    -------
    int
        Number of rows in the table.
    """
    return db.query(table).count()


def get_table(table_name) -> Table:
    """
    Given the table name, return the SQLAlchemy Table object.

    Parameters
    ----------
    table_name : str
        Name of the table.
    metadata : MetaData
        SQLAlchemy MetaData object.
    engine : Engine
        SQLAlchemy Engine object.

    Returns
    -------
    Table
        SQLAlchemy Table object.
    """
    return Table(table_name, metadata, autoload_with=engine)


def get_table_summary(db: Session, table: Table) -> TableModel:
    """
    Given the table, return the TableModel object.

    Parameters
    ----------
    db : Session
        SQLAlchemy Session.
    table : Table
        SQLAlchemy Table object.
    engine : Engine
        SQLAlchemy Engine object.

    Returns
    -------
    TableModel
        Instance of the TableModel representing the table summary.
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


def locate_vn_term(term: str) -> Union[None, str, str, List[str], List[str]]:
    """
    Locate the Vietnamese term in the database.

    Parameters
    ----------
    term : str
        Vietnamese term to locate.
    metadata : MetaData
        SQLAlchemy MetaData object.
    engine : Engine
        SQLAlchemy Engine object.

    Returns
    -------
    Union[None, str, str, List[str], List[str]]
        Tuple containing Vietnamese main, English main, Vietnamese synonyms, and English synonyms.
    """

    with engine.connect() as conn:
        # Search in tungdev_DICTIONARY for a match
        dictionary_match = vn_main_in_dictionary(conn, term)

        if dictionary_match:
            vn_main = dictionary_match.VN_main
            en_main = dictionary_match.EN_main
        else:
            # If not found in tungdev_DICTIONARY, search in tungdev_VN_SYNONYM
            vn_main = vn_synonym_to_vn_main(conn, term)

            if vn_main:
                en_main = vn_main_in_dictionary(conn, vn_main).EN_main

            else:
                # If no matches found for vn_main
                return None, None, [None], [None]

        vn_synonyms = vn_main_to_synonyms(conn, vn_synonym_table, vn_main)
        en_synonyms = en_main_to_synonyms(
            conn, en_vsrc_tables, en_vsrc_synonym_tables, en_main
        )
        return vn_main, en_main, vn_synonyms, en_synonyms


def vn_synonym_to_vn_main(conn: Connection, vn_term: str):
    query_synonym = select(vn_synonym_table.c.VN_main).where(
        vn_synonym_table.c.VN_synonym == vn_term
    )
    result_main = conn.execute(query_synonym).fetchone()

    if result_main:
        vn_main = result_main.VN_main
        return vn_main
    else:
        return None


def vn_main_in_dictionary(conn: Connection, vn_main: str) -> Row:
    """
    Assuming vn_main 1:1 en_main. Find rows in
    dictionary_table where vn_main lies
    """
    match = conn.execute(
        select(dictionary_table).where(dictionary_table.c.VN_main == vn_main)
    ).fetchone()
    return match


def en_main_in_dictionary(conn: Connection, en_main: str) -> Row:
    """
    Assuming vn_main 1:1 en_main. Find rows in
    dictionary_table where en_main lies
    """
    match = conn.execute(
        select(dictionary_table).where(dictionary_table.c.EN_main == en_main)
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
    conn: Connection,
    en_vsrc_tables: List[Table],
    en_vsrc_synonym_tables: List[Table],
    en_main: str,
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


def en_term_to_en_main(conn: Connection, en_term: str):
    """
    Check if en_term corresponds to a known en_main
    """
    dictionary_match = conn.execute(
        select(dictionary_table).where(dictionary_table.c.EN_main == en_term)
    ).fetchone()
    if dictionary_match:
        return dictionary_match
    else:
        return None


def en_synonym_to_vsource(conn, src_synonym, en_synonym):
    match = conn.execute(
        select(src_synonym).where(src_synonym.c.EN_synonym == en_synonym)
    ).fetchone()

    if match:
        print("HEHEHE", match)
        return match
    else:
        return None


def en_synonym_to_en_main(conn, en_synonym):
    en_main = None
    for src, src_synonym in zip(en_vsrc_tables, en_vsrc_synonym_tables):
        primary_key = [i.name for i in src.primary_key.columns.values()][0]
        src_synonym_match = en_synonym_to_vsource(conn, src_synonym, en_synonym)
        if src_synonym_match:
            print(primary_key)
            print(type(src_synonym_match))

            # NEEED CHANGE
            src_code = src_synonym_match._asdict()[primary_key]

            print("found", src_code)

            en_main = (
                conn.execute(
                    select(src.c.EN_main).where(src.c[primary_key] == src_code)
                )
                .fetchone()
                .EN_main
            )
            return en_main
    return en_main


def locate_en_term(en_term: str):
    with engine.connect() as conn:
        dictionary_match = en_term_to_en_main(conn, en_term)

        if dictionary_match:
            en_main = dictionary_match.EN_main
            vn_main = dictionary_match.VN_main

        else:
            en_main = en_synonym_to_en_main(conn, en_term)
            if en_main:
                vn_main = en_main_in_dictionary(conn, en_main).VN_main
            else:
                return None, None

    return vn_main, en_main


#        dictionary_match = conn.execute(
#            select(dictionary_table.c.EN_main).where(
#                dictionary_table.c.EN_main == en_term
#            )
#        ).fetchone()
#
#        if dictionary_match:
#            en_main = dictionary_match.EN_main
#        else:
#            for src, src_synonym in zip(en_vsrc_tables, en_vsrc_synonym_tables):
#                primary_key = [i.name for i in src.primary_key.columns.values()][0]
#
#                # find the matched value of DOID/CUI
#                src_synonym_match = conn.execute(
#                    select(src_synonym.c[primary_key]).where(
#                        src_synonym.c.EN_synonym == en_term
#                    )
#                ).fetchone()[0]
#
#                if src_synonym_match:
#                    en_main = conn.execute(
#                        select(src.c.EN_main).where(
#                            src.c[primary_key] == src_synonym_match
#                        )
#                    ).fetchone()
#                else:
#                    return None, None, [None], [None]
