from pydantic import BaseModel
from typing import Optional

class DicomMetadata(BaseModel):
    patient_id: Optional[str] = None
    modality: Optional[str] = None
    study_date: Optional[str] = None
    body_part: Optional[str] = None
    institution: Optional[str] = None
    rows: Optional[int] = None
    columns: Optional[int] = None
    pixel_spacing: Optional[str] = None

class SummaryResponse(BaseModel):
    metadata: DicomMetadata
    summary: str