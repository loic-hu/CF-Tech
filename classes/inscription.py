"""Modèle Inscription (table SQL + objet Python) du projet CF-Tech.
 
Ce module définit :
    - StatutInscription : l'énumération des statuts d'une inscription ;
    - Inscription       : la table « inscription », qui relie un Apprenant à
                          une SessionFormation (relation N-N portée par cette
                          table), avec la date, le statut et la présence.
"""

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
    """Statuts possibles d'une inscription.
 
    Hérite de `str` pour pouvoir être comparé et affiché comme une chaîne.
 
    Valeurs:
        ENREGISTRE: inscription confirmée.
        DESINSCRIT: l'apprenant s'est désinscrit.
        EN_ATTENTE: inscription en attente (ex. liste d'attente).
    """
    ENREGISTRE = 'ENREGISTRE'
    DESINSCRIT = 'DESINSCRIT'
    EN_ATTENTE = 'EN_ATTENTE'

    def __str__(self):
        """Retourne la valeur "ENREGISTRE" plutôt que "StatutInscription.ENREGISTRE"."""
        return self.value

class Inscription(SQLModel, table=True):
    """Inscription d'un apprenant à une session de formation (table « inscription »).
 
    Attributs:
        id: Clé primaire auto-incrémentée (None tant que non inséré en base).
        date_inscription: Date et heure de l'inscription (UTC), remplie
            automatiquement à la création de l'objet.
        statut_inscription: Statut de l'inscription (StatutInscription).
        presence: Présence de l'apprenant à la session (None tant que non
            renseignée).
        id_apprenant: Clé étrangère vers apprenant.id.
        id_sessionformation: Clé étrangère vers sessionformation.id.
        apprenant: Objet Apprenant lié, chargé via la relation.
        session_formation: Objet SessionFormation lié, chargé via la relation.
    """
    model_config = pyd.ConfigDict(validate_assignment=True, use_enum_values=True)

    # --- Colonnes de la table ---
    id: int | None                        = Field(default=None, primary_key=True, description="")
    date_inscription: dt.datetime         = Field(default_factory=lambda: dt.datetime.now(dt.timezone.utc), description="Date d'inscription de l'apprenant")
    statut_inscription: StatutInscription = Field(description="")
    presence: bool | None                 = Field(default=None, description="")
    # Clés étrangères (colonnes en base)
    id_apprenant: int                     = Field(foreign_key="apprenant.id", description="")
    id_sessionformation: int              = Field(foreign_key="sessionformation.id", description="")
    # Relations (pas des colonnes) : donnent accès aux objets complets
    apprenant: Apprenant                  = Relationship()
    session_formation: SessionFormation   = Relationship()



    #Vérifier que nombre d’inscrits < capacite_max de la session.
    @pyd.model_validator(mode='after')
    def valider_session(self) -> 'Inscription':
        """Vérifie que la session est ouverte et qu'il reste de la place.
 
        Règles contrôlées :
            1. la session liée doit avoir le statut « OUVERTE » ;
            2. le nombre d'inscriptions existantes doit être inférieur à
               `capacite_max` de la session.
 
        Returns:
            L'inscription elle-même si les règles sont respectées.
 
        Raises:
            ValueError: si la session n'est pas ouverte, n'existe pas ou a
                atteint sa capacité maximale.
 
        Note:
            Le contrôle de capacité n'est effectué que si une variable
            `engine` existe dans les variables globales de ce module ;
            sinon la méthode retourne l'inscription sans rien vérifier.
        """
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
 
        Appel : Inscription.ajouter_inscriptions(engine, liste)
 
        Args:
            engine: Moteur SQLAlchemy connecté à la base.
            sessions_formation: Liste d'objets Inscription à insérer (malgré
                son nom, ce paramètre ne contient pas des sessions).
        """
        with Session(engine) as session:
            session.add_all(sessions_formation)         # 1. on confie l'objet à la session (rien n'est encore écrit)
            session.commit()                            # 2. la session envoie l'INSERT et valide la transaction
            for une_session_formation in sessions_formation:
                session.refresh(une_session_formation)  # 3. on recharge l'objet depuis la base, pour récupérer son id


    def afficher_inscription(engine):
        """Affiche toutes les inscriptions dans un tableau (console).
 
        Appel : Inscription.afficher_inscription(engine)
 
        Colonnes affichées : id, date et statut de l'inscription, nom de
        l'apprenant, titre et date de début de la session.
 
        Args:
            engine: Moteur SQLAlchemy connecté à la base.
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