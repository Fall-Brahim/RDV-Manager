from pydantic import BaseModel,Field
from typing import Generic,TypeVar,List,Optional
from datetime import date,datetime
from pydantic.generics import GenericModel
from enum import Enum


class Genre(str, Enum):
    Homme = "Homme"
    Femme = "Femme"
class MedecinSchemas(BaseModel):
    Nom: str
    Prenom: str
    Telephone: int
    Email: str
    mdp: str # Mot de Passe
    sexe:Genre
    profil: str
    specialite:str

    class Config:
        orm_mode = True


class MedecinUpdate(BaseModel):
    Nom: str = Field(None, title="Nom du medecin")
    Prenom: str = Field(None, title="Prénom du medecin")
    Telephone: int = Field(None, title="Numéro de téléphone du medecin")
    Email: str = Field(None, title="Adresse email du medecin")
    profil: str = Field(None, title="URL du profil du medecin")
    specialite:str = Field(None,title="Specialite du medecin")

    class Config:
        orm_mode = True

