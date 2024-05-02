from pydantic import BaseModel,Field,EmailStr,constr
from datetime import date,datetime
from enum import Enum
from typing import Optional,List

class Genre(str,Enum):
    Homme = "Homme"
    Femme = "Femme"
class PatientSchemas(BaseModel):
    Nom: constr(min_length=1, max_length=180)
    Prenom: constr(min_length=1, max_length=180)
    Telephone: int
    Email: str = None
    Mot_de_Passe: constr(min_length=8, max_length=255)
    Profil: constr(min_length=1, max_length=255)
    Sexe :Genre
    Date_Naissance: date

    class Config:
        orm_mode = True


class PatientUpdateSchemas(BaseModel):
    Nom: str = Field(None, title="Nom du patient")
    Prenom: str = Field(None, title="Prénom du patient")
    Telephone: int = Field(None, title="Numéro de téléphone du patient")
    Email: str = Field(None, title="Adresse email du patient")
    profil: str = Field(None, title="URL du profil du patient")
    dateNaissance: datetime = Field(None, title="Date de naissance du patient")

    class Config:
        orm_mode = True
