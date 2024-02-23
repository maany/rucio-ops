from pydantic import BaseModel

class ChecksumMismatch(BaseModel):
    timestamp: str
    activity: str
    scope: str
    name: str
    reason: str
    type: str
    source_rse: str
    destination_rse: str
    duration: str
    file_size: str
    fts_link: str
    source_url: str
    destination_url: str
    protocol: str
    size: int
    