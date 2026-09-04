import os
from typing import Any

import pandas as pd
from openai import OpenAI

MAX_CHARS = 8192 * 4

def _get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY is not set."
        )

    return OpenAI(api_key=api_key)


def generate_summary(patient_id: str, notes_df: pd.DataFrame, prompt: str) -> str:
    if not isinstance(notes_df, pd.DataFrame):
        raise TypeError("notes_df must be a pandas DataFrame")

    required_columns = {'person_id', 'clean_note_text'}
    missing_columns = required_columns.difference(notes_df.columns)
    if missing_columns:
        raise KeyError(f"notes_df is missing required columns: {sorted(missing_columns)}")

    patient_notes = notes_df[notes_df['person_id'] == patient_id].copy()
    if patient_notes.empty:
        raise ValueError(f"No notes found for patient_id={patient_id}")

    patient_notes = patient_notes.sort_values('creation_timestamp')
    concatenated = "\n\n".join(patient_notes['clean_note_text'].astype(str).tolist())

    if len(concatenated) > MAX_CHARS:
        concatenated = concatenated[:MAX_CHARS]

    client = _get_client()
    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": concatenated}
        ],
    )
    return response.choices[0].message.content


def generate_rag_summary(context: str, prompt: str) -> str:
    if not isinstance(context, str):
        raise TypeError("context must be a string")

    if not context.strip():
        raise ValueError("context cannot be empty")

    if len(context) > MAX_CHARS:
        context = context[:MAX_CHARS]

    client = _get_client()

    response = client.chat.completions.create(
        model="gpt-5.6-luna",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": context}
        ],
    )

    return response.choices[0].message.content