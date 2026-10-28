

from sqlmodel import Field, Relationship, Session, SQLModel, col, create_engine, func, or_, select
from sqlalchemy.schema import CreateTable
from pathlib import Path

from classes.utilisateur import Utilisateur
from classes.formateur import Formateur


# Libération d'abord des connexions déjà ouvertes
for nom_variable in ("engine",):
    if nom_variable in globals():
        globals()[nom_variable].dispose()

# Suppression de la bdd. Bipass l'erreur en cas de fichier inexistant
for chemin in ("db/CFTeck.db",):
    Path(chemin).unlink(missing_ok=True)

# Création de la nouvelle bdd

engine = create_engine("sqlite:///db/CFTeck.db")
print("✔️  Engine prêt :", engine.url, "\n")

CreateTable(Utilisateur.__table__).compile(engine)
CreateTable(Formateur.__table__).compile(engine)


SQLModel.metadata.create_all(engine)