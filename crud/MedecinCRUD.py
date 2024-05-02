from sqlalchemy.orm import Session
from models.models import Medecin
from schemas.SchemasMedecin import MedecinSchemas
from .passwordManager import verify_Password


def Get_All_Medecin(db:Session,skip:int=0,limit:int=100):
    return db.query(Medecin).offset(skip).limit(limit).all()

#Ajouter des Medecins
def create_Medecin(db:Session,medecin:MedecinSchemas):
    db_medecin = Medecin(
        Nom = medecin.Nom,
        Prenom = medecin.Prenom,
        Telephone = medecin.Telephone,
        Email = medecin.Email,
        mdp = medecin.mdp,
        Sexe =medecin.sexe,
        profil = medecin.profil,
        specialite = medecin.specialite
    )
    db.add(db_medecin)
    db.commit()
    db.refresh(db_medecin)
    return  db_medecin

def get_Medecin(db:Session,Id_medecin=int):
    return db.query(Medecin).filter(Id_medecin=Medecin.Id_med).first()

def get_Medecin_by_email(db: Session, email: str):
    return db.query(Medecin).filter(Medecin.Email == email).first()

def UpdateMedecin(db:Session,Id_medecin:int,Nom:str,Prenom:str,Telephone:str,Email:str,profil:str,specialite:str):
    patient_Update = get_Medecin(db=db,Id_medecin=Id_medecin)
    patient_Update.Nom = Nom
    patient_Update.Prenom = Prenom
    patient_Update.Telephone = Telephone
    patient_Update.Email = Email
    patient_Update.profil = profil
    patient_Update.specialite = specialite
    db.commit()

#Fonction de  Suppression  des Medecins
def Remove_Medecin(db:Session,Id_medecin=int):
    Rem_Medecin = get_Medecin(db=db,Id_med = Id_medecin)
    db.delete(Rem_Medecin)
    db.commit()
