from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from typing import List
import models, schemas, crud, auth, database
from pydantic import EmailStr
import os
import uvicorn

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
    return {"message": "Welcome to the Contacts API"}

@app.post("/register/", response_model=schemas.User, status_code=201)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    return auth.register_user(db, user)

@app.post("/login/", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return auth.login_user(db, form_data.username, form_data.password)

@app.post("/verify-email/", status_code=200)
def verify_email(token: str, db: Session = Depends(database.get_db)):
    return auth.verify_email(db, token)

@app.post("/contacts/", response_model=schemas.Contact, status_code=201)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    if crud.contact_creation_limit_exceeded(db, current_user.id):
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    return crud.create_contact(db, contact, current_user.id)

@app.get("/contacts/", response_model=List[schemas.Contact])
def read_contacts(skip: int = 0, limit: int = 10, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    contacts = crud.get_contacts(db, skip=skip, limit=limit, owner_id=current_user.id)
    return contacts

@app.get("/contacts/{contact_id}", response_model=schemas.Contact)
def read_contact(contact_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_contact = crud.get_contact(db, contact_id, current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.put("/contacts/{contact_id}", response_model=schemas.Contact)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_contact = crud.update_contact(db, contact_id, contact, current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.delete("/contacts/{contact_id}", response_model=schemas.Contact)
def delete_contact(contact_id: int, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    db_contact = crud.delete_contact(db, contact_id, current_user.id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

@app.get("/contacts/search/", response_model=List[schemas.Contact])
def search_contacts(query: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    contacts = db.query(models.Contact).filter(
        (models.Contact.first_name.contains(query)) |
        (models.Contact.last_name.contains(query)) |
        (models.Contact.email.contains(query)),
        models.Contact.owner_id == current_user.id
    ).all()
    return contacts

@app.get("/contacts/upcoming_birthdays/", response_model=List[schemas.Contact])
def upcoming_birthdays(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    contacts = crud.get_upcoming_birthdays(db, owner_id=current_user.id)
    return contacts

@app.post("/update-avatar/", response_model=schemas.User)
def update_avatar(avatar_url: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return crud.update_avatar(db, avatar_url, current_user.id)

@app.post("/password-reset/", status_code=200)
def reset_password(email: EmailStr, db: Session = Depends(database.get_db)):
    return auth.reset_password(db, email)

if __name__ == "__main__":
    uvicorn.run("main:app",host="localhost",port=8000,reload=True)
