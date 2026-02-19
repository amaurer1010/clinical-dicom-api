import pydicom
from app.schemas import DicomMetadata

def extract_metadata(file_bytes: bytes) -> DicomMetadata:
    import io
    ds = pydicom.dcmread(io.BytesIO(file_bytes))

    def get(tag, default=None):
        try:
            return str(getattr(ds, tag))
        except AttributeError:
            return default

    return DicomMetadata(
        patient_id=get("PatientID"),
        modality=get("Modality"),
        study_date=get("StudyDate"),
        body_part=get("BodyPartExamined"),
        institution=get("InstitutionName"),
        rows=int(ds.Rows) if hasattr(ds, "Rows") else None,
        columns=int(ds.Columns) if hasattr(ds, "Columns") else None,
        pixel_spacing=get("PixelSpacing"),
        slice_thickness=get("SliceThickness"),
        number_of_slices=get("NumberOfSlices"),
        series_description=get("SeriesDescription"),
        study_description=get("StudyDescription"),
        cardiac_trigger=get("TriggerSourceOrType"),
        trigger_delay=get("TriggerDelayTime"),
        heart_rate=get("HeartRate"),
        manufacturer=get("Manufacturer"),
        manufacturer_model=get("ManufacturerModelName"),
    )