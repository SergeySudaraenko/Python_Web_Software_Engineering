from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Student, Group, Teacher, Subject, Grade

fake = Faker()

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(bind=engine)
session = Session()

groups = []
for _ in range(3):
    group = Group(name=fake.word())
    groups.append(group)

session.add_all(groups)
session.commit()

teachers = []
for _ in range(3):
    teacher = Teacher(name=fake.name())
    teachers.append(teacher)

session.add_all(teachers)
session.commit()

subjects = []
for _ in range(5):
    subject = Subject(name=fake.catch_phrase(), teacher_id=fake.random_element(teachers).id)
    subjects.append(subject)

session.add_all(subjects)
session.commit()

students = []
for _ in range(30):
    student = Student(name=fake.name(), group_id=fake.random_element(groups).id)
    students.append(student)

session.add_all(students)
session.commit()

grades = []
for student in students:
    for subject in subjects:
        grade = Grade(student_id=student.id, subject_id=subject.id, score=fake.random_int(min=1, max=100), date=fake.date_this_year())
        grades.append(grade)

session.add_all(grades)
session.commit()

session.close()
