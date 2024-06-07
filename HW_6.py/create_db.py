import sqlite3
from faker import Faker
import random
from datetime import datetime, timedelta

def create_database():
   
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()
    
    
    create_tables_script = '''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        group_id INTEGER,
        FOREIGN KEY (group_id) REFERENCES groups(id)
    );

    CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS teachers (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS subjects (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        teacher_id INTEGER,
        FOREIGN KEY (teacher_id) REFERENCES teachers(id)
    );

    CREATE TABLE IF NOT EXISTS grades (
        id INTEGER PRIMARY KEY,
        student_id INTEGER,
        subject_id INTEGER,
        grade INTEGER,
        date DATE,
        FOREIGN KEY (student_id) REFERENCES students(id),
        FOREIGN KEY (subject_id) REFERENCES subjects(id)
    );
    '''

    
    cursor.executescript(create_tables_script)
    
    conn.close()

def populate_database():
    
    fake = Faker()

   
    conn = sqlite3.connect('university.db')
    cursor = conn.cursor()

   
    groups = [('Group 1',), ('Group 2',), ('Group 3',)]
    cursor.executemany("INSERT INTO groups (name) VALUES (?)", groups)

   
    teachers = [(fake.name(),) for _ in range(5)]
    cursor.executemany("INSERT INTO teachers (name) VALUES (?)", teachers)

  
    subjects = [(fake.word(), random.randint(1, 5)) for _ in range(8)]
    cursor.executemany("INSERT INTO subjects (name, teacher_id) VALUES (?, ?)", subjects)

   
    for _ in range(random.randint(30, 50)):
        student_name = fake.name()
        group_id = random.randint(1, 3)
        cursor.execute("INSERT INTO students (name, group_id) VALUES (?, ?)", (student_name, group_id))
        student_id = cursor.lastrowid
        
        
        for subject_id in range(1, 9):
            for _ in range(random.randint(10, 20)):
                grade = random.randint(1, 5)
                date = fake.date_between(start_date='-1y', end_date='today').strftime('%Y-%m-%d')
                cursor.execute("INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)",
                               (student_id, subject_id, grade, date))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_database()
    populate_database()





