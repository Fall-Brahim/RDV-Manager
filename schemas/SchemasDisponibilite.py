from pydantic import BaseModel
from typing import Generic,TypeVar
from datetime import date,datetime
from pydantic.generics import GenericModel


class DisponibiliteSchemas(BaseModel):
    id: int
    jour: str
    mois:str
    annee:str
    heure_debut: datetime
    heure_fin: datetime
    medecin_id: int
    medecin: str