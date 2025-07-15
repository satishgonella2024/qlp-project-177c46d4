from pydantic import BaseModel
import platform

class VersionResponse(BaseModel):
    version: str
    python_version: str
    platform: str