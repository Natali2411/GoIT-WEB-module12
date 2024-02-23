from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ChannelResponse, ContactResponse, ContactChannelResponse, \
    ContactModel
from src.repository import contacts as repository_contacts

router = APIRouter(prefix='/contacts', tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def read_contacts(firstName: str = None, lastName: str = None,
                        email: str = None, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts(db, firstName, lastName, email)
    return contacts


@router.get("/birthdays", response_model=List[ContactResponse])
async def read_contacts_birthdays(daysForward: int, db: Session = Depends(get_db)):
    contacts = await repository_contacts.get_contacts_birthdays(db, daysForward)
    return contacts

@router.get("/{contactId}", response_model=ContactResponse)
async def read_contact(contactId: int, db: Session = Depends(get_db)):
    contact = await repository_contacts.get_contact(contactId, db)
    if contact is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found"
        )
    return contact


@router.post("/", response_model=ContactResponse)
async def create_contact(body: ContactModel, db: Session = Depends(get_db)):
    return await repository_contacts.create_contact(body, db)
