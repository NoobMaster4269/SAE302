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
   NomPrenom	TEXT	NOT NULL,
   NomPromo TEXT    NOT NULL,
   FOREIGN KEY (NomPromo) REFERENCES Prpmotion (NomPromo)
  );

INSERT INTO Etudiant VALUES('0','Noah Claudel--Ruiellet', 'rt1');


DROP TABLE IF EXISTS Notert1;

CREATE TABLE Notert1
  (idNotes	INTEGER	PRIMARY KEY,
   idEtud   INTEGER
   Notes	INTEGER NULL,
   Coef	INTEGER NOT NULL,
   FOREIGN KEY (idEtud) REFERENCES Etudiant (idEtud)

  );

COMMIT;