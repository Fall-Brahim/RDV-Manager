from fastapi import Depends, HTTPException, status,APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional
from .PatientCRUD import get_Patient_by_email
from .MedecinCRUD import get_Medecin_by_email
# Importez vos modèles SQLAlchemy ici
from models.models import Patient,Medecin
from sqlalchemy.orm import Session
from config.db import get_db

auth = APIRouter()



# Configuration des paramètres de hachage
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
import os
def generate_secret_key() -> str:
    return os.urandom(32).hex()

# Configuration des paramètres JWT
SECRET_KEY = generate_secret_key()  # Changez ceci par une clé secrète sécurisée
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Créez un objet OAuth2PasswordBearer pour gérer l'authentification
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Fonction pour vérifier le mot de passe haché
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Fonction pour hacher le mot de passe
def get_password_hash(password):
    return pwd_context.hash(password)

# Fonction pour créer un token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Fonction pour vérifier et décoder un token JWT
def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Fonction pour l'authentification des utilisateurs Patient
async def authenticate_patient(email: str, password: str,db:Session):
    patient = get_Patient_by_email(db,email)  # Remplacez ceci par votre fonction de recherche de patient
    if not patient:
        return False
    if not verify_password(password, patient.Mot_de_Passe):
        return False
    return patient

# Fonction pour l'authentification des utilisateurs Medecin
async def authenticate_medecin(email: str, password: str,db:Session):
    medecin = get_Medecin_by_email(db,email)  # Remplacez ceci par votre fonction de recherche de médecin
    if not medecin:
        return False
    if not verify_password(password, medecin.mdp):
        return False
    return medecin

# Route pour obtenir le token d'authentification
@auth.post("/Connexion")
async def Connexion(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    patient = await authenticate_patient(form_data.username, form_data.password)
    medecin = await authenticate_medecin(form_data.username, form_data.password)
    if not patient and not medecin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if patient:
        access_token = create_access_token(
            data={"sub": patient.Email, "user_type": "patient"},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
    elif medecin:
        access_token = create_access_token(
            data={"sub": medecin.Email, "user_type": "medecin"},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        )
    return {"access_token": access_token, "token_type": "bearer"}



# Exemple de route protégée nécessitant une authentification
"""@auth.get("/consultations")
async def get_consultations(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_type"] != "medecin":
        raise HTTPException(status_code=403, detail="Permission denied")
    # Continuez avec la logique de récupération des consultations pour les médecins
    # Exemple :
    consultations = your_medecin_consultations_query_function(payload["sub"])
    return consultations
"""