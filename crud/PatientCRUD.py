from sqlalchemy.orm import Session
from models.models import Patient
from .passwordManager import verify_Password
from schemas.SchemasPatient import PatientSchemas
from fastapi import HTTPException


#------------->Operation CRUD de Patient

#Affichage de tout les Patient

def Get_All_Patient(db:Session,skip:int=0,limit:int=100):
    return db.query(Patient).offset(skip).limit(limit).all()


def create_patient(db: Session, patient: PatientSchemas):
    db_patient = Patient(
        Nom=patient.Nom,
        Prenom=patient.Prenom,
        Telephone=patient.Telephone,
        Email=patient.Email,
        Mot_de_Passe=patient.Mot_de_Passe,
        Profil=patient.Profil,
        Sexe=patient.Sexe,
        Date_Naissance=patient.Date_Naissance
    )
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

#Authentification des patients
def get_Patient_by_email(db: Session, email: str):
    return db.query(Patient).filter(Patient.Email == email).first()

#Affichage de Patient selon son ID(Recherche)
def get_Patient(db:Session,ID_Patient:int):
    return db.query(Patient).filter(Patient.ID_U==ID_Patient).first()

def Remove_Patient(db:Session,ID_Patient=int):
    RemPatient = get_Patient(db=db,ID_U = ID_Patient)
    db.delete(RemPatient)
    db.commit()

def Update_Patient(db:Session,ID_Patient:int,Nom:str,Prenom:str,Telephone:int,Email:str,profil:str,Sexe,dateNaissance:str):
    Patient_Update = get_Patient(db=db,ID_Patient=ID_Patient)
    Patient_Update.Nom = Nom
    Patient_Update.Prenom = Prenom
    Patient_Update.Telephone = Telephone
    Patient_Update.Email = Email
    Patient_Update.profil = profil
    Patient_Update.Sexe = Sexe
    Patient_Update.dateNaissance = dateNaissance
    db.commit()




#-------------------->Operation CRUD de Medecin


