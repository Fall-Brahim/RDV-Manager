from fastapi import FastAPI
from routes.routePatient import Patientrouter
from routes.routeMedecin import Medecinrouter
from routes.routeRendezVous import Rdvrouter
from routes.routesDisponibilte import DispRoute
from config.db import Base, engine
from models import *
from crud.auth import auth

app = FastAPI()

# Créer toutes les tables dans la base de données
models.Base.metadata.create_all(bind=engine)

# Inclure les routeurs dans l'application FastAPI
app.include_router(Patientrouter)
app.include_router(Medecinrouter)
#
app.include_router(DispRoute)
app.include_router(Rdvrouter)
app.include_router(auth)
