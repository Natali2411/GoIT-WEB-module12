from typing import List

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ChannelResponse, ChannelModel, ContactChannelModel, \
    ContactChannelResponse
from src.repository import contacts_channels as repository_contacts_channels


router = APIRouter(prefix='/contactsChannels', tags=["contactsChannels"])


@router.get("/", response_model=List[ContactChannelResponse])
async def read_contacts_channels(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    contacts_channels = await repository_contacts_channels.get_contacts_channels(skip, limit, db)
    return contacts_channels


@router.post("/", response_model=ContactChannelResponse)
async def create_contacts_channels(body: ContactChannelModel, db: Session = Depends(get_db)):
    contacts_channels = await repository_contacts_channels.create_contacts_channels(
        body, db)
    if contacts_channels == 1:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Such channel value already "
                                                         "exists in the DB")
    elif contacts_channels == 2:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Contact or channel name "
                                                          "is not found")
    return contacts_channels


@router.put("/{contactChannelId}", response_model=ContactChannelResponse)
async def update_contact_channel(contactChannelId: int, body: ContactChannelModel, db: Session = Depends(
    get_db)):
    contact_channel = await repository_contacts_channels.update_contact_channel(
        contactChannelId, body, db)
    if not contact_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact channel {contactChannelId} "
                                                          "is not found")
    return contact_channel

@router.delete("/{contactChannelId}", response_model=ContactChannelResponse)
async def delete_contact_channel(contactChannelId: int, db: Session = Depends(
    get_db)):
    contact_channel = await repository_contacts_channels.remove_contact_channel(
        contactChannelId, db)
    if not contact_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Contact channel {contactChannelId} "
                                                          "is not found")
    return contact_channel
