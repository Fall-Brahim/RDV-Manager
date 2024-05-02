from crud.auth import oauth2_scheme,decode_access_token
from fastapi import APIRouter,Depends,HTTPException
from config.db import get_db
from sqlalchemy.orm import Session
from schemas.SchemasDisponibilite import DisponibiliteSchemas
from crud.auth import oauth2_scheme,decode_access_token
from crud.DisponibiliteCRUD import *

DispRoute = APIRouter()

@DispRoute.get("/programmes/",response_model=list[DisponibiliteSchemas])
async def get_Disponibles(skip:int=0,limit:int=0,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_type"]!="patients":
        raise HTTPException(status_code=403,detail="Permission denied")
    disp = get_Disponibilites(db,skip=skip,limit=limit)
    if disp is None:
        raise HTTPException(status_code=404,detail="Pas de medecin disponible ")
    return disp

@DispRoute.get("/programmes/{disp_id}/",response_model=DisponibiliteSchemas)
async def get_By_ID(IdD:int,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_type"] != "patients":
        raise HTTPException(status_code=403,detail="Permission denied")
    disp = get_BY_Id(db,IdD)
    if disp is None:
        raise HTTPException(status_code=404,detail="Non Diponible")
    return disp

@DispRoute.post("/programmes/",response_model=DisponibiliteSchemas)
async def create_Disp(db:Session=Depends(get_db),disponibilite=DisponibiliteSchemas,token:str=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_type"] != "medecin":
        raise HTTPException(status_code=403, detail="Permission denied")
    return create_Disponibilite(db,disponibilite)

@DispRoute.delete("/programmes/{disp_id}/")
async def Remove_Disp(idD:int,db:Session=Depends(get_db),token:str=Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    if payload["user_Type"] != "medecin":
        raise HTTPException(status_code=403,detail="Permission denied")
    db_disp = get_By_ID(db,id=idD)
    if db_disp is None:
        raise HTTPException(status_code=404,detail="disponibilite inexistant!!")
    return {"message":"Suppression effectuer avec success"}