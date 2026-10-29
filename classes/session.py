from sqlmodel             import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select, Column, JSON
from sqlalchemy.orm       import joinedload
from sqlalchemy           import func

from tabulate             import tabulate
from decimal              import Decimal
from enum                 import Enum


from classes.utilisateur  import Utilisateur
from classes.formateur    import Formateur
from classes.salle        import Salle
# from classes.inscription  import Inscription

import pydantic   as pyd
import datetime   as dt




class StatutSession(str, Enum):
    """
    
    """
    OUVERTE  = 'OUVERTE'
    FERMEE   = 'FERMEE'
    ARCHIVEE = 'ARCHIVEE'

    def __str__(self):
        return self.value


class SessionFormation(SQLModel, table=True):    #On évite le nom de classe "Session" reservé par SQLModel
    """
    
    """
    model_config = pyd.ConfigDict(validate_assignment=True, use_enum_values=True)
   
    id: int | None                                 = Field(default=None, primary_key=True, description="")
    titre: str                                     = Field(max_length=100, description="")
    description: str | None                        = Field(default=None, max_length=255, description="")
    date_debut: dt.datetime                        = Field(... , description="Date et heure de début de session")
    date_fin: dt.datetime                          = Field(... , description="Date et heure de fin de session")
    capacite_max: int                              = Field(... , description="") # le=Salle.capacite
    statut: StatutSession                          = Field(default="OUVERTE", description="")

    id_formateur: int                              = Field(foreign_key="formateur.id", description="")
    id_salle: int                                  = Field(foreign_key="salle.id", description="")
    formateur: Formateur                           = Relationship()
    salle: Salle                                   = Relationship()


    @pyd.field_validator("date_debut")
    @classmethod
    def valider_date_salle(cls, v: dt.datetime, info: pyd.ValidationInfo) -> dt.datetime:
        
        date_fin = info.data.get("date_fin")
        
        if date_fin and v >= date_fin:
            raise ValueError("La date de début doit être strictement antérieure à la date de fin.")
            
        return v


    @pyd.model_validator(mode='after')
    def valider_capacite_salle(self) -> 'SessionFormation':

        # Récupération de l'engine pour vérifier la capacité physique de la salle
        engine = globals().get("engine")
        if not engine:
            return self

        with Session(engine) as session_db:
            salle_db = session_db.get(Salle, self.id_salle)
            if not salle_db:
                raise ValueError(f"La salle avec l'ID {self.id_salle} n'existe pas.")

            # Vérification : Le quota de la session ne doit pas dépasser la limite physique de la salle
            if self.capacite_max > salle_db.capacite:
                raise ValueError(
                    f"La capacité de la session ({self.capacite_max} personnes) "
                    f"ne peut pas dépasser la capacité maximale de la salle ({salle_db.capacite} places)."
                )

        return self


    def ajouter_sessions(engine, sessions_formation:list):
        """
        Ajouter une ou des session(s) de formation à partir d'une liste d'instance(s)
        """
        with Session(engine) as session:
            session.add_all(sessions_formation)         # 1. on confie l'objet à la session (rien n'est encore écrit)
            session.commit()                            # 2. la session envoie l'INSERT et valide la transaction
            for session_formation in sessions_formation:
                session.refresh(session_formation)      # 3. on recharge l'objet depuis la base, pour récupérer son id


    def afficher_sessions(engine):
        """
        
        """
        with Session(engine) as session:

            print(f"\nSessions de formation : ")
            
            requete = (
                select(
                    SessionFormation.id,
                    SessionFormation.titre,
                    SessionFormation.date_debut,
                    SessionFormation.date_fin,
                    Utilisateur.nom.label("formateur")
                )
                # Jointure en cascade :  -> Formateur -> Utilisateur
                .join(Formateur, SessionFormation.id_formateur == Formateur.id)
                .join(Utilisateur, Formateur.id_utilisateur == Utilisateur.id)
                
                # Jointure :  -> Salle
                .join(Salle, SessionFormation.id_salle == Salle.id)
                   
            )

            donnees = session.exec(requete).all()

            if not donnees:
                print("Aucune donnée.")
                return

            # Extraction et filtrage des colonnes
            cols_donnees = donnees[0]._fields
            
            # En-têtes complets (convertis en majuscules pour le style)
            en_tetes = [colonne.upper() for colonne in cols_donnees]

            # Extraction et formatage des données
            lignes = []
            for donnee in donnees:
                ligne = []
                
                # Données
                for colonne in cols_donnees:
                    valeur = getattr(donnee, colonne, "N/A")
                    if isinstance(valeur, (dt.date, dt.datetime)):
                        valeur = valeur.strftime("%Y-%m-%d")
                    ligne.append(valeur)
                    
                lignes.append(ligne)

            # Affichage propre avec tabulate
            print("\n" + tabulate(lignes, headers=en_tetes, tablefmt="rounded", missingval="N/A"))
