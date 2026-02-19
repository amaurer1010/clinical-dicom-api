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
    slice_thickness: Optional[str] = None
    number_of_slices: Optional[str] = None
    series_description: Optional[str] = None
    study_description: Optional[str] = None
    cardiac_trigger: Optional[str] = None
    trigger_delay: Optional[str] = None
    heart_rate: Optional[str] = None
    manufacturer: Optional[str] = None
    manufacturer_model: Optional[str] = None

class SummaryResponse(BaseModel):
    metadata: DicomMetadata
    summary: str


class CompareResponse(BaseModel):
    file1_metadata: DicomMetadata
    file2_metadata: DicomMetadata
    comparison: str