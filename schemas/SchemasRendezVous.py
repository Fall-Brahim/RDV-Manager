from pydantic import BaseModel
from typing import Generic,TypeVar
from datetime import date,datetime
from pydantic.generics import GenericModel


class RendezVousSchemas(BaseModel):
    date_heure:str
    MedecinID:int
    Notes:str

class RdvSchemasUpdate(BaseModel):
    date_heure:str
    MedecinID:int
    Notes:str
