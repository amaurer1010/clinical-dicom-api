from fastapi import FastAPI, UploadFile, File, HTTPException
from app.dicom_parser import extract_metadata
from app.llm_client import summarize_metadata, compare_metadata
from app.fhir_converter import to_fhir_imaging_study
from app.schemas import DicomMetadata, SummaryResponse, CompareResponse, FHIRResponse

app = FastAPI(
    title="Clinical DICOM Analysis API",
    description="Extracts metadata from DICOM files and generates plain-language clinical summaries using LLM.",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.post("/dicom/analyze", response_model=DicomMetadata)
async def analyze_dicom(file: UploadFile = File(...)):
    if not file.filename.endswith(".dcm"):
        raise HTTPException(status_code=400, detail="File must be a .dcm DICOM file")
    contents = await file.read()
    try:
        return extract_metadata(contents)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not parse DICOM file: {str(e)}")

@app.post("/dicom/summarize", response_model=SummaryResponse)
async def summarize_dicom(file: UploadFile = File(...)):
    if not file.filename.endswith(".dcm"):
        raise HTTPException(status_code=400, detail="File must be a .dcm DICOM file")
    contents = await file.read()
    try:
        metadata = extract_metadata(contents)
        summary = summarize_metadata(metadata)
        return SummaryResponse(metadata=metadata, summary=summary)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error processing file: {str(e)}")
    

@app.post("/dicom/compare", response_model=CompareResponse)
async def compare_dicom(
    file1: UploadFile = File(...),
    file2: UploadFile = File(...)
):
    for f in [file1, file2]:
        if not f.filename.endswith(".dcm"):
            raise HTTPException(status_code=400, detail=f"{f.filename} must be a .dcm DICOM file")
    try:
        contents1 = await file1.read()
        contents2 = await file2.read()
        metadata1 = extract_metadata(contents1)
        metadata2 = extract_metadata(contents2)
        comparison = compare_metadata(metadata1, metadata2)
        return CompareResponse(
            file1_metadata=metadata1,
            file2_metadata=metadata2,
            comparison=comparison
        )
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error comparing files: {str(e)}")
    
@app.post("/dicom/fhir", response_model=FHIRResponse)
async def dicom_to_fhir(file: UploadFile = File(...)):
    if not file.filename.endswith(".dcm"):
        raise HTTPException(status_code=400, detail="File must be a .dcm DICOM file")
    try:
        contents = await file.read()
        metadata = extract_metadata(contents)
        fhir_resource = to_fhir_imaging_study(metadata)
        return FHIRResponse(resourceType="ImagingStudy", fhir_resource=fhir_resource)
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Error converting to FHIR: {str(e)}")    