import os
import anthropic
from dotenv import load_dotenv
from app.schemas import DicomMetadata

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def summarize_metadata(metadata: DicomMetadata) -> str:
    prompt = f"""You are a clinical informatics assistant with expertise in medical imaging workflows. 
Given the following DICOM scan metadata, write a concise plain-language summary (2-3 sentences) 
suitable for a non-technical clinical workflow dashboard. Focus on what kind of scan this is and 
any relevant technical details a clinician would care about. If cardiac gating parameters are 
present (trigger delay, heart rate, cardiac trigger source), include the likely cardiac phase 
and its clinical significance — for example whether the acquisition corresponds to systole or 
diastole based on the trigger delay.

Metadata:
{metadata.model_dump_json(indent=2)}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def compare_metadata(metadata1: DicomMetadata, metadata2: DicomMetadata) -> str:
    prompt = f"""You are a clinical informatics assistant with expertise in medical imaging workflows.
Compare the following two DICOM scans and write a concise plain-language summary (3-4 sentences)
of the key differences between them, suitable for a clinical workflow dashboard.
Focus on clinically meaningful differences such as modality, body part, acquisition parameters,
image resolution, and cardiac gating if present.

Scan 1:
{metadata1.model_dump_json(indent=2)}

Scan 2:
{metadata2.model_dump_json(indent=2)}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text