BEGIN TRANSACTION;


DROP TABLE IF EXISTS rt1;

CREATE TABLE rt1
  (idrt1   INTEGER	PRIMARY KEY AUTOINCREMENT,
   NomPromo TEXT    NOT NULL,
   Prenom	TEXT	NOT NULL,
   Nom      TEXT    NOT NULL
  );

INSERT INTO rt1 VALUES('0',  'rt1', 'Noah', 'Claudel--Ruiellet');


DROP TABLE IF EXISTS Notesrt1;

CREATE TABLE Notesrt1
  (idNotert1	INTEGER	PRIMARY KEY,
   idrt1  INTEGER NOT NULL,
   NomPromo TEXT  NOT NULL,
   Nom  INTEGER NOT NULL,
   Prenom INTEGER NOT NULL,
   Note	  INTEGER NULL,
   Coef	    INTEGER NULL,
   FOREIGN KEY (idrt1) REFERENCES rt1 (idrt1),
      FOREIGN KEY (NomPromo) REFERENCES rt1 (NomPromo),
   FOREIGN KEY (Nom) REFERENCES rt1 (Nom),
   FOREIGN KEY (Prenom) REFERENCES rt1 (Prenom)
  );

COMMIT;