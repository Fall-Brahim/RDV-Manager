from schemas.SchemasRendezVous import RendezVousSchemas
from models.models import RendezVous
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .auth import decode_access_token
from .DisponibiliteCRUD import is_medecin_available
def CreateRdv(db:Session,rendezVous:RendezVousSchemas,token:str):
    payload = decode_access_token(token)
    patient_id = payload.get("sub")

    if not is_medecin_available(db,rendezVous.MedecinID,rendezVous.date_heure):
        raise HTTPException(status_code=400, detail="Le médecin n'est pas disponible à cette heure")
        db_Rdv = RendezVous(
        date_heure=rendezVous.date_heure,
        PatientID=patient_id,
        Medecin = rendezVous.MedecinID,
        Notes = rendezVous.Notes,
    )
    db.add(db_Rdv)
    db.commit()
    db.refresh(db_Rdv)
    return db_Rdv

def get_all_RdV(db:Session,skip:int=0,limit:int=100):
    return db.query(RendezVous).offset(skip).limit(limit).all()

def getRdv(db:Session,IDR:int):
    return db.query(RendezVous).filter(RendezVous.Id_Rdv==IDR).first()

def update_Rdv(db:Session,IdR:int,Date_heure:str,Patient:str,Medecin:str,Notes:str):
    updateRdv = getRdv(db,IdR)
    updateRdv.date_heure = Date_heure
    updateRdv.patientID= Patient
    updateRdv.MedecinID = Medecin
    updateRdv.Notes = Notes
    db.commit()


def removeRdv(db:Session,IdR:int):
    db_Rdv = getRdv(db,IdR)
    db.delete(db_Rdv)
    db.commit()

