from datetime import date
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from .models import Student
from .schemas import StudentCreate, StudentUpdate


def create_student(db: Session, student: StudentCreate) -> Student:
    obj = Student(**student.model_dump())
    db.add(obj)
    try:
        db.commit()
        db.refresh(obj)
    except IntegrityError:
        db.rollback()
        raise ValueError("A student with this email already exists.")
    return obj


def get_students(db: Session, name: str | None = None, course: str | None = None,
                  born_after: date | None = None) -> list[Student]:
    stmt = select(Student).order_by(Student.student_id)
    if name:
        stmt = stmt.where(Student.name.ilike(f"%{name}%"))
    if course:
        stmt = stmt.where(Student.course.ilike(f"%{course}%"))
    if born_after:
        stmt = stmt.where(Student.date_of_birth > born_after)
    return list(db.scalars(stmt).all())


def get_student(db: Session, student_id: int) -> Student | None:
    return db.get(Student, student_id)


def update_student(db: Session, student_id: int, payload: StudentUpdate) -> Student | None:
    obj = get_student(db, student_id)
    if obj is None:
        return None
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    try:
        db.commit()
        db.refresh(obj)
    except IntegrityError:
        db.rollback()
        raise ValueError("A student with this email already exists.")
    return obj


def delete_student(db: Session, student_id: int) -> bool:
    obj = get_student(db, student_id)
    if obj is None:
        return False
    db.delete(obj)
    db.commit()
    return True
