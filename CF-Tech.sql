CREATE TABLE Utilisateur(
   id INT NOT NULL AUTO_INCREMENT,
   nom VARCHAR(50) NOT NULL,
   prenom VARCHAR(50) NOT NULL,
   email VARCHAR(100) NOT NULL,
   date_creation DATE,
   est_actif LOGICAL,
   PRIMARY KEY(id),
   UNIQUE(email)
);

CREATE TABLE Salle(
   id INT NOT NULL AUTO_INCREMENT,
   nom VARCHAR(50) NOT NULL,
   capacite INT NOT NULL CHECK(capacite > 0),
   localisation VARCHAR(255),
   equipements VARCHAR(50),
   PRIMARY KEY(id),
   UNIQUE(nom)
);

CREATE TABLE Equipement(
   id INT NOT NULL AUTO_INCREMENT,
   nom VARCHAR(100) NOT NULL,
   description VARCHAR(255),
   PRIMARY KEY(id)
);

CREATE TABLE Apprenant(
   id INT NOT NULL AUTO_INCREMENT,
   poste VARCHAR(50) NOT NULL,
   date_naissance DATE NOT NULL CHECK(date_naissance >= 16),
   niveau_etude VARCHAR(50),
   telephone CHAR(10),
   date_inscription_plateforme DATETIME NOT NULL,
   certification_obtenue VARCHAR(100),
   id_utilisateur INT NOT NULL AUTO_INCREMENT NOT NULL,
   PRIMARY KEY(id),
   UNIQUE(id_utilisateur),
   UNIQUE(poste),
   FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id)
);

CREATE TABLE Formateur(
   id INT NOT NULL AUTO_INCREMENT,
   specialite VARCHAR(50) NOT NULL,
   date_embauche DATE NOT NULL -- (<= date du jour).,
   taux_horaire DECIMAL(10,2) NOT NULL CHECK(taux_horaire >= 0),
   bio VARCHAR(255),
   id_utilisateur INT NOT NULL AUTO_INCREMENT NOT NULL,
   PRIMARY KEY(id),
   UNIQUE(id_utilisateur),
   UNIQUE(specialite),
   FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id)
);

CREATE TABLE PersonnelPedagogique(
   id INT NOT NULL AUTO_INCREMENT,
   poste ENUM (ex. 'Responsable pédagogique', 'Chargée de Projet', 'Tuteur', 'Intervenant') NOT NULL,
   date_prise_fonction DATE NOT NULL,
   responsabilites VARCHAR(50) --JSON,
   id_utilisateur INT NOT NULL AUTO_INCREMENT NOT NULL,
   PRIMARY KEY(id),
   UNIQUE(id_utilisateur),
   FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id)
);

CREATE TABLE Admin(
   id INT NOT NULL AUTO_INCREMENT,
   niveau_acces ENUM ('SUPERADMIN', 'ADMIN') NOT NULL,
   date_promotion DATE NOT NULL,
   id_utilisateur INT NOT NULL AUTO_INCREMENT NOT NULL,
   PRIMARY KEY(id),
   UNIQUE(id_utilisateur),
   FOREIGN KEY(id_utilisateur) REFERENCES Utilisateur(id)
);

CREATE TABLE Session(
   id INT NOT NULL AUTO_INCREMENT,
   titre VARCHAR(100) NOT NULL,
   description VARCHAR(255),
   date_debut DATETIME NOT NULL,
   date_fin DATETIME NOT NULL CHECK(date_debut < date_fin),
   capacite_max VARCHAR(50) NOT NULL /*CHECK(<=salle.capacite)*/,
   statut ENUM ('OUVERTE', 'FERMEE', 'ARCHIVEE') DEFAULT 'OUVERTE' NOT NULL,
   id_formateur INT NOT NULL AUTO_INCREMENT NOT NULL,
   id_salle INT NOT NULL AUTO_INCREMENT NOT NULL,
   PRIMARY KEY(id),
   FOREIGN KEY(id_formateur) REFERENCES Formateur(id),
   FOREIGN KEY(id_salle) REFERENCES Salle(id)
);

CREATE TABLE Inscription(
   id INT NOT NULL AUTO_INCREMENT,
   date_inscription DATETIME NOT NULL,
   statut_inscription ENUM (ENREGISTRE, 'DESINSCRIT', 'EN_ATTENTE') NOT NULL,
   presence LOGICAL,
   id_apprenant INT NOT NULL AUTO_INCREMENT NOT NULL,
   id_session INT NOT NULL AUTO_INCREMENT NOT NULL,
   PRIMARY KEY(id),
   FOREIGN KEY(id_apprenant) REFERENCES Apprenant(id),
   FOREIGN KEY(id_session) REFERENCES Session(id)
);

CREATE TABLE Est_équipé(
   id_salle INT NOT NULL AUTO_INCREMENT,
   id_equipement INT NOT NULL AUTO_INCREMENT,
   quantite INT NOT NULL,
   information VARCHAR(255),
   PRIMARY KEY(id_salle, id_equipement),
   FOREIGN KEY(id_salle) REFERENCES Salle(id),
   FOREIGN KEY(id_equipement) REFERENCES Equipement(id)
);
