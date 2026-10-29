from sqlmodel             import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select, Column, JSON
from sqlalchemy.orm       import joinedload
from sqlalchemy           import func

from tabulate             import tabulate
from decimal              import Decimal
from enum                 import Enum

from classes.utilisateur import Utilisateur
from classes.apprenant   import Apprenant
from classes.session     import SessionFormation

import pydantic   as pyd
import datetime   as dt


class StatutInscription(str, Enum):
    ENREGISTRE = 'ENREGISTRE'
    DESINSCRIT = 'DESINSCRIT'
    EN_ATTENTE = 'EN_ATTENTE'

    def __str__(self):
        return self.value

class Inscription(SQLModel, table=True):
    """
    
    """
    model_config = pyd.ConfigDict(validate_assignment=True, use_enum_values=True)

    id: int | None                        = Field(default=None, primary_key=True, description="")
    date_inscription: dt.datetime         = Field(default_factory=lambda: dt.datetime.now(dt.timezone.utc), description="Date d'inscription de l'apprenant")
    statut_inscription: StatutInscription = Field(description="")
    presence: bool | None                 = Field(default=None, description="")

    id_apprenant: int                     = Field(foreign_key="apprenant.id", description="")
    id_sessionformation: int              = Field(foreign_key="sessionformation.id", description="")
    apprenant: Apprenant                  = Relationship()
    session_formation: SessionFormation   = Relationship()



    #Vérifier que nombre d’inscrits < capacite_max de la session.
    @pyd.model_validator(mode='after')
    def valider_session(self) -> 'Inscription':
        # Contrainte CHECK(session.statut = 'OUVERTE')
        if self.session_formation and self.session_formation.statut != "OUVERTE":
            raise ValueError("La session voulue n'est pas ouverte.")

        # Récupération sécurisée du moteur de base de données
        engine = globals().get("engine")
        if not engine:
            return self

        # Validation de la capacité restante de la session
        with Session(engine) as session_db:
            # Récupérer la session de formation pour connaître sa capacité max propre
            session_form = session_db.get(SessionFormation, self.id_sessionformation)
            if not session_form:
                raise ValueError(f"La session avec l'ID {self.id_sessionformation} n'existe pas.")

            # Compter le nombre d'inscriptions déjà enregistrées pour cette session
            statement = (
                select(func.count(Inscription.id))
                .where(Inscription.id_sessionformation == self.id_sessionformation)
            )
            nb_inscrits = session_db.exec(statement).one()

            # Vérifier s'il reste de la place
            if nb_inscrits >= session_form.capacite_max:
                raise ValueError(
                    f"Impossible de s'inscrire : la session a atteint sa capacité maximale "
                    f"de {session_form.capacite_max} participants."
                )

        return self


    def ajouter_inscriptions(engine, sessions_formation:list):
        """
        Ajouter une ou des inscriptions(s) à une formation à partir d'une liste d'instance(s)
        """
        with Session(engine) as session:
            session.add_all(sessions_formation)         # 1. on confie l'objet à la session (rien n'est encore écrit)
            session.commit()                            # 2. la session envoie l'INSERT et valide la transaction
            for une_session_formation in sessions_formation:
                session.refresh(une_session_formation)  # 3. on recharge l'objet depuis la base, pour récupérer son id


    def afficher_inscription(engine):
        """
        
        """
        with Session(engine) as session:

            print(f"\nInscriptions : ")
            
            requete = (
                select(
                    Inscription.id,
                    Inscription.date_inscription,
                    Inscription.statut_inscription,
                    Utilisateur.nom.label("nom_apprenant"),                 # Cible directement la classe Utilisateur
                    SessionFormation.titre.label("titre_session"),          # Cible directement la classe SessionFormation
                    SessionFormation.date_debut.label("date_debut_session")
                )
                # 1. Jointure en cascade : Inscription -> Apprenant -> Utilisateur
                .join(Apprenant, Inscription.id_apprenant == Apprenant.id)
                .join(Utilisateur, Apprenant.id_utilisateur == Utilisateur.id) # Ajuster id_utilisateur selon votre modèle
                
                # 2. Jointure parallèle : Inscription -> SessionFormation
                .join(SessionFormation, Inscription.id_sessionformation == SessionFormation.id)
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