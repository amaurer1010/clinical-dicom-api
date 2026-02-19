from app.schemas import DicomMetadata
from datetime import datetime

def to_fhir_imaging_study(metadata: DicomMetadata) -> dict:
    # Format study date from YYYYMMDD to YYYY-MM-DD
    study_date = None
    if metadata.study_date:
        try:
            study_date = datetime.strptime(metadata.study_date, "%Y%m%d").strftime("%Y-%m-%d")
        except ValueError:
            study_date = metadata.study_date

    return {
        "resourceType": "ImagingStudy",
        "status": "available",
        "subject": {
            "reference": f"Patient/{metadata.patient_id}" if metadata.patient_id else "Patient/unknown"
        },
        "started": study_date,
        "numberOfSeries": 1,
        "numberOfInstances": 1,
        "series": [
            {
                "modality": {
                    "system": "http://dicom.nema.org/resources/ontology/DCM",
                    "code": metadata.modality,
                    "display": metadata.modality
                },
                "bodySite": {
                    "display": metadata.body_part
                } if metadata.body_part else None,
                "performer": [
                    {
                        "actor": {
                            "display": metadata.institution
                        }
                    }
                ] if metadata.institution else [],
                "instance": [
                    {
                        "sopClass": {
                            "system": "urn:ietf:rfc:3986",
                            "code": "urn:oid:1.2.840.10008.5.1.4.1.1.1"
                        },
                        "number": 1,
                        "extension": [
                            {
                                "url": "rows",
                                "valueInteger": metadata.rows
                            },
                            {
                                "url": "columns",
                                "valueInteger": metadata.columns
                            },
                            {
                                "url": "pixelSpacing",
                                "valueString": metadata.pixel_spacing
                            },
                            {
                                "url": "sliceThickness",
                                "valueString": metadata.slice_thickness
                            },
                            {
                                "url": "cardiacTrigger",
                                "valueString": metadata.cardiac_trigger
                            },
                            {
                                "url": "triggerDelay",
                                "valueString": metadata.trigger_delay
                            },
                            {
                                "url": "heartRate",
                                "valueString": metadata.heart_rate
                            }
                        ]
                    }
                ]
            }
        ],
        "meta": {
            "source": f"{metadata.manufacturer} {metadata.manufacturer_model}".strip()
            if metadata.manufacturer else None
        }
    }