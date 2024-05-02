from sqlalchemy import Column,Integer,String,DateTime,ForeignKey,Text,Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()

Genre = Enum("Homme", "Femme", name="genre_enum")

class Patient(Base):
    __tablename__ = "patients"

    ID_U = Column(Integer,primary_key=True,index=True) # cle primaire auto-incrmente
    Nom = Column(String(180))
    Prenom = Column(String(180))
    Telephone = Column(Integer)
    Email = Column(String(155),unique=True) # l'adresse Email est unique
    Mot_de_Passe = Column(String(255)) # mot de passe
    Sexe = Column(Genre)
    Profil = Column(String(255)) # Photo de profile doit etre obligatoire
    Date_Naissance = Column(DateTime)
    rdvs = relationship("RendezVous", back_populates="patient")

class Medecin(Base):
    __tablename__ = "medecin"

    Id_med= Column(Integer,primary_key=True,index=True)
    Nom = Column(String(180))
    Prenom = Column(String(180))
    Telephone = Column(Integer) #
    Email = Column(String(155), unique=True)
    mdp = Column(String(255))
    sexe = Column(Genre)
    profil = Column(String(255)) # Profil du medecin aussi est necessaire
    specialite = Column(String(255))
    # Ajoute la relation avec les disponibilités du médecin
    disponibilites = relationship("Disponibilite", back_populates="medecin")
    rdvs = relationship("RendezVous", back_populates="medecin")

class RendezVous(Base):
    __tablename__ = "rendez_vous"

    Id_Rdv = Column(Integer,primary_key=True,index=True)
    date_heure = Column(DateTime)
    PatientID = Column(Integer,ForeignKey('patients.ID_U'))
    patient = relationship("Patient", back_populates="rdvs")
    MedecinID = Column(Integer,ForeignKey('medecin.Id_med'))
    medecin = relationship("Medecin", back_populates="rdvs")
    Notes = Column(String(255),nullable=True) # des Documents ou Ordonnance pour les


# Calendrier du Medecin
class Disponibilite(Base):
    __tablename__ = "disponibilites"

    id = Column(Integer, primary_key=True, index=True)
    jour = Column(String(10))  # Par exemple, "lundi", "mardi", etc.
    mois = Column(String(10))  # Par exemple, "Janvier", "Fevrier"...etc.
    annee = Column(String(10)) # Par Exemple, "2024"
    heure_debut = Column(DateTime)
    heure_fin = Column(DateTime)
    medecin_id = Column(Integer, ForeignKey('medecin.Id_med'))  # Clé étrangère vers le médecin
    # Relation avec le modèle Medecin
    medecin = relationship("Medecin", back_populates="disponibilites")

class Consultation(Base):
    __tablename__ = "consultations"

    Id_Consultations = Column(Integer, primary_key=True, index=True)
    DhConsultations = Column(DateTime)
    patient_id = Column(Integer, ForeignKey("patients.ID_U"))  # Utilisation de la clé étrangère
    medecin_id = Column(Integer, ForeignKey("medecin.Id_med"))  # Utilisation de la clé étrangère
    description = Column(Text)

    # Relations avec les modèles Patient et Medecin
    patient = relationship("Patient", backref="consultations")  # Utilisation de relationship
    medecin = relationship("Medecin", backref="consultations")  # Utilisation de relationship
