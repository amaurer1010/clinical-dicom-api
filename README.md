# Clinical DICOM Analysis API

A FastAPI service that extracts structured metadata from DICOM medical imaging files, generates plain-language clinical summaries using the Anthropic Claude API, and converts studies to FHIR ImagingStudy resources for health system interoperability.

Built with the assistance of Claude  as a portfolio project to demonstrate healthcare domain knowledge combined with modern backend development — directly relevant to clinical workflow integration work.

---

## Development Approach

This project was built collaboratively with Claude (Anthropic) as a learning and portfolio exercise. The domain knowledge — DICOM workflows, cardiac gating parameters, clinical imaging pipelines — comes from my research engineering experience at AKH Vienna. The software architecture, FastAPI patterns, and FHIR implementation were developed through an iterative back-and-forth with Claude, reflecting how I approach new technical domains: combining existing expertise with AI-assisted learning to move quickly without sacrificing code quality.

This is also a deliberate reflection of how I expect to work in a Forward Deployed Engineer role — using the best available tools, including LLMs, to prototype and validate ideas rapidly.

---

## Background

During my time as a research engineer at the Ludwig Boltzmann Institute @ AKH Vienna, I worked with DICOM data from cardiac 4D CT studies — extracting imaging data from PACS, segmenting patient-specific heart models, and collaborating with clinicians on device positioning and scan timing. This project reflects that experience: the metadata fields selected, including cardiac gating parameters like trigger delay and heart rate, are chosen based on what mattered for us in a clinical imaging workflow.

---

## Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Health check |
| POST | `/dicom/analyze` | Extract structured metadata from a DICOM file |
| POST | `/dicom/summarize` | Extract metadata + generate LLM clinical summary |
| POST | `/dicom/compare` | Compare two DICOM files and summarize differences |
| POST | `/dicom/fhir` | Convert DICOM metadata to a FHIR ImagingStudy resource |

---

## Tech Stack

- **FastAPI** — REST API framework
- **pydicom** — DICOM file parsing
- **Anthropic Claude API** — LLM-powered clinical summarization
- **Docker** — Containerized deployment
- **Python 3.11**

---

## Setup

**1. Clone the repo**
```bash
git clone git@github.com:amaurer1010/clinical-dicom-api.git
cd clinical-dicom-api
```

**2. Add your Anthropic API key**
```bash
cp .env.example .env
# Edit .env and add your key from console.anthropic.com
```

**3a. Run with Docker (recommended)**
```bash
docker build -t clinical-dicom-api .
docker run -p 8000:8000 --env-file .env clinical-dicom-api
```

**3b. Run locally**
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**4. Open the interactive API docs**

Navigate to `http://localhost:8000/docs`

---

## Example Responses

### /dicom/analyze
```json
{
  "modality": "PX",
  "body_part": "JAW",
  "study_date": "20160330",
  "rows": 1480,
  "columns": 2775,
  "manufacturer": "Instrumentarium Dental",
  "manufacturer_model": "OP300"
}
```

### /dicom/summarize
```json
{
  "metadata": { "...": "..." },
  "summary": "Dental panoramic radiograph (PX) of the jaw acquired on 03/30/2016 using an Instrumentarium Dental OP300. Image dimensions are 2775 × 1480 pixels with fine 0.077mm pixel spacing, providing detailed visualization suitable for dental assessment and treatment planning."
}
```

### /dicom/fhir
```json
{
  "resourceType": "ImagingStudy",
  "status": "available",
  "subject": { "reference": "Patient/0" },
  "started": "2016-03-30",
  "series": [{
    "modality": {
      "system": "http://dicom.nema.org/resources/ontology/DCM",
      "code": "PX"
    },
    "bodySite": { "display": "JAW" }
  }]
}
```

---

## Project Structure
```
clinical-dicom-api/
├── app/
│   ├── main.py             # FastAPI app and route definitions
│   ├── dicom_parser.py     # DICOM metadata extraction via pydicom
│   ├── llm_client.py       # Anthropic API integration
│   ├── fhir_converter.py   # DICOM to FHIR ImagingStudy translation
│   └── schemas.py          # Pydantic response models
├── .env.example            # Environment variable template
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## Potential Next Steps

This project is a functional prototype. Moving it toward production would involve:

- **Authentication** — Protect endpoints with API key or JWT token authentication so only authorized systems can submit imaging data
- **Database layer** — Persist extracted metadata to PostgreSQL, enabling historical queries such as retrieving all CT studies for a given patient
- **Async LLM calls** — Move Anthropic API calls to a background task queue (e.g. Celery + Redis) so large DICOM files don't block the request thread
- **FHIR compliance validation** — Validate generated ImagingStudy resources against the official HL7 FHIR R4 schema before returning them
- **Expanded FHIR support** — Add conversion for related resources such as `Patient` and `DiagnosticReport` to support fuller EHR integration workflows
- **CI/CD pipeline** — Add GitHub Actions to run tests and auto-build the Docker image on every push
- **Broader DICOM tag coverage** — Extend the parser to handle multi-frame studies, structured reports (DICOM SR), and dose summary objects (RDSR)