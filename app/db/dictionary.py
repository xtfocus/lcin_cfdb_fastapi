from enum import Enum

from sqlalchemy import MetaData

# Reflect the existing CID_DISEASE_ONTOLOGY_ALL table from the database
metadata = MetaData()


class TableName(str, Enum):
    TRANSLATION = "CID_LCIN_DICTIONARY"
    EN_UMLS = "CID_LCIN_EN_UMLS"
    EN_DO = "CID_LCIN_EN_DO"
    VN_SYNONYM = "CID_LCIN_VN_SYNONYM"
    CID_LCIN_EN_SYNONYM = "CID_LCIN_EN_SYNONYM"
    UMLS_SYNONYM = "CID_LCIN_EN_UMLS_SYNONYM"
    DO_SYNONYM = "CID_LCIN_EN_DO_SYNONYM"
    EDITOR = "CID_LCIN_EDITOR"
    VSOURCE = "CID_LCIN_VALIDATION_SOURCE"
