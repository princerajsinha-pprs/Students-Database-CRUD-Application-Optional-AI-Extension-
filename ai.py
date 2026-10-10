import os
import re
import requests
from datetime import date

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")


def select_relevant_students(question: str, students):
    """Small deterministic retrieval layer before calling the local model."""
    q = question.lower()
    if "how many" in q or "count" in q or "total" in q:
        return students

    match = re.search(r"born\s+(?:after|since)\s+(\d{4})", q)
    if match:
        year = int(match.group(1))
        return [s for s in students if s.date_of_birth.year > year]

    return students


def ask_ollama(question: str, students) -> str:
    rows = [
        {
            "student_id": s.student_id,
            "name": s.name,
            "date_of_birth": s.date_of_birth.isoformat(),
            "email": s.email,
            "phone": s.phone,
            "course": s.course,
            "address": s.address,
            "enrollment_date": s.enrollment_date.isoformat() if s.enrollment_date else None,
        }
        for s in students
    ]

    prompt = (
        "You answer questions only from the supplied student records. "
        "Do not invent records or fields. If the records do not contain enough information, say so.\n\n"
        f"Student records:\n{rows}\n\nQuestion: {question}"
    )

    response = requests.post(
        OLLAMA_URL,
        json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
        timeout=60,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("response", "No response returned by Ollama.").strip()
