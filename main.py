

from classes.utilisateur import Utilisateur

import db.init_db as db


try:
    utilisateurs = [
    Utilisateur(id=None, nom="Dupont",  prenom="Marie",   email="marie.dupont@mail.fr"),
    Utilisateur(id=None, nom="Martin",  prenom="Lucas",   email="lucas.martin@mail.fr"),
    Utilisateur(id=None, nom="Bernard", prenom="Emma",    email="emma.bernard@mail.fr"),
    Utilisateur(id=None, nom="Petit",   prenom="Hugo",    email="hugo.petit@mail.fr"),
    Utilisateur(id=None, nom="Durand",  prenom="Chloé",   email="chloe.durand@mail.fr"),
    Utilisateur(id=None, nom="Leroy",   prenom="Nathan",  email="nathan.leroy@mail.fr", est_actif=False),
    Utilisateur(id=None, nom="Moreau",  prenom="Léa",     email="lea.moreau@mail.fr"),
    Utilisateur(id=None, nom="Simon",   prenom="Thomas",  email="thomas.simon@mail.fr"),
    Utilisateur(id=None, nom="Laurent", prenom="Camille", email="camille.laurent@mail.fr", est_actif=False),
    Utilisateur(id=None, nom="Garcia",  prenom="Julien",  email="julien.garcia@mail.fr"),
    ]

    Utilisateur.ajouter_utilisateurs(utilisateurs, db.engine)
    Utilisateur.afficher(utilisateurs)

except Exception as e:
    print("Erreur :",e)

