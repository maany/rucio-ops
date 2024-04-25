import datetime
from pydantic import BaseModel
from typing import Literal

class TimeRangeSourceData(BaseModel):
    start: datetime.datetime
    end: datetime.datetime
    file: str
    source: Literal['SEAL'] | Literal['Rucio']

