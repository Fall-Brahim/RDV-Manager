from pydantic import BaseModel
from typing import Generic,TypeVar
from datetime import date,datetime
from pydantic.generics import GenericModel


class ConsultationSchemas(BaseModel):
    Id_Consultations :int
    Dhconsultations :str
    patient:str
    medecin:str
    description :str
