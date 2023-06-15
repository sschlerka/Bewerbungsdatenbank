from os.path import exists
db_vorhanden = exists("Bewerbungen.db")
import sqlite3
datenbank = sqlite3.connect("Bewerbungen.db")
cur = datenbank.cursor()
if db_vorhanden == False:
    with open("init-db.sql") as initfile:
        initfile = initfile.read()
        datenbank.executescript(initfile)
        datenbank.commit()
datenbank.close()
from datetime import datetime
import re



###### Funktionen ######

def anzeige_bewerbungen(x): # x: Wird von der filter-Option übergeben; 1 für alle Bewerbungen, 2 für nicht eingereichte
    datenbank = sqlite3.connect("Bewerbungen.db")
    cur = datenbank.cursor()
    if x == 1:
        cur.execute("SELECT * FROM anzeige_bewerbungen WHERE Status IS NOT 'Bewerbung nicht fertiggestellt'")
    elif x == 2:
        cur.execute("SELECT * FROM anzeige_bewerbungen WHERE Status IN ('Ausschreibung gespeichert', 'In Bearbeitung', 'Fertig, noch nicht abgeschickt')")
    bewerbungen = cur.fetchall()
    datenbank.close()
    #p.pprint(bewerbungen)
    bewerbungsliste = []
    for bewerbung in bewerbungen:
        if bewerbung[10] == 1:
            einladung = "Ja"
            einl_logik = True
        else:
            einladung = "Nein"
            einl_logik = False
        datum_fund = datetime.strptime(bewerbung[6], "%d.%m.%Y").date().__format__("%Y-%m-%d")
        frist = datetime.strptime(bewerbung[7], "%d.%m.%Y").date().__format__("%Y-%m-%d")
        if bewerbung[8] != None and re.fullmatch("\d{2}\.\d{2}\.\d{4}", bewerbung[8]):
            verschickt = datetime.strptime(bewerbung[8], "%d.%m.%Y").date().__format__("%Y-%m-%d")
        else:
            verschickt = ""
        if bewerbung[9] != None and re.fullmatch("\d{2}\.\d{2}\.\d{4}", bewerbung[9]):
            antwort = datetime.strptime(bewerbung[9], "%d.%m.%Y").date().__format__("%Y-%m-%d")
        else:
            antwort = ""
        if bewerbung[11] != None and re.fullmatch("\d{2}\.\d{2}\.\d{4}", bewerbung[11]):
            gespraech = datetime.strptime(bewerbung[11], "%d.%m.%Y").date().__format__("%Y-%m-%d")
        else:
            gespraech = ""
        eintrag = {"id": bewerbung[0], "status": bewerbung[1], "jobtyp": bewerbung[2], "titel": bewerbung[3], "arbeitgeber": bewerbung[4], "inst-typ": bewerbung[5], "datum-fund": datum_fund, "frist": frist, "verschickt": verschickt, "antwort": antwort, "einladung": einladung, "gespraech": gespraech, "status-id": bewerbung[12], "einl-logik": einl_logik}
        bewerbungsliste.append(eintrag)
    return bewerbungsliste



def get_status():
    datenbank = sqlite3.connect("Bewerbungen.db")
    cur = datenbank.cursor()
    cur.execute("SELECT * FROM Status")
    status = cur.fetchall()
    datenbank.close()
    statusliste = {}
    for item in status:
        statusliste[item[0]] = item[1]
    #p.pprint(statusliste)
    return statusliste

def get_jobtyp():
    datenbank = sqlite3.connect("Bewerbungen.db")
    cur = datenbank.cursor()
    cur.execute("SELECT * FROM Jobtypen")
    jobtypen = cur.fetchall()
    datenbank.close()
    jobtypliste = {}
    for item in jobtypen:
        jobtypliste[item[0]] = item[1]
    return jobtypliste

def get_insttyp():
    datenbank = sqlite3.connect("Bewerbungen.db")
    cur = datenbank.cursor()
    cur.execute("SELECT * FROM Institutionen")
    insttypen = cur.fetchall()
    datenbank.close()
    insttypliste = {}
    for item in insttypen:
        insttypliste[item[0]] = item[1]
    return insttypliste

def set_status(
        bewerbungen, # wird durch Auswahl aus der Liste übergeben
        status # wird durch die eingegebenen Daten übergeben
    ):
    #p.pprint(status)
    datenbank = sqlite3.connect("Bewerbungen.db")
    cur = datenbank.cursor()
    for bewerbung in bewerbungen:
        cur.execute("UPDATE Bewerbungen SET Status = ? WHERE ID = ?", (str(status["status-id"]), str(bewerbung["id"])))
        if status["frist"]:
            frist = datetime.strptime(status["frist"],"%Y-%m-%d").date().__format__("%d.%m.%Y")
            cur.execute("UPDATE Bewerbungen SET Frist = ? WHERE ID = ?",(str(frist), str(bewerbung["id"])))
        if status["bewerbungsdatum"]:
            bewerbungsdatum = datetime.strptime(status["bewerbungsdatum"],"%Y-%m-%d").date().__format__("%d.%m.%Y")
            #print(str(bewerbungsdatum))
            cur.execute("UPDATE Bewerbungen SET DatumVerschickt = ? WHERE ID = ?", (str(bewerbungsdatum), str(bewerbung["id"])))
        if status["antwort"]:
            antwort = datetime.strptime(status["antwort"],"%Y-%m-%d").date().__format__("%d.%m.%Y")
            cur.execute("UPDATE Bewerbungen SET DatumAntwort = ? WHERE ID = ?",(str(antwort), str(bewerbung["id"])))
        if status["gespraech"]:
            gespraech = datetime.strptime(status["antwort"],"%Y-%m-%d").date().__format__("%d.%m.%Y")
            cur.execute("UPDATE Bewerbungen SET DatumGespraech = ? WHERE ID = ?",(str(gespraech), str(bewerbung["id"])))
        if status["einladung"] == True:
            einladung = "1"
            cur.execute("UPDATE Bewerbungen SET Einladung = ? WHERE ID = ?", (einladung, str(bewerbung["id"])))
    datenbank.commit()
    datenbank.close()

def neue_bewerbung(
        daten
):
    datenbank = sqlite3.connect("Bewerbungen.db")
    cur = datenbank.cursor()
    frist = datetime.strptime(daten["frist"],"%Y-%m-%d").date().__format__("%d.%m.%Y")
    gefunden = datetime.strptime(daten["gefunden"],"%Y-%m-%d").date().__format__("%d.%m.%Y")
    #p.pprint(daten)
    cur.execute("INSERT INTO Bewerbungen (Arbeitgeber, DatumGefunden, Institutionstyp, Jobtyp, Status, Titel, Frist) VALUES (?, ?, ?, ?, ?, ?, ?)", (daten["arbeitgeber"], str(gefunden), daten["insttyp"], daten["jobtyp"], daten["status-id"], daten["titel"], str(frist)))
    datenbank.commit()
    datenbank.close()

