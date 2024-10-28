import datetime
from pydantic import BaseModel
from typing import Literal
from pandas import DataFrame as Dataframe
from rucio.common.types import InternalScope, InternalAccount

class TimeRangeSourceData(BaseModel):
    start: datetime.datetime
    end: datetime.datetime
    file: str
    source: Literal['SEAL'] | Literal['RUCIO'] | Literal['SEAL_ENTRIES'] | Literal['SEAL_ERRORS']
    df: Dataframe

    class Config:
        arbitrary_types_allowed = True


class Replica(BaseModel):
    scope: InternalScope
    name: str
    rse_id: str

class DeclareBadReplicaRequest(BaseModel):
    replicas: list[Replica]
    reason: str

class DeclareBadReplicaSuccessResponse(BaseModel):
    status: Literal['OK'] 
    scope: InternalScope
    name: str
    rse_id: str
    state: Literal['BAD']
    updated_at: datetime.datetime
    reason: str

class DeclareBadReplicaErrorResponse(BaseModel):
    status: Literal['ERROR']
    scope: InternalScope
    name: str
    rse_id: str
    state: Literal['BAD']
    updated_at: datetime.datetime
    reason: str
    error: str