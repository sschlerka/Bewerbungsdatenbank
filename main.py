# Datenbankoperationen importieren
import db_funktionen

# Weitere Bibliotheken
import datetime
import re

# NiceGUI
from nicegui import ui

# Definition von Variablen
columns = [
    {"name": "id", "label": "ID", "field": "id", "align": "left", "required": True, "sortable": True},
    {"name": "status", "label": "Status", "field": "status", "align": "left", "style": "max-width: 300px", "headerStyle": "max-width: 300px"},
    {"name": "jobtyp", "label": "Jobtyp", "field": "jobtyp", "align": "left"},
    {"name": "titel", "label": "Stellentitel", "field": "titel", "align": "left"},
    {"name": "arbeitgeber", "label": "Arbeitgeber", "field": "arbeitgeber", "align": "left"},
    {"name": "inst-typ", "label": "Art des Arbeitgebers", "field": "inst-typ", "align": "left"},
    {"name": "datum-fund", "label": "Wann gefunden?", "field": "datum-fund", "align": "left", "sortable": True},
    {"name": "frist", "label": "Frist", "field": "frist", "align": "left", "sortable": True},
    {"name": "verschickt", "label": "Bewerbungsdatum", "field": "verschickt", "align": "left", "sortable": True},
    {"name": "antwort", "label": "Datum der Antwort", "field": "antwort", "align": "left", "sortable": True,},
    {"name": "einladung", "label": "Einladung bekommen?", "field": "einladung", "align": "left"},
    {"name": "gespraech", "label": "Datum Vorstellungsgespräch", "field": "gespraech", "align": "left", "sortable": True},
    {"name": "status-id", "label": "Status-ID (sollte unsichtbar sein)", "field": "status-id"},
    {"name": "einl-logik", "label": "Einladung (Logikwert; sollte unsichtbar sein)", "field": "einl-logik"}
]
visible_columns = {column["name"] for column in columns}
statusliste = db_funktionen.get_status()
jobtypliste = db_funktionen.get_jobtyp()
insttypliste = db_funktionen.get_insttyp()
status = {"status-id": 1, "einladung": False, "bewerbungsdatum": "", "frist": "", "antwort": "", "gespraech": ""}
default_status = {"status-id": 1}
neue_bewerbung = {"gefunden": datetime.date.today().__format__("%Y-%m-%d"), "status-id": 1, "arbeitgeber": "", "frist": "", "insttyp": 0, "jobtyp": 0, "titel": ""}


# Definition von Funktionen, die direkt in der GUI gebraucht werden
def reload_table():
    rows = db_funktionen.anzeige_bewerbungen(1)
    table.remove_rows(*table.rows)
    for row in rows:
        table.add_rows(row)
    table.update()

def filtern(x): # x: Value des Toggles im Tabellen-Header
    rows = db_funktionen.anzeige_bewerbungen(x)
    table.remove_rows(*table.rows)
    for row in rows:
        table.add_rows(row)
    table.update()
def statusupdate_klick(bewerbung,status_dict):
    #print(status_dict)
    if re.fullmatch("\d{4}-\d{2}-\d{2}", status_dict["bewerbungsdatum"]) == None and status_dict["bewerbungsdatum"] != "":
        ui.notify("Es wurde kein gültiges Bewerbungsdatum eingegeben! Änderung nicht geschrieben.")
        return
    db_funktionen.set_status(bewerbung, status_dict)
    reload_table()

def toggle(column: dict, visible: bool) -> None:
    if visible:
        visible_columns.add(column['name'])
    else:
        visible_columns.remove(column['name'])
    table._props['columns'] = [column for column in columns if column['name'] in visible_columns]
    table.update()

def status_dropdown_update(x,y):
    if len(y) > 0:
        x.set_value(y[0]["status-id"])
    else:
        print("Nothing to do...")

def neueintrag_klick(daten):
    if daten["arbeitgeber"] == "":
        ui.notify("Es wurde kein Arbeitgeber eingegeben! Änderung nicht geschrieben.")
        return
    if daten["frist"] == "" or re.fullmatch("\d{4}-\d{2}-\d{2}",daten["frist"]) == None:
        ui.notify("Es wurde keine gültige Frist eingegeben! Änderung nicht geschrieben.")
        return
    if daten["insttyp"] == "":
        ui.notify("Es wurde kein Institutionstyp angegeben! Änderung nicht geschrieben.")
        return
    if daten["jobtyp"] == "":
        ui.notify("Es wurde kein Jobtyp angegeben! Änderung nicht geschrieben.")
        return
    if daten["titel"] == "":
        ui.notify("Es wurde kein Jobtitel eingegeben! Änderung nicht geschrieben.")
        return
    abgleichliste = db_funktionen.anzeige_bewerbungen(1)
    for bewerbung in abgleichliste:
        if daten["titel"] == bewerbung["titel"] and daten["arbeitgeber"] == bewerbung["arbeitgeber"] and bewerbung["frist"] == daten["frist"]:
            ui.notify("Diese Bewerbung ist schon im System! Kein neuer Eintrag erzeugt.")
            return
    db_funktionen.neue_bewerbung(daten)
    input_jobtitel.set_value("")
    neu_jobtyp_dropdown.set_value(0)
    input_arbeitgeber.set_value("")
    neu_insttyp_dropdown.set_value(0)
    new_status_dropdown.set_value(1)
    found_date.set_value("")
    neu_frist_date.set_value("")
    neue_bewerbung.update({"gefunden": datetime.date.today().__format__("%Y-%m-%d"), "status-id": 1, "arbeitgeber": "", "frist": "", "insttyp": 0, "jobtyp": 0, "titel": ""})
    reload_table()




