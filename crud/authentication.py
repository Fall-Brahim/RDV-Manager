from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import random
from fastapi import Request
from fastapi import Body
from config.db import get_db

security = HTTPBasic()

def authenticate_user(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.Email == credentials.username).first()
    if patient is None or patient.Mot_de_Passe != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return patient

def create_session(user_id: int):
    session_id = len(sessions) + random.randint(0, 1000000)
    sessions[session_id] = user_id
    return session_id