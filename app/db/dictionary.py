from enum import Enum

from app.db.db_setup import engine
from sqlalchemy import MetaData, Table
from sqlalchemy.engine import Engine

# Reflect the existing CID_DISEASE_ONTOLOGY_ALL table from the database
metadata = MetaData()

# TRANSLATION = Table("tungdev_DICTIONARY", metadata, autoload_with=engine)
# EN_UMLS = Table("tungdev_EN_UMLS", metadata, autoload_with=engine)
# EN_DO = Table("tungdev_EN_DO", metadata, autoload_with=engine)
# VN_SYNONYM = Table("tungdev_VN_SYNONYM", metadata, autoload_with=engine)
# EN_SYNONYM = Table("tungdev_EN_SYNONYM", metadata, autoload_with=engine)
# UMLS_SYNONYM = Table("tungdev_UMLS_SYNONYM", metadata, autoload_with=engine)
# DO_SYNONYM = Table("tungdev_DO_SYNONYM", metadata, autoload_with=engine)
#

"""
In the future I want to use ORM in this
"""


class TableName(str, Enum):
    TRANSLATION = "tungdev_DICTIONARY"
    EN_UMLS = "tungdev_EN_UMLS"
    EN_DO = "tungdev_EN_DO"
    VN_SYNONYM = "tungdev_VN_SYNONYM"
    tungdev_EN_SYNONYM = "tungdev_EN_SYNONYM"
    UMLS_SYNONYM = "tungdev_UMLS_SYNONYM"
    DO_SYNONYM = "tungdev_DO_SYNONYM"
