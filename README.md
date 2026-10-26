# CF-Tech : Base de données pilotée par un ORM

## 1. Contexte et objectifs

- **Contexte** : migration d'Excel + ERP vieillissant vers une base relationnelle centralisée.
  - Vous êtes Data Engineer au sein d’un centre de formation (CF-Tech) qui dispense des cours
et ateliers sur les technologies numériques. Jusqu’à présent, les informations concernant les
sessions, les salles, les formateurs et les apprenants étaient gérées à la main, au moyen de
fichiers Excel et d’un ERP vieillissant. La direction souhaite passer à une solution plus
robuste : une base de données relationnelle pilotée par un ORM (SQLAlchemy/SQLModel)
avec migrations (Alembic) et validation stricte des données (Pydantic). L’objectif est d’avoir
un système centralisé capable de :
    - Gérer l’ensemble des utilisateurs de la plateforme (apprenants, formateurs, staff pédagogique, administrateurs).
    - Suivre les sessions de formation (planning, salle, formateur, capacité).
    - Enregistrer les inscriptions des apprenants aux sessions et leur historique d’avancement.
Assurer la qualité des données à l’insertion (emails valides, dates cohérentes, plage d’âge, unicité des comptes, etc...).
    - Faire évoluer le schéma au fil des besoins (ajout de nouveaux rôles, champs, etc.)
sans interrompre l’exploitation
  
- **Objectifs** :
  - Concevoir le schéma relationnel (en SQLModel/SQLAlchemy) pour représenter :
    - Les utilisateurs de la plateforme : Apprenant, Formateur, StaffPédagogique, Admin.
    - Les salles, leurs capacités et leurs équipements.
    - Les sessions (cours ou ateliers) planifiées dans ces salles, avec leur formateur, leur date/heure, leur statut, leurs prérequis éventuels et leur capacité.
    - Les inscriptions des apprenants aux sessions et leur historique de présence.
  - Implémenter la validation des données à l’entrée (création/modification) à l’aide de Pydantic :
    - Vérifier le format des emails, la cohérence des dates (date_debut < date_fin), l’âge minimal des apprenants (≥ 16 ans), les rôles autorisés, etc.
    - S’assurer qu’un apprenant ne puisse pas s’inscrire à deux sessions qui se chevauchent ou dépasser la capacité maximale de la salle.
  - Mettre en place Alembic pour gérer les migrations successives du schéma :
    - Création initiale des tables.
    - Ajout d’un champ « statut_session » (ouverte/fermée).
    - Refonte de la table « Salle » pour y inclure un champ JSON d’équipements.
    - Évolution des rôles (par exemple, ajout d’un rôle « SuperAdmin »).
- **Équipe (trinôme)** :
  - Hurblain Loïc
  - Bellot Clovis
  - Vandenabeele Alex

## 2. Stack technique

| Domaine | Outil |
|---|---|
| ORM | SQLModel / SQLAlchemy |
| Validation | Pydantic |
| Migrations | Alembic |
| Base de données | <!-- SQLite / PostgreSQL / autre --> |
| Interface (bonus) | <!-- Streamlit / Tkinter / Flask --> |

## 3. Installation

```bash
# 1. Cloner le dépôt
git clone <url-du-depot>
cd CF-Tech

# 2. (Recommandé) créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

## 4. Structure du projet

```
CF-Tech/
├── main.py
├── config
├── interface/
│   ├──
│   └──
├── fichier.py/
│   ├──
│   └──
├── graph/
│   ├──
│   └──
└── requirements.txt
```

## 5. Modèle de données

- **Diagramme** (UML / Merise) : <!-- lien ou image -->
- **Choix d'architecture** (tables séparées ou héritage `UserBase`) : <!-- justification -->
- **Entités** :
  - Utilisateurs : Apprenant, Formateur, StaffPédagogique, Admin
  - Salle
  - Session
  - Inscription
- **Relations et contraintes clés** : <!-- FK, unicités, index -->

## 6. Validations métier

- Pydantic : <!-- email, dates (début < fin), âge ≥ 16, téléphone, taux horaire -->
- Règles métier : <!-- pas de chevauchement salle/formateur/apprenant, capacité max, session OPEN -->
- Fonctions utilitaires : `check_permission`, `is_salle_disponible` <!-- décrire -->
- Gestion des erreurs : <!-- exceptions custom -->

## 7. Migrations Alembic

| Révision | Description | Message / ID |
|---|---|---|
| v1 | Version 1 | <!-- --> |
| v2 | Version 2 | <!-- --> |
| v3 | Version 3 | <!-- --> |
| v4 | Version 4 | <!-- --> |

```bash
# commandes à compléter
alembic upgrade head
alembic downgrade -1
```

## 8. Application graphique (bonus)

- **Techno choisie** : <!-- -->
- **Fonctionnalités** : CRUD utilisateurs / sessions / inscriptions, dashboard de reporting
- **Lancement** : <!-- commande -->
- **Captures d'écran** : <!-- -->

## 9. Tests

<!-- scénarios testés : création utilisateur, conflit de sessions, inscription d'un mineur, migration d'une version à l'autre -->


## 10. Auteurs

<!-- noms, liens GitHub -->
