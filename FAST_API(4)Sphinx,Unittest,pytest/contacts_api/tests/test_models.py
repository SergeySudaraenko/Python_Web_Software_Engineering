import pytest
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Base
from database import DATABASE_URL


TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="module")
def test_engine():
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def test_session(test_engine):
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = SessionLocal()
    yield session
    session.close()

def test_user_model(test_engine):
   
    inspector = inspect(test_engine)
    tables = inspector.get_table_names()
    assert "users" in tables

    
    columns = [column["name"] for column in inspector.get_columns("users")]
    expected_columns = ["id", "email", "hashed_password", "is_verified", "avatar_url", "verification_token"]
    assert sorted(columns) == sorted(expected_columns)

def test_contact_model(test_engine):
    
    inspector = inspect(test_engine)
    tables = inspector.get_table_names()
    assert "contacts" in tables

    
    columns = [column["name"] for column in inspector.get_columns("contacts")]
    expected_columns = ["id", "first_name", "last_name", "email", "phone", "birthday", "owner_id", "created_at"]
    assert sorted(columns) == sorted(expected_columns)