table = ui.table(columns=columns,rows=db_funktionen.anzeige_bewerbungen(1),row_key="id",title="Laufende Bewerbungen",pagination=5,selection="single").classes("w-full table-fixed border-collapse")
with table.add_slot('top-right'):
    with ui.input(placeholder='Suche…').props('type=search').bind_value(table, 'filter').add_slot('append'):
        ui.icon('search')
with table.add_slot('top-left'):
    with ui.row():
        with ui.button(on_click=lambda: menu_tabelle.open()).props('icon=menu'):
            with ui.menu() as menu_tabelle, ui.column().classes('gap-0 p-2'):
                for column in columns:
                    if column["name"] not in ["id", "status", "titel", "arbeitgeber"] and column["name"] not in ["einladung", "gespraech", "jobtyp", "inst-typ", "antwort", "status-id", "einl-logik"]:
                        ui.switch(column['label'], value=True, on_change=lambda e, column=column: toggle(column, e.value))
                    elif column["name"] in ["einladung", "gespraech", "jobtyp", "inst-typ", "antwort"] and column["name"] != "status-id" and column["name"] != "einl-logik":
                        ui.switch(column['label'], value=False, on_change=lambda e, column=column: toggle(column, e.value))
                        toggle(column, False)
                    elif column["name"] == "status-id" or column["name"] == "einl-logik":
                        toggle(column, False)
        ui.button("", on_click=lambda: reload_table()).props("icon=refresh")
        ui.toggle({1: "Alle", 2: "Nur Uneingereichte"}, value=1, on_change=lambda e: filtern(e.value))
auswahl=table.selected
#ui.label().bind_text_from(table, 'selected', lambda val: f'Current selection: {auswahl}')
with ui.tabs() as tabs:
    ui.tab("Bewerbungen updaten", icon="edit_document")
    ui.tab("Neue Bewerbung eintragen", icon="add_circle")

