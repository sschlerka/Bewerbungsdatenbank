CREATE TABLE IF NOT EXISTS "Institutionen" (
	"ID"	INTEGER,
	"Institutionstyp"	TEXT,
	PRIMARY KEY("ID" AUTOINCREMENT),
	UNIQUE(Institutionstyp)
);
INSERT OR IGNORE INTO Institutionen (Institutionstyp) VALUES 
    ("Universität (D)"), 
    ("Universität (UK)"), 
    ("Universität (NL)"), 
    ("Universität (sonstiges Ausland)"), 
    ("Öffentlicher Dienst (kommunal)"), 
    ("Öffentlicher Dienst (Land)"), 
    ("Öffentlicher Dienst (Bund)"), 
    ("Privatwirtschaft");
CREATE TABLE IF NOT EXISTS "Jobtypen" (
    "ID" INTEGER,
    "Jobtyp" TEXT,
    PRIMARY KEY("ID" AUTOINCREMENT),
    UNIQUE(Jobtyp)
);
INSERT OR IGNORE INTO Jobtypen (Jobtyp) VALUES 
    ("Forschung"), 
    ("Verwaltung"), 
    ("Evaluation"), 
    ("Referent"), 
    ("Lektor"), 
    ("Sonstiges");
CREATE TABLE IF NOT EXISTS "Status" (
    "ID" INTEGER,
    "Status" TEXT,
    PRIMARY KEY("ID" AUTOINCREMENT),
    UNIQUE(Status)
);
INSERT OR IGNORE INTO Status (Status) VALUES 
    ("Ausschreibung gespeichert"), 
    ("In Bearbeitung"), 
    ("Fertig, noch nicht abgeschickt"), 
    ("Abgeschickt"), 
    ("Direkte Absage"), 
    ("Einladung zum Vorstellungsgespräch"), 
    ("Entscheidung steht aus"), 
    ("Absage nach Vorstellungsgespräch"), 
    ("Zusage"),
    ("Bewerbung nicht fertiggestellt");
CREATE TABLE IF NOT EXISTS "Bewerbungen" (
    "ID" INTEGER,
    "Status" INTEGER,
    "Jobtyp" INTEGER,
    "Titel" TEXT,
    "Arbeitgeber"	INTEGER,
    "Institutionstyp" INTEGER,
    "DatumGefunden" TEXT,
    "Frist" TEXT,
    "DatumVerschickt" TEXT,
    "DatumAntwort" TEXT,
    "Einladung" INTEGER,
    "DatumGespraech" TEXT,
    "Aktiv"	INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY ("Status") REFERENCES "Status"("ID"),
    FOREIGN KEY ("Institutionstyp") REFERENCES "Institutionen"("ID"),
    FOREIGN KEY ("Jobtyp") REFERENCES "Jobtypen"("ID"),
    PRIMARY KEY("ID" AUTOINCREMENT)
);
CREATE VIEW IF NOT EXISTS anzeige_bewerbungen
AS
SELECT
    b.ID,
    s.Status,
    j.Jobtyp,
    b.Titel,
    b.Arbeitgeber,
    i.Institutionstyp,
    b.DatumGefunden,
    b.Frist,
    b.DatumVerschickt,
    b.DatumAntwort,
    b.Einladung,
    b.DatumGespraech
FROM
    Bewerbungen b
INNER JOIN Institutionen i ON b.Institutionstyp = i.ID
INNER JOIN Status s ON b.Status = s.ID
INNER JOIN Jobtypen j ON b.Jobtyp = j.ID
