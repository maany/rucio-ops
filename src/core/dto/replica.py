from typing import Literal
from pydantic import BaseModel


class BadReplicaDeclarationSuccessDTO(BaseModel):
    success: True

class BadReplicaDeclarationFailureDTO(BaseModel):
    success: False
    type: Literal["AlreadyDeclared", "NotFound", "Other"]
    error: str