with ui.tab_panels(tabs, value="Bewerbungen updaten"):
    with ui.tab_panel("Bewerbungen updaten"):
        with ui.column():
            with ui.row().classes("place-items-baseline"):
                status_dropdown = ui.select(db_funktionen.get_status(), value=1, with_input=True, label="Status der Bewerbung", on_change=lambda e: status.update({"status-id": e.value})).classes("w-80")
                table.on("selection", lambda: (status_dropdown.set_value(auswahl[0]["status-id"]) if len(auswahl) > 0 else None))
                einladung_checkbox = ui.checkbox("Einladung zum Gespräch", on_change=lambda e: status.update({"einladung": e.value}))
                table.on("selection", lambda: (einladung_checkbox.set_value(auswahl[0]["einl-logik"]) if len(auswahl) > 0 else None))
            with ui.row().classes("place-items-baseline"):
            #ui.button("Print ID", on_click=lambda: ui.notify(auswahl[0][0]["titel"]))
                with ui.input('Frist', placeholder="JJJJ-MM-DD", on_change=lambda e: status.update({"frist": e.value}), validation={"Bitte ein Datum im Format JJJJ-MM-DD eingeben!": lambda value: re.fullmatch("\d{4}-\d{2}-\d{2}", value) or re.fullmatch("", value)}) as frist_date:
                    with frist_date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', lambda: menu_frist.open()).classes('cursor-pointer')
                    with ui.menu() as menu_frist:
                        ui.date(value=datetime.date.today()).bind_value(frist_date)
                    table.on("selection", lambda: (frist_date.set_value(auswahl[0]["frist"]) if len(auswahl) > 0 else None))
                with ui.input('Bewerbungsdatum', placeholder="JJJJ-MM-DD", on_change=lambda e: status.update({"bewerbungsdatum": e.value}), validation={"Bitte ein Datum im Format JJJJ-MM-DD eingeben!": lambda value: re.fullmatch("\d{4}-\d{2}-\d{2}", value) or re.fullmatch("", value)}) as appl_date:
                    with appl_date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', lambda: menu_bewerbungsdatum.open()).classes('cursor-pointer')
                    with ui.menu() as menu_bewerbungsdatum:
                        ui.date(value=datetime.date.today()).bind_value(appl_date)
                    table.on("selection", lambda: (appl_date.set_value(auswahl[0]["verschickt"]) if len(auswahl) > 0 else None))
                #ui.label().bind_text_from(appl_date, "value", lambda val: f"Datum: {appl_date.value}")
            with ui.row().classes("place-items-baseline"):
                with ui.input('Datum der Antwort', placeholder="JJJJ-MM-DD", on_change=lambda e: status.update({"antwort": e.value}), validation={"Bitte ein Datum im Format JJJJ-MM-DD eingeben!": lambda value: re.fullmatch("\d{4}-\d{2}-\d{2}", value) or re.fullmatch("", value)}) as reply_date:
                    with reply_date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', lambda: menu_antwort.open()).classes('cursor-pointer')
                    with ui.menu() as menu_antwort:
                        ui.date(value=datetime.date.today()).bind_value(reply_date)
                    table.on("selection", lambda: (reply_date.set_value(auswahl[0]["antwort"]) if len(auswahl) > 0 else None))
                with ui.input('Datum des Interviews', placeholder="JJJJ-MM-DD", on_change=lambda e: status.update({"gespraech": e.value}), validation={"Bitte ein Datum im Format JJJJ-MM-DD eingeben!": lambda value: re.fullmatch("\d{4}-\d{2}-\d{2}", value) or re.fullmatch("", value)}) as gespraech_date:
                    with gespraech_date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', lambda: menu_gespraech.open()).classes('cursor-pointer')
                    with ui.menu() as menu_gespraech:
                        ui.date(value=datetime.date.today()).bind_value(gespraech_date)
                    table.on("selection",lambda: (reply_date.set_value(auswahl[0]["antwort"]) if len(auswahl) > 0 else None))
            ui.button("Status updaten", on_click=lambda: statusupdate_klick(auswahl, status))
    with ui.tab_panel("Neue Bewerbung eintragen"):
        with ui.column():
            with ui.row():
                input_jobtitel = ui.input("Jobtitel", placeholder="Hier den Jobtitel eintragen", on_change=lambda e: neue_bewerbung.update({"titel": e.value})).classes("w-96")
                neu_jobtyp_dropdown = ui.select(db_funktionen.get_jobtyp(), with_input=True, label="Jobtyp", on_change=lambda e: neue_bewerbung.update({"jobtyp": e.value})).classes("w-64")
            with ui.row():
                input_arbeitgeber = ui.input("Arbeitgeber", placeholder="Hier den Namen des Arbeitgebers eintragen", on_change=lambda e: neue_bewerbung.update({"arbeitgeber": e.value})).classes("w-96")
                neu_insttyp_dropdown = ui.select(db_funktionen.get_insttyp(), with_input=True,label="Typ des Arbeitgebers", on_change=lambda e: neue_bewerbung.update({"insttyp": e.value})).classes("w-64")
            with ui.row():
                new_status_dropdown = ui.select(db_funktionen.get_status(), value=1, with_input=True,label="Status der Bewerbung",on_change=lambda e: neue_bewerbung.update({"status-id": e.value})).classes("w-96")
                with ui.input('Wann gefunden?', value=datetime.date.today(), on_change=lambda e: neue_bewerbung.update({"gefunden": e.value}), validation={"Bitte ein Datum im Format JJJJ-MM-DD eingeben!": lambda value: re.fullmatch("\d{4}-\d{2}-\d{2}", value) or re.fullmatch("", value)}).classes("w-32") as found_date:
                    with found_date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', lambda: menu_found.open()).classes('cursor-pointer')
                    with ui.menu() as menu_found:
                        ui.date(value=datetime.date.today()).bind_value(found_date)
                with ui.input('Bewerbungsfrist', value=datetime.date.today(), on_change=lambda e: neue_bewerbung.update({"frist": e.value}), validation={"Bitte ein Datum im Format JJJJ-MM-DD eingeben!": lambda value: re.fullmatch("\d{4}-\d{2}-\d{2}", value) or re.fullmatch("", value)}).classes("w-32") as neu_frist_date:
                    with neu_frist_date.add_slot('append'):
                        ui.icon('edit_calendar').on('click', lambda: menu_frist.open()).classes('cursor-pointer')
                    with ui.menu() as menu_frist:
                        ui.date(value=datetime.date.today()).bind_value(neu_frist_date)
            eintrag_button = ui.button("Bewerbung eintragen", on_click=lambda: neueintrag_klick(neue_bewerbung))




ui.run(host="127.0.0.1", title="Bewerbungsdatenbank",native=True,window_size=(1920, 1080))