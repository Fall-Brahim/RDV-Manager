from fastapi import  APIRouter,Depends,HTTPException
from schemas.SchemasRendezVous import RendezVousSchemas,RdvSchemasUpdate
from crud.auth import oauth2_scheme,decode_access_token
from config.db import get_db
from sqlalchemy.orm import Session
from crud.RendezVousCRUD import *


Rdvrouter = APIRouter()

@Rdvrouter.get('/rendezvous/',response_model=list[RendezVousSchemas])
async def get_Rdv(skip:int=0,limit:int=100,db:Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["type_User"]!="patients":
        raise HTTPException(status_code=403,detail="Permission denied")
    Rdvs = get_all_RdV(db,skip=skip,limit=limit)
    return Rdvs

#Route pour la Recherche des Rendez vous cree
@Rdvrouter.get("/rendezvous/{Rdv_Id}",response_model=RendezVousSchemas)
async def get_Rdv_by_ID(Id_R:int,db:Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["type_User"]!="patients":
        raise HTTPException(status_code=403,detail="Permission denied")
    Rdvs= getRdv(db,Id_Rdv=Id_R)
    if Rdvs is None:
        raise HTTPException(status_code=404,detail="Rendez Vous non Trouvez")
    return Rdvs

#Route de creation des Rendez Vous
@Rdvrouter.post("/rendezvous/",response_model=RendezVousSchemas)
async def CreateRdv(rendezvous:RendezVousSchemas,db:Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["type_User"]!="patients":
        raise HTTPException(status_code=403,detail="Permission denied")
    return CreateRdv(db,rendezvous)

@Rdvrouter.put("/rendezvous/{rdv_Id}",response_model=RendezVousSchemas)
async def update_rdv(IdR:int,rendezvous:RdvSchemasUpdate,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload =decode_access_token(token)
    if payload["Usertype"] != "patients":
        raise HTTPException(status_code=403,detail="Permission Denied")
    db_Rdv = getRdv(db,Id_Rdv=IdR)
    if db_Rdv is None:
        raise HTTPException(status_code=404,detail="Rendez vous inexistante")
    update_Rdv(
        db,
        Id_Rdv=IdR,
        date_heure=rendezvous.date_heure,
        PatientID = rendezvous.PatientID,
        MedecinID = rendezvous.MedecinID,
        Notes = rendezvous.Notes,
    )
    return rendezvous

@Rdvrouter.delete("/rendezvous/{Rdv_ID}")
async def Delete_rdv(Rdv_Id:int,db: Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_Type"] != "patients":
        raise HTTPException(status_code=403,detail="Permission denied")

    db_Rdv = get_Rdv(db,Id_Rdv=Rdv_Id)
    if db_Rdv is None:
        raise HTTPException(status_code=404,detail="Rendez-vous non Trouver")
    removeRdv(db,Id_Rdv=Rdv_Id)
    return {"message ":"Rendez-vous Supprimer avec success"}