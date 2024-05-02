from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas.SchemasPatient import PatientSchemas, PatientUpdateSchemas
from crud.PatientCRUD import (
    create_patient,
    get_Patient,
    Get_All_Patient,
    Remove_Patient,
    Update_Patient,
)
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from config.db import SessionLocal
from crud.auth import oauth2_scheme,decode_access_token
from config.db import get_db

Patientrouter = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@Patientrouter.get("/patients/", response_model=list[PatientSchemas])
async def get_all_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_Type"] != "patients":
        raise HTTPException(status_code=403,detail="Permission denied")
    patients = Get_All_Patient(db, skip=skip, limit=limit)
    return patients

@Patientrouter.get("/patients/{patient_id}", response_model=PatientSchemas)
async def get_patient(patient_id: int, db: Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_Type"] != "patients":
        raise HTTPException(status_code=403,detail="Permission denied")
    patient = get_Patient(db, ID_Patient=patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@Patientrouter.post("/patients/", response_model=PatientSchemas)
async def create_patient_route(patient: PatientSchemas, db: Session = Depends(get_db)):
    if db.query(Patient).filter(Patient.Email == patient.Email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )
    new_patient= create_patient(db,patient)
    return {"Message":"Patient Inscrit avec success"}

@Patientrouter.get("/me/",response_model=PatientSchemas)
def Get_Current_Patient(current_patient:PatientSchemas = Depends()):
    pass

@Patientrouter.put("/patients/{patient_id}", response_model=PatientSchemas)
async def update_patient(
    patient_id: int, patient: PatientUpdateSchemas, db: Session = Depends(get_db),
        token:str=Depends(oauth2_scheme)
):
    payload = decode_access_token(token)
    if payload["type_user"] != "patients":
        raise HTTPException(status_code=403,detail="Permission denied")
    db_patient = get_Patient(db, ID_Patient=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    Update_Patient(
        db,
        ID_Patient=patient_id,
        Nom=patient.Nom,
        Prenom=patient.Prenom,
        Telephone=patient.Telephone,
        Email=patient.Email,
        profil=patient.profil,
        Sexe=patient.Sexe,
        dateNaissance=patient.dateNaissance,
    )
    return patient

@Patientrouter.delete("/patients/{patient_id}")
async def delete_patient(patient_id: int, db: Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_Type"] != "patients":
        raise HTTPException(status_code=403,detail="Permission denied")
    patient = get_Patient(db, ID_Patient=patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    Remove_Patient(db, ID_Patient=patient_id)
    return {"message": "Patient deleted successfully"}
