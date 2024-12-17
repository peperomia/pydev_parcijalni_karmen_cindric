
from sqlmodel import SQLModel, Field, create_engine, Session, select

class Student(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str

class Course(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str

class Enrollment(SQLModel, table=True):
    student_id: int = Field(foreign_key="student.id", primary_key=True)
    course_id: int = Field(foreign_key="course.id", primary_key=True)
    grade: str  # Dodatni stupac koji nije iz drugih tablica

engine = create_engine("sqlite:///database.db")
SQLModel.metadata.create_all(engine)


with Session(engine) as session:
    student1 = Student(name="Ivan")
    student2 = Student(name="Ana")
    course1 = Course(title="Matematika")
    course2 = Course(title="Fizika")

    session.add_all([student1, student2, course1, course2])
    session.commit()

    enrollment1 = Enrollment(student_id=student1.id, course_id=course1.id, grade="A")
    enrollment2 = Enrollment(student_id=student2.id, course_id=course2.id, grade="B")

    session.add_all([enrollment1, enrollment2])
    session.commit()

def add_enrollment_if_not_exists(student_id: int, course_id: int, grade: str):
    with Session(engine) as session:
        statement = select(Enrollment).where(Enrollment.student_id == student_id, Enrollment.course_id == course_id)
        result = session.exec(statement).first()
        
        if not result:
            enrollment = Enrollment(student_id=student_id, course_id=course_id, grade=grade)
            session.add(enrollment)
            session.commit()
            print("Enrollment added.")
        else:
            print("Enrollment already exists.")

# Primjer korištenja funkcije
add_enrollment_if_not_exists(1, 1, "A")
add_enrollment_if_not_exists(1, 1, "A")  # Ovaj unos neće biti dodan jer već postoji

