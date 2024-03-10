from typing import List
from langchain.pydantic_v1 import BaseModel


# Define Properties
class Properties(BaseModel):
    # Attributes
    patient_age: str
    patient_gender: str
    patient_diagnosis: str
    patient_medical_history: str
    patient_symptoms: List[str]