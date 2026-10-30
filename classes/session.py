"""Modèle SessionFormation (table SQL + objet Python) du projet CF-Tech.
 
Ce module définit :
    - StatutSession     : l'énumération des statuts d'une session ;
    - SessionFormation  : la table « sessionformation » : un cours ou un atelier
                          planifié dans une salle, animé par un formateur, avec
                          dates, capacité et statut.
"""

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
    """Statuts possibles d'une session de formation.
 
    Hérite de `str` pour pouvoir être comparé et affiché comme une chaîne.
 
    Valeurs:
        OUVERTE: les inscriptions sont possibles.
        FERMEE: les inscriptions sont closes.
        ARCHIVEE: session terminée et archivée.
    """
    OUVERTE  = 'OUVERTE'
    FERMEE   = 'FERMEE'
    ARCHIVEE = 'ARCHIVEE'

    def __str__(self):
        return self.value


class SessionFormation(SQLModel, table=True):    #On évite le nom de classe "Session" reservé par SQLModel
    """Session de formation planifiée (table « sessionformation »).
 
    Le nom `Session` est évité car SQLModel exporte déjà une classe `Session`
    (la session de base de données), utilisée plus bas dans ce fichier.
 
    Attributs:
        id: Clé primaire auto-incrémentée (None tant que non inséré en base).
        titre: Titre de la session (100 caractères maximum).
        description: Description facultative (255 caractères maximum).
        date_debut: Date et heure de début.
        date_fin: Date et heure de fin (doit être après le début).
        capacite_max: Nombre maximal de participants (ne doit pas dépasser la
            capacité de la salle).
        statut: Statut de la session (StatutSession), « OUVERTE » par défaut.
        id_formateur: Clé étrangère vers formateur.id.
        id_salle: Clé étrangère vers salle.id.
        formateur: Objet Formateur lié, chargé via la relation.
        salle: Objet Salle lié, chargé via la relation.
    """
    # validate_assignment : revalide un champ à chaque affectation (s.titre = ...)
    # use_enum_values     : stocke la valeur de l'Enum (ex. "OUVERTE") et non le membre
    model_config = pyd.ConfigDict(validate_assignment=True, use_enum_values=True)

    # --- Colonnes de la table (Field(...) = champ obligatoire) ---
    id: int | None                                 = Field(default=None, primary_key=True, description="")
    titre: str                                     = Field(max_length=100, description="")
    description: str | None                        = Field(default=None, max_length=255, description="")
    date_debut: dt.datetime                        = Field(... , description="Date et heure de début de session")
    date_fin: dt.datetime                          = Field(... , description="Date et heure de fin de session")
    capacite_max: int                              = Field(... , description="") # le=Salle.capacite
    statut: StatutSession                          = Field(default="OUVERTE", description="")
    # Clés étrangères (colonnes en base)
    id_formateur: int                              = Field(foreign_key="formateur.id", description="")
    id_salle: int                                  = Field(foreign_key="salle.id", description="")
    # Relations (pas des colonnes) : donnent accès aux objets complets
    formateur: Formateur                           = Relationship()
    salle: Salle                                   = Relationship()


    @pyd.field_validator("date_debut")
    @classmethod
    def valider_date_salle(cls, v: dt.datetime, info: pyd.ValidationInfo) -> dt.datetime:
        """Vérifie que la date de début est strictement antérieure à la date de fin.
 
        Args:
            v: Date de début à contrôler.
            info: Contexte de validation ; `info.data` contient les champs déjà
                validés (ici on y lit `date_fin`).
 
        Returns:
            La date de début inchangée si elle est valide.
 
        Raises:
            ValueError: si la date de début n'est pas avant la date de fin.
 
        Note:
            Pydantic valide les champs dans l'ordre de leur déclaration. Comme
            `date_fin` est déclarée après `date_debut`, elle n'est pas encore
            disponible dans `info.data` à ce moment-là : le contrôle risque de
            ne jamais se déclencher. Le placer sur `date_fin` (en lisant
            `date_debut`) ou dans un model_validator règle ce point.
        """
        
        # date_fin déjà validée (None si absente)
        date_fin = info.data.get("date_fin")
        
        if date_fin and v >= date_fin:
            raise ValueError("La date de début doit être strictement antérieure à la date de fin.")
            
        return v


    @pyd.model_validator(mode='after')
    def valider_capacite_salle(self) -> 'SessionFormation':
        """Vérifie que la capacité de la session ne dépasse pas celle de la salle.
 
        Returns:
            La session elle-même si la capacité est valide.
 
        Raises:
            ValueError: si la salle n'existe pas ou si `capacite_max` est
                supérieure à la capacité de la salle.
 
        Note:
            Le contrôle n'est effectué que si une variable `engine` existe dans
            les variables globales de ce module ; sinon la méthode retourne la
            session sans rien vérifier. Sur un modèle table=True, ce validator
            n'est de toute façon pas appelé à la création de l'objet.
        """
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
 
        Appel : SessionFormation.ajouter_sessions(engine, liste)
 
        Args:
            engine: Moteur SQLAlchemy connecté à la base.
            sessions_formation: Liste d'objets SessionFormation à insérer.
        """
        with Session(engine) as session:
            session.add_all(sessions_formation)         # 1. on confie l'objet à la session (rien n'est encore écrit)
            session.commit()                            # 2. la session envoie l'INSERT et valide la transaction
            for session_formation in sessions_formation:
                session.refresh(session_formation)      # 3. on recharge l'objet depuis la base, pour récupérer son id


    def afficher_sessions(engine):
        """Affiche toutes les sessions de formation dans un tableau (console).
 
        Appel : SessionFormation.afficher_sessions(engine)
 
        Colonnes affichées : id, titre, dates de début et de fin, et nom du
        formateur (nom de son Utilisateur).
 
        Args:
            engine: Moteur SQLAlchemy connecté à la base.
        """
        with Session(engine) as session:

            print(f"\nSessions de formation : ")

            # Requête sur des colonnes précises (et non sur des objets entiers) :
            # le .label() donne un nom clair à la colonne du formateur
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
