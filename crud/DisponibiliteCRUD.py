from models.models import Disponibilite
from datetime import  datetime
from schemas.SchemasDisponibilite import DisponibiliteSchemas
from fastapi import HTTPException
from sqlalchemy.orm import Session
from .auth import decode_access_token

def is_medecin_available(db, medecin_id, date_heure):
    # Convertir la chaîne de date_heure en objet datetime
    date_time_obj = datetime.strptime(date_heure, '%Y-%m-%d %H:%M:%S')

    # Vérifier si le médecin est disponible pour la date et l'heure spécifiées
    disponibilite = db.query(Disponibilite).filter(
        Disponibilite.medecin_id == medecin_id,
        Disponibilite.jour == date_time_obj.strftime("%A").lower(),
        Disponibilite.heure_debut <= date_time_obj.time(),
        Disponibilite.heure_fin >= date_time_obj.time()
    ).first()

    return disponibilite is not None

def create_Disponibilite(db:Session,programme:DisponibiliteSchemas,token:str):
    payload = decode_access_token(token)
    medecin_id = payload.get("sub")
    db_disponibilite = Disponibilite(
        jour = programme.jour,
        mois = programme.mois,
        annee = programme.annee,
        heure_debut = programme.heure_debut,
        heure_fin = programme.heure_fin,
        medecin_id = medecin_id,
    )
    db.add(db_disponibilite)
    db.commit()
    db.refresh(db_disponibilite)
    return  db_disponibilite

def get_Disponibilites(db:Session,skip:int=0,limit:int=100):
    return db.query(Disponibilite).offset(skip).limit(limit).all()

def get_BY_Id(db:Session,IdDisp:int):
    return db.query(Disponibilite).filter(Disponibilite.medecin_id==IdDisp).first()


def update_Disponibilite(db:Session,IdD:int,jour:str,mois:str,annee:str,heure_debut:str,heure_fin:str):
    update_disp = get_BY_Id(db,IdD)
    update_disp.jour = jour
    update_disp.mois = mois
    update_disp.annee = annee
    update_disp.heure_debut = heure_debut
    update_disp.heure_fin = heure_fin
    db.commit()


def Remove_Dispo(db:Session,IdD:int):
    db_disp = get_BY_Id(db,IdD)
    db.delete(db_disp)
    db.commit()
