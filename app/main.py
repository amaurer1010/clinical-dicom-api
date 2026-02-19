from fastapi import FastAPI, UploadFile, File, HTTPException
from app.dicom_parser import extract_metadata
from app.llm_client import summarize_metadata
from app.schemas import DicomMetadata, SummaryResponse

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