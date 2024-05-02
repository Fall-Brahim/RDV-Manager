from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from schemas.SchemasMedecin import MedecinSchemas,MedecinUpdate
from config.db import SessionLocal
from crud.MedecinCRUD import (
create_Medecin,
Get_All_Medecin,
get_Medecin,
Remove_Medecin,
UpdateMedecin,
)
from crud.auth import oauth2_scheme,decode_access_token
from config.db import get_db

Medecinrouter = APIRouter()

@Medecinrouter.get('/Medecin/', response_model=list[MedecinSchemas])
async def GetALLMedecin(skip:int=0,limit:int=0,db:Session=Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_type"] != "medecin":
        raise HTTPException(status_code=403, detail="Permission denied")
    medecins = Get_All_Medecin(db=db,skip=skip,limit=limit)
    return medecins

@Medecinrouter.get('/Medecin/{medecin_Id}', response_model=MedecinSchemas)
async def Get_Medecin(medecin_Id:int, db:Session=Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_type"] != "medecin":
        raise HTTPException(status_code=403, detail="Permission denied")
    medecin = get_Medecin(db, Id_medecin=medecin_Id)
    if medecin is None:
        raise HTTPException(status_code=404, detail="Medecin non Trouver")
    return medecin

@Medecinrouter.post('/Medecin/',response_model=MedecinSchemas)
async def create_Med(medecin:MedecinSchemas,db:Session=Depends(get_db)):
    if db.query(Patient).filter(Medecin.Email == medecin.Email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already exists",
        )
    new_medecin = create_Medecin(db,medecin)
    return {"message":"Medecin ajouter avec success"}





@Medecinrouter.put('/Medecin/{medecin_id}',response_model=MedecinSchemas)
async def Update_Med(medecin_id:int,medecin:MedecinUpdate,db:Session=Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_type"] != "medecin":
        raise HTTPException(status_code=403, detail="Permission denied")

    db_medecin = get_Medecin(db,Id_medecin=medecin_id)
    if db_medecin is None:
        raise HTTPException(status_code=404,detail="Medecin non trouver !!")
    UpdateMedecin(
        db,
        Id_medecin=medecin_id,
        Nom=medecin.Nom,
        Prenom=medecin.Prenom,
        Telephone=medecin.Telephone,
        Email=medecin.Email,
        profil=medecin.profil,
        specialite=medecin.specialite
    )
    return medecin

@Medecinrouter.delete('/Medecin/{medecin_id}')
async def RemoveMedecin(medecin_id: int, db:Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_type"] != "medecin":
        raise HTTPException(status_code=403, detail="Permission denied")
    db_medecin = get_Medecin(Id_medecin=medecin_id)
    if db_medecin is None:
        raise HTTPException(status_code=404, detail="Medecin non trouver")
    Remove_Medecin(db, Id_medecin=medecin_id)
    return {"message": "Suppression effectuer avec succès"}
