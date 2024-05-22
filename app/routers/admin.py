"""Endpoints for the administrator.

"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Security,status
from ..reporting.caplog import logger
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import ServerMessage, UserMessage
from typing import Annotated
import logging

from app.schemas import UserBase
from ..database import get_session
from ..authorization.auth import get_api_key
from ..models import User

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/users",response_model=List[UserBase])
def get_users_for_admin(
    u: User = Security(get_api_key),
    session:Session =Depends(get_session)
)->List[User]:
    """Provide an admin with a list of users.
    
        Only the admin user has access to this.
    
        Exception: if the key is not valid

        Exception: if the user is not admin
    """
    if u.username!='admin':
        raise HTTPException(status_code=400, detail='Only admin can do this')
    user = session.query(User).all()
    return user

@router.get("/user/{username}",response_model=UserBase)
def get_user_for_admin(
    username:str,
    u: User = Security(get_api_key),
    session:Session =Depends(get_session)
)->User:
    """Provide an admin with the details of the user called username.
    
    Backdoor access to global data via an API key.
        
        username: the name of the user.
        
        The API key must be the admin's key
    
        Returns: authentication error if the key is not valid.

        Returns: not allowed error if requester is not the admin

        Returns: None if the user does not exist.
    """
    if u.username!="admin" and u.username!=username:
        raise HTTPException(status_code=400, detail='Non-admin user requested data on another user')
    user = session.query(User).where(User.username==username).first()
    return user

@router.get("/lock/{username}",response_model=ServerMessage)
def lock_user(
    username: str,
    u: User = Security(get_api_key),
    session:Session =Depends(get_session)
)->ServerMessage:
    """Lock a username to restrict access to it to one player.

      {username} is the name of the user to lock.  
      If there is no such user, send a failure (status code 400?).   
      (TODO Only guest can request a lock. If another user, send a failure).  
      If user is not locked, generate and send an apikey (status code 200)  [NB IS THIS NEEDED?].  
      If user is locked, send a refusal (status code 400).  
    """
    logger.info(f"request to lock user called {username}")
    # Find out if the user exists.  
    user = session.query(User).where(User.username==username).first()
    if user is None:
        raise HTTPException(status_code=400, detail='Request to lock non-existent user')
    if user.is_locked:
        raise HTTPException(status_code=400, detail='Request to lock user who is already locked')
    session.add(user)
    user.is_locked=True
    session.commit()
    return {'message': f'User {username} was locked',"statusCode":status.HTTP_200_OK}
        

@router.get("/unlock/{username}",response_model=ServerMessage)
def unlock_user(
    username: str,
    u: User = Security(get_api_key),
    session:Session =Depends(get_session)
)->ServerMessage:
    """Unlock a username to allow other players to use it.

      {username} is the name of the user to unlock.  
      If there is no such user, send a failure (status code 400?).   
      If user is not locked, send a message and status code 204.    
      If user is locked, unlock it and return status code 200.  
    """
    logger.info(f"request to lock user called {username}")
    # Find out if the user exists.  
    user = session.query(User).where(User.username==username).first()
    if user is None:
        raise HTTPException(status_code=400, detail='Request to ulock non-existent user')
    if not user.is_locked:
        raise HTTPException(status_code=400, detail='Request to unlock user who is not locked')
    session.add(user)
    user.is_locked=False
    session.commit()
    return {'message': f'User {username} was unlocked',"statusCode":status.HTTP_200_OK}

@router.post("/register", status_code=201,response_model=UserMessage)
def register(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
    u:User=Security(get_api_key)
)->str:
    """Register a new user and API key. ONLY admin user can do this.

        form_data: user and api key. (The api_key is called a password
        because we haven't customised the form as yet)

        Return status 400 for malformed form.
        
        Return status 400 if user already exists.
        
        Return status 201 if the user is registered.
    """
    if u.username!='admin':
        raise HTTPException(status_code=400, detail='Only admin can do this')
    if session.query(User).where(User.username == form_data.username).first() is not None:
        raise HTTPException(status_code=400, detail='Username is taken')
    user:User=User(
        username=form_data.username,
        api_key=form_data.password,
        current_simulation_id=0
    )
    session.add(user)
    session.commit()
    return {'message': f'User {form_data.username} registered'}

