import os
import anthropic
from dotenv import load_dotenv
from app.schemas import DicomMetadata

load_dotenv()

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def summarize_metadata(metadata: DicomMetadata) -> str:
    prompt = f"""You are a clinical informatics assistant. Given the following DICOM scan metadata, 
write a concise plain-language summary (2-3 sentences) suitable for a clinical workflow dashboard. 
Focus on what kind of scan this is and any relevant technical details a clinician would care about.

Metadata:
{metadata.model_dump_json(indent=2)}"""

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=256,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text