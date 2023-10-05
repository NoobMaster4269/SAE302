BEGIN TRANSACTION;


DROP TABLE IF EXISTS Promotion;

CREATE TABLE Promotion
  (idPromo	INTEGER	PRIMARY KEY AUTOINCREMENT,
   NomPromo	TEXT	NOT NULL
  );

INSERT INTO Pormotion VALUES('0','rt1');


DROP TABLE IF EXISTS Etudiant;

CREATE TABLE Etudiant
  (idEtud	INTEGER	PRIMARY KEY AUTOINCREMENT,
   Prenom TEXT NOT NULL,
   Nom	TEXT	NOT NULL,
   NomPromo TEXT    NOT NULL,
   FOREIGN KEY (NomPromo) REFERENCES Promotion (NomPromo)
   FOREIGN KEY (idPromo) REFERENCES Promotion (idPromo)
  );

INSERT INTO Etudiant VALUES('0', 'Noah', 'Claudel--Ruiellet', 'rt1');


DROP TABLE IF EXISTS Notes;

CREATE TABLE Notes
  (idNotes	INTEGER	PRIMARY KEY,
   idPromo  INTEGER NOT NULL,
   NomPromo INTEGER NOT NULL,
   Nom  INTEGER NOT NULL,
   Prenomom  INTEGER NOT NULL,
   Notes	  INTEGER NULL,
   Coef	    INTEGER NOT NULL,
   FOREIGN KEY (idPromo) REFERENCES Promotion (idPromo),
   FOREIGN KEY (NomPromo) REFERENCES Promotion (NomPromo),
   FOREIGN KEY (Nom) REFERENCES Etudiant (Nom),
   FOREIGN KEY (Prenom) REFERENCES Etudiant (Prenom)
  );

COMMIT;