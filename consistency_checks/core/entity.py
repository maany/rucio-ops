import datetime
from pydantic import BaseModel
from typing import Literal
from pandas import DataFrame as Dataframe

class TimeRangeSourceData(BaseModel):
    start: datetime.datetime
    end: datetime.datetime
    file: str
    source: Literal['SEAL'] | Literal['RUCIO'] | Literal['SEAL_ENTRIES'] | Literal['SEAL_ERRORS']
    df: Dataframe

    class Config:
        arbitrary_types_allowed = True
