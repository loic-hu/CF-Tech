"""Modèle Personnel (table SQL + objet Python) du projet CF-Tech.
 
Ce module définit :
    - NiveauEtude : l'énumération des niveaux d'études possibles ;
    - Personnel   : la table « personnel », reliée à la table « utilisateur »
                    par une relation 1-1 (id_utilisateur).
 
Un membre du Personnel ne contient pas nom, prénom ni email : ces données sont dans
l'utilisateur associé, accessible via la relation `personnel.utilisateur`.
"""

from sqlmodel import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select, Column, JSON
from sqlalchemy.orm import joinedload

from decimal              import Decimal
from classes.utilisateur  import Utilisateur

import pydantic   as pyd
import datetime   as dt

class Personnel(SQLModel, table=True):
    """Profil d'un membre du Personnel de la plateforme (table « personnel »).
 
   Chaque membre du Personnel est relié à un unique Utilisateur (relation 1-1) qui
   porte les informations communes : nom, prénom, email, etc.
 
   Attributs:
        id: Clé primaire auto-incrémentée (None tant que non inséré en base).
        poste: Intitulé du poste (50 caractères maximum), ex. « Responsable pédagogique ».
        date_prise_fonction: Date de prise de fonction.
        responsabilites: Liste de responsabilités, stockée en base au format JSON (liste vide par défaut).
        id_utilisateur: Clé étrangère vers utilisateur.id, unique (1 profil personnel au maximum par utilisateur).
        utilisateur: Objet Utilisateur lié, chargé via la relation.
   """
    # validate_assignment : revalide un champ à chaque affectation (p.poste = ...)
    model_config = pyd.ConfigDict(validate_assignment=True)
    # --- Colonnes de la table ---
    id: int | None                  = Field(default=None, primary_key=True)
    poste: str                      = Field(max_length=50)                 
    date_prise_fonction: dt.date    = Field(default_factory=lambda: dt.date.now(dt.timezone.utc), description="Date de prise de fonction du personnel")
    responsabilites: list[str]      = Field(default=[], sa_column=Column(JSON))
    id_utilisateur: int             = Field(unique=True, foreign_key="utilisateur.id")

    utilisateur: Utilisateur        = Relationship()

    def ajouter_personnel(engine, personnels):
        """Insère une liste de membres du personnel (et leurs utilisateurs liés) en base.

        Appel : Personnel.ajouter_personnel(engine, liste)

        Args:
            engine: Moteur SQLAlchemy connecté à la base.
            personnels: Liste d'objets Personnel, chacun avec son Utilisateur associé via `utilisateur=...`.

        Note:
            L'Utilisateur lié est ajouté automatiquement avec le Personnel.
        """
        with Session(engine) as session:
            session.add_all(personnels)       # 1. on confie l'objet à la session (rien n'est encore écrit)
            session.commit()        # 2. la session envoie l'INSERT et valide la transaction
            for personnel in personnels:
                session.refresh(personnel)   # 3. on recharge l'objet depuis la base, pour récupérer son id



    def afficher_personnel(engine):
        """Affiche tout le personnel dans un tableau aligné (console).
 
        Appel : Personnel.afficher_personnel(engine)

        Le tableau fusionne les colonnes de l'Utilisateur (id, nom, prénom, email, date de création, état actif) 
        et celles du Personnel (poste, date de prise de fonction, responsabilités).

        Args:
            engine: Moteur SQLAlchemy connecté à la base.
        """

        with Session(engine) as session:
            # joinedload : charge l'utilisateur dans la même requête (JOIN),
            # ce qui permet de le lire même après la fermeture de la session
            requete = (
                select(Personnel)
                .options(joinedload(Personnel.utilisateur))
            ) 
            personnel = session.exec(requete).all()

        # Rien à afficher si la table est vide
        if not personnel:
            print("Aucune donnée.")
            return
        
        # 1. On récupère les colonnes du Personnel ET de l'Utilisateur lié
        cols_personnel = list(type(personnel[0]).model_fields)
        # On exclut 'utilisateur' (qui est la relation) et 'id_utilisateur' pour éviter les doublons d'affichage
        if "utilisateur" in cols_personnel: cols_personnel.remove("utilisateur")
        if "id" in cols_personnel: cols_personnel.remove("id")
        if "id_utilisateur" in cols_personnel: cols_personnel.remove("id_utilisateur")
                        
                
        # Colonnes de l'utilisateur (id inclus : c'est l'id affiché en première colonne)
        cols_utilisateur = list(type(personnel[0].utilisateur).model_fields)
                
        # En-tête complet du tableau : colonnes utilisateur d'abord, puis personnel
        colonnes = cols_utilisateur + cols_personnel
        
        # 2. Extraction des valeurs pour chaque ligne
        lignes = []
        for f in personnel:
            # Valeurs de l'utilisateur lié (via la Relationship)
            ligne = []
            for c in cols_utilisateur:
                # "N/A" si le menbre du personnel n'a pas d'utilisateur lié
                valeur = getattr(f.utilisateur, c, "N/A") if hasattr(f, "utilisateur") and f.utilisateur else "N/A"
                # Formatage propre si c'est une date ou un datetime
                if isinstance(valeur, (dt.date, dt.datetime)):
                    valeur = valeur.strftime("%Y-%m-%d")
                ligne.append(str(valeur))
                    
            # Valeurs spécifiques au personnel
            for c in cols_personnel:
                valeur = getattr(f, c)
                if isinstance(valeur, (dt.date, dt.datetime)):
                    valeur = valeur.strftime("%Y-%m-%d")
                ligne.append(str(valeur))
                        
            lignes.append(ligne)
        
        # 3. Calcul de la largeur de chaque colonne (votre logique d'origine conservée)
        largeurs = [max(len(c), *(len(l[i]) for l in lignes))
                    for i, c in enumerate(colonnes)]
        
        # 4. Affichage à l'écran
        print("\n" + "  ".join(c.upper().ljust(w) for c, w in zip(colonnes, largeurs)))
        print("-" * (sum(largeurs) + (len(largeurs) * 2))) # Ligne de séparation
        for l in lignes:
            print("  ".join(v.ljust(w) for v, w in zip(l, largeurs)))
