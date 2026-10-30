"""Modèle Equipement (table SQL + objet Python) du projet CF-Tech.
 
Ce module définit la classe Equipement : un équipement (vidéoprojecteur,tableau, etc.) 
rattaché à une Salle par une clé étrangère `salle_id`.
Une salle peut avoir plusieurs équipements (relation 1-N).
"""

from sqlmodel import Field, Relationship, Session, SQLModel, select
from sqlalchemy.orm import joinedload
from classes.salle import Salle

import pydantic as pyd
import datetime as dt

# Bibliothèque externe (pip install tabulate) pour l'affichage en tableau
from tabulate import tabulate


class Equipement(SQLModel, table=True):
    """Équipement disponible dans une salle (table « equipement »).
 
    Attributs:
        id: Clé primaire auto-incrémentée (None tant que non inséré en base).
        nom: Nom de l'équipement (50 caractères maximum).
        description: Description facultative (255 caractères maximum).
        salle_id: Clé étrangère vers salle.id (None si l'équipement n'est
            encore affecté à aucune salle).
        salle: Objet Salle lié, chargé via la relation.
    """
    # validate_assignment : revalide un champ à chaque affectation (e.nom = ...)
    model_config = pyd.ConfigDict(validate_assignment=True)
    # --- Colonnes de la table ---
    id: int | None          = Field(default=None, primary_key=True)
    nom: str                = Field(max_length=50)
    description: str | None = Field(default=None, max_length=255, description="Description optionnelle")
    # Clé étrangère (colonne en base) vers la salle d'affectation
    salle_id: int | None    = Field(default=None, foreign_key="salle.id")
    # Relation (pas une colonne) : donne accès à l'objet Salle complet
    salle: Salle | None     = Relationship()

    def ajouter_equipement(engine, equipements):
        """Insère une liste d'équipements en base.
 
        Appel : Equipement.ajouter_equipement(engine, liste)
 
        Args:
               engine: Moteur SQLAlchemy connecté à la base.
            equipements: Liste d'objets Equipement à insérer.
        """        
        with Session(engine) as session:
            session.add_all(equipements)
            session.commit()
            for equipement in equipements:
                session.refresh(equipement)

    def afficher_equipement(engine):
        """Affiche tous les équipements avec leur salle dans un tableau (console).
 
        Appel : Equipement.afficher_equipement(engine)
 
        Le tableau fusionne les colonnes de la Salle liée (en premier) et celles
        de l'Equipement. Les valeurs absentes (équipement sans salle) sont
        affichées « N/A ».
 
        Args:
            engine: Moteur SQLAlchemy connecté à la base.
        """
        with Session(engine) as session:
            print(f"\nSalle - Equipements : ")
            a_exclure_du_role = [] # Colonne(s) spécifique au role à retirer du résultat

            # Colonnes masquées : la relation, l'id et la clé étrangère (doublons d'affichage)
            a_exclure = {"salle", "id", "salle_id"} | set(a_exclure_du_role)

            # joinedload : charge la salle dans la même requête (JOIN),
            # ce qui évite une requête supplémentaire par équipement
            # (la variable `salles` contient en réalité des équipements)
            requete = select(__class__).options(joinedload(__class__.salle))
            salles = session.exec(requete).all()

            # Rien à afficher si la table est vide
            if not salles:
                    print("Aucune donnée.")
                    return

            # Extraction et filtrage des colonnes de l'Equipement
            cols_salle = list(type(salles[0]).model_fields)
            cols_salle = [colonne for colonne in cols_salle if colonne not in a_exclure]
            
            # Extraction des colonnes de la Salle liée
            cols_utilisateur = list(type(salles[0].salle).model_fields)
            
            # En-têtes complets : colonnes de la salle d'abord, puis de l'équipement (en majuscules pour le style)
            en_tetes = [colonne.upper() for colonne in (cols_utilisateur + cols_salle)]
            # Extraction et formatage des données
            lignes = []
            for salle in salles:
                ligne = []
                
                # Données de l'utilisateur
                for colonne in cols_utilisateur:
                    valeur = getattr(salle.salle, colonne, "N/A") if salle.salle else "N/A"
                    if isinstance(valeur, (dt.date, dt.datetime)):
                        valeur = valeur.strftime("%Y-%m-%d")
                    ligne.append(valeur)
                
                # Données spécifiques au role
                for colonne in cols_salle:
                    valeur = getattr(salle, colonne, "N/A")
                    if isinstance(valeur, (dt.date, dt.datetime)):
                        valeur = valeur.strftime("%Y-%m-%d")
                    ligne.append(valeur)
                lignes.append(ligne)

            # Affichage propre avec tabulate (bordures arrondies, "N/A" pour les valeurs vides)
            print("\n" + tabulate(lignes, headers=en_tetes, tablefmt="rounded", missingval="N/A"))
            