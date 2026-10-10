from datetime import date
from fastapi import Depends, FastAPI, HTTPException, Query, status
import requests
from sqlalchemy.orm import Session

from . import crud
from .ai import ask_ollama, select_relevant_students
from .database import Base, engine, get_db
from .schemas import StudentCreate, StudentResponse, StudentUpdate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EWB Students Database CRUD API",
    version="1.0.0",
    description="FastAPI + SQLite backend for managing student records.",
)


@app.get("/", tags=["Health"])
def root():
    return {"message": "EWB Students CRUD API is running", "docs": "/docs"}


@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_student(db, student)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))


@app.get("/students", response_model=list[StudentResponse], tags=["Students"])
def list_students(
    name: str | None = Query(default=None),
    course: str | None = Query(default=None),
    born_after: date | None = Query(default=None, description="Return students born after this date"),
    db: Session = Depends(get_db),
):
    return crud.get_students(db, name=name, course=course, born_after=born_after)


@app.get("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = crud.get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.put("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def update_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    try:
        student = crud.update_student(db, student_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student


@app.patch("/students/{student_id}", response_model=StudentResponse, tags=["Students"])
def patch_student(student_id: int, payload: StudentUpdate, db: Session = Depends(get_db)):
    return update_student(student_id, payload, db)


@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Students"])
def delete_student(student_id: int, db: Session = Depends(get_db)):
    if not crud.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found")
    return None


@app.post("/ai/ask", tags=["Optional AI"])
def ai_question(question: str = Query(min_length=3), db: Session = Depends(get_db)):
    """Optional Ollama extension. No SQL is generated or executed by the model."""
    students = crud.get_students(db)
    relevant = select_relevant_students(question, students)
    try:
        answer = ask_ollama(question, relevant)
    except requests.RequestException as exc:  # type: ignore[name-defined]
        raise HTTPException(status_code=503, detail=f"Ollama is unavailable: {exc}")
    return {"question": question, "answer": answer, "records_used": len(relevant)}
