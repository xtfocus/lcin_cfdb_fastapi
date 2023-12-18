from enum import Enum

from pydantic import BaseModel


class SlackName(str, Enum):
    admin = "tungnx28"
    chanh = "chanhnh"
    dai = "daitt5"
    truc = "trucvhc"


class User(BaseModel):
    name: str
    email: SlackName
