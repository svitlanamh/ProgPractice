from typing import Optional
from pydantic import BaseModel, Field

class Block(BaseModel):
    block_id: str = Field(pattern=r"^[0-9a-fA-F]{8}$")
    view: int = Field(ge=0)
    desc: Optional[str] = Field(default=None)

class Person(BaseModel):
    name: str = Field(min_length=1, pattern= r"^[A-Za-z]+\ [A-Za-z]+$")
    addr: str = Field(min_length=1)

class Source(BaseModel):
    ip_addr: str = Field(pattern=r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    country_code: str = Field(min_length=2, max_length=2)

class Vote(BaseModel):
    voter_id: int = Field(gt=10000)
    block_id: str = Field(pattern=r"^[0-9a-fA-F]{8}$")
    source_id: int = Field(gt=0)