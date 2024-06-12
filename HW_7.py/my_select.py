from sqlalchemy import func
from sqlalchemy.orm import sessionmaker
from models import Student, Subject, Grade, Group, Teacher
from database_engine import engine


Session = sessionmaker(bind=engine)
session = Session()

def select_1():
    return session.query(Student).order_by(Student.id).all()

def select_2(subject_name):
    return session.query(Student).join(Grade).join(Subject).filter(Subject.name == subject_name).order_by(Grade.score.desc()).first()

def select_3(subject_name):
    return session.query(func.avg(Grade.score)).join(Subject).filter(Subject.name == subject_name).scalar()

def select_4():
    return session.query(func.avg(Grade.score)).scalar()

def select_5(teacher_name):
    return session.query(Subject).join(Teacher).filter(Teacher.name == teacher_name).all()

def select_6(group_name):
    return session.query(Student).join(Group).filter(Group.name == group_name).all()

def select_7(group_name, subject_name):
    return session.query(Grade).join(Student).join(Group).join(Subject).filter(Group.name == group_name, Subject.name == subject_name).all()

def select_8(teacher_name):
    return session.query(func.avg(Grade.score)).join(Subject).join(Teacher).filter(Teacher.name == teacher_name).scalar()

def select_9(student_name):
    return session.query(Subject).join(Grade).join(Student).filter(Student.name == student_name).all()

def select_10(student_name, teacher_name):
    return session.query(Subject).join(Grade).join(Student).join(Teacher).filter(Student.name == student_name, Teacher.name == teacher_name).all()

session.close()
