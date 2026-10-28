from sqlmodel import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select, Column, JSON
from sqlalchemy.orm import joinedload

from decimal              import Decimal
from classes.utilisateur  import Utilisateur

import pydantic   as pyd
import datetime   as dt

class Personnel(SQLModel, table=True):
    """
    Représente la classe Personnel, enfant d'Utilisateur
    """
    # FORCE la validation stricte de Pydantic v2 dès la création de l'objet
    model_config = pyd.ConfigDict(validate_assignment=True)

    id: int | None                  = Field(default=None, primary_key=True)
    poste: str                      = Field(max_length=50)                 
    date_prise_fonction: dt.date    = Field(default_factory=lambda: dt.date.now(dt.timezone.utc), description="Date de prise de fonction du personnel")
    responsabilites: list[str]      = Field(default=[], sa_column=Column(JSON))
    id_utilisateur: int             = Field(unique=True, foreign_key="utilisateur.id")

    utilisateur: Utilisateur        = Relationship()

    def ajouter_personnel(engine, personnels):
            """
            
            """
            with Session(engine) as session:
                session.add_all(personnels)       # 1. on confie l'objet à la session (rien n'est encore écrit)
                session.commit()        # 2. la session envoie l'INSERT et valide la transaction
                for personnel in personnels:
                    session.refresh(personnel)   # 3. on recharge l'objet depuis la base, pour récupérer son id



    def afficher_personnel(engine):
            """
            Affiche une liste du personnel avec leurs infos sous forme de tableau.
            """

            with Session(engine) as session:
                requete = (
                    select(Personnel)
                    .options(joinedload(Personnel.utilisateur))
                ) 
            
                personnel = session.exec(requete).all()

            if not personnel:
                print("Aucune donnée.")
                return
            
            # 1. On récupère les colonnes du Formateur ET de l'Utilisateur lié
            cols_personnel = list(type(personnel[0]).model_fields)
            # On exclut 'utilisateur' (qui est la relation) et 'id_utilisateur' pour éviter les doublons d'affichage
            if "utilisateur" in cols_personnel: cols_personnel.remove("utilisateur")
            if "id" in cols_personnel: cols_personnel.remove("id")
            if "id_utilisateur" in cols_personnel: cols_personnel.remove("id_utilisateur")
                            
                    
            # On ajoute les colonnes de l'utilisateur (en excluant son id)
            cols_utilisateur = list(type(personnel[0].utilisateur).model_fields)
                    
            # En-tête complet du tableau
            colonnes = cols_utilisateur + cols_personnel
            
            # 2. Extraction des valeurs pour chaque ligne
            lignes = []
            for f in personnel:
                ligne = []
            # Valeurs de l'utilisateur lié (via la Relationship)
                for c in cols_utilisateur:
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
