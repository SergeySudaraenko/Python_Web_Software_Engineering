from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
from . import models, schemas, crud, auth, database
from pydantic import EmailStr


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=database.engine)

@app.get("/")
def read_root():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: A welcome message.
    """
    return {"message": "Welcome to the Contacts API"}

@app.post("/register/", response_model=schemas.User, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    """
    Registers a new user.

    Args:
        user (schemas.UserCreate): The user data for registration.
        db (Session): The database session.

    Returns:
        schemas.User: The registered user.
    """
    return auth.register_user(db, user)

@app.post("/login/", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Logs in a user and returns access and refresh tokens.

    Args:
        form_data (OAuth2PasswordRequestForm): The login form data.
        db (Session): The database session.

    Returns:
        schemas.Token: The generated tokens.
    """
    return auth.login_user(db, form_data.username, form_data.password)

@app.post("/verify-email/", status_code=200)
def verify_email(token: str, db: Session = Depends(database.get_db)):
    """
    Verifies a user's email using the provided token.

    Args:
        token (str): The verification token.
        db (Session): The database session.

    Returns:
        schemas.User: The verified user.
    """
    return auth.verify_email(db, token)

@app.post("/contacts/", response_model=schemas.Contact, status_code=201)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """
    Creates a new contact for the current user.

    Args:
        contact (schemas.ContactCreate): The contact data.
        db (Session): The database session.
        current_user (models.User): The current user.

    Returns:
        schemas.Contact: The created contact.

    Raises:
        HTTPException: If the contact creation limit is exceeded.
    """
    if crud.contact_creation_limit_exceeded(db, current_user.id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return crud.create_contact(db, contact, current_user.id)

@app.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """
    Retrieves a list of contacts for the current user.

    Args:
        skip (int): The number of records to skip.
        limit (int): The maximum number of records to return.
        db (Session): The database session.
        current_user (models.User): The current user.

    Returns:
        List[schemas.Contact]: The list of contacts.
    """
    contacts = crud.get_contacts(db, skip=skip, limit=limit, owner_id=current_user.id)
    return contacts

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """
    Retrieves a specific contact for the current user.

    Args:
        contact_id (int): The ID of the contact.
        db (Session): The database session.
        current_user (models.User): The current user.

    Returns:
        schemas.Contact: The contact if found.

    Raises:
        HTTPException: If the contact is not found.
    """
    db_contact = crud.get_contact(db, contact_id, current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """
    Updates a specific contact for the current user.

    Args:
        contact_id (int): The ID of the contact.
        contact (schemas.ContactUpdate): The new contact data.
        db (Session): The database session.
        current_user (models.User): The current user.

    Returns:
        schemas.Contact: The updated contact.

    Raises:
        HTTPException: If the contact is not found.
    """
    db_contact = crud.update_contact(db, contact_id, contact, current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """
    Deletes a specific contact for the current user.

    Args:
        contact_id (int): The ID of the contact.
        db (Session): The database session.
        current_user (models.User): The current user.

    Returns:
        schemas.Contact: The deleted contact.

    Raises:
        HTTPException: If the contact is not found.
    """
    db_contact = crud.delete_contact(db, contact_id, current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.get("/contacts/search/", response_model=List[schemas.Contact])
def search_contacts(query: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """
    Searches for contacts matching the query for the current user.

    Args:
        query (str): The search query.
        db (Session): The database session.
        current_user (models.User): The current user.

    Returns:
        List[schemas.Contact]: The list of matching contacts.
    """
    contacts = db.query(models.Contact).filter(
        (models.Contact.first_name.contains(query)) |
        (models.Contact.last_name.contains(query)) |
        (models.Contact.email.contains(query)),
        models.Contact.owner_id == current_user.id
    ).all()
    return contacts

@app.get("/contacts/upcoming_birthdays/", response_model=List[schemas.Contact])
def upcoming_birthdays(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """
    Retrieves contacts with upcoming birthdays for the current user.

    Args:
        db (Session): The database session.
        current_user (models.User): The current user.

    Returns:
        List[schemas.Contact]: The list of contacts with upcoming birthdays.
    """
    contacts = crud.get_upcoming_birthdays(db, owner_id=current_user.id)
    return contacts

@app.post("/update-avatar/", response_model=schemas.User)
def update_avatar(avatar_url: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    """
    Updates the avatar URL of the current user.

    Args:
        avatar_url (str): The new avatar URL.
        db (Session): The database session.
        current_user (models.User): The current user.

    Returns:
        schemas.User: The user with the updated avatar URL.
    """
    return crud.update_avatar(db, avatar_url, current_user.id)

@app.post("/password-reset/", status_code=200)
def reset_password(email: EmailStr, db: Session = Depends(database.get_db)):
    """
    Sends a password reset email to the user.

    Args:
        email (EmailStr): The user's email.
        db (Session): The database session.

    Returns:
        dict: A message indicating that the password reset email has been sent.
    """
    return auth.reset_password(db, email)
