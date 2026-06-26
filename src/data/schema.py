from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class Vitals(BaseModel):
    blood_pressure: Optional[str] = None
    heart_rate: Optional[int] = None
    weight_kg: Optional[float] = None
    temperature_c: Optional[float] = None
    oxygen_saturation: Optional[float] = None


class LabResults(BaseModel):
    # Diabetes markers
    HbA1c: Optional[float] = None
    glucose: Optional[float] = None
    # Kidney function
    creatinine: Optional[float] = None
    # Thyroid
    TSH: Optional[float] = None
    # Cardiac
    cholesterol: Optional[float] = None
    LDL: Optional[float] = None
    HDL: Optional[float] = None
    # General
    hemoglobin: Optional[float] = None
    WBC: Optional[float] = None


class Medication(BaseModel):
    name: str
    dose: str
    frequency: str


class ClinicalVisit(BaseModel):
    date: date
    encounter_type: str  # outpatient, inpatient, emergency
    chief_complaint: str
    vitals: Optional[Vitals] = None
    lab_results: Optional[LabResults] = None
    medications: List[Medication] = []
    physician_notes: str
    diagnosis: str
    follow_up: Optional[str] = None


class PatientRecord(BaseModel):
    patient_id: str
    age: int
    gender: str
    conditions: List[str]  # chronic conditions
    encounters: List[Encounter] = Field(
        ..., 
        min_length=3,  # minimum 3 encounters for longitudinal
        description="Must have at least 3 encounters for longitudinal analysis"
    )

    def get_encounter_count(self) -> int:
        return len(self.encounters)

    def get_date_range(self) -> str:
        dates = [e.date for e in self.encounters]
        return f"{min(dates)} to {max(dates)}"


class GroundTruthSummary(BaseModel):
    patient_id: str
    summary: str
    key_facts: List[str]  # facts that MUST appear in any good summary
    numeric_values: dict   # specific numbers that must be accurate
    temporal_sequence: List[str]  # correct chronological order of events