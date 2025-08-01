"""
Beispiele für die Verwendung des Dimetrics MCP Servers.
"""

# Beispiel 1: Stromvertrags-App erstellen
POWER_CONTRACT_APP = {
    "app_name": "Stromverträge Verwaltung",
    "app_description": "Verwaltung von Stromverträgen für Kunden",
    "tables": [
        {
            "name": "kunden",
            "description": "Kundenstammdaten",
            "attributes": [
                {"name": "vorname", "type": "input", "required": True},
                {"name": "nachname", "type": "input", "required": True},
                {"name": "email", "type": "input", "required": True},
                {"name": "telefon", "type": "input", "required": False},
                {"name": "adresse", "type": "input", "required": True},
                {"name": "kundennummer", "type": "input", "required": True},
                {"name": "status", "type": "dropdown", "required": True, "options": {
                    "choices": ["aktiv", "inaktiv", "gesperrt"]
                }}
            ]
        },
        {
            "name": "stromvertraege",
            "description": "Stromverträge der Kunden",
            "attributes": [
                {"name": "vertragsnummer", "type": "input", "required": True},
                {"name": "kunde_id", "type": "relation", "required": True, "options": {
                    "related_table": "kunden"
                }},
                {"name": "tarif", "type": "dropdown", "required": True, "options": {
                    "choices": ["Grundtarif", "Ökostrom", "Nachtstrom", "Gewerbe"]
                }},
                {"name": "verbrauch_jahr", "type": "number", "required": True},
                {"name": "preis_kwh", "type": "number", "required": True},
                {"name": "grundpreis_monat", "type": "number", "required": True},
                {"name": "vertragsbeginn", "type": "date", "required": True},
                {"name": "vertragsende", "type": "date", "required": False},
                {"name": "kuendigungsfrist", "type": "number", "required": True},
                {"name": "automatische_verlaengerung", "type": "boolean", "required": True},
                {"name": "zaehlerstand_start", "type": "number", "required": False},
                {"name": "zaehlerstand_aktuell", "type": "number", "required": False},
                {"name": "status", "type": "dropdown", "required": True, "options": {
                    "choices": ["aktiv", "gekündigt", "beendet"]
                }}
            ]
        },
        {
            "name": "rechnungen",
            "description": "Stromrechnungen",
            "attributes": [
                {"name": "rechnungsnummer", "type": "input", "required": True},
                {"name": "vertrag_id", "type": "relation", "required": True, "options": {
                    "related_table": "stromvertraege"
                }},
                {"name": "abrechnungsperiode_von", "type": "date", "required": True},
                {"name": "abrechnungsperiode_bis", "type": "date", "required": True},
                {"name": "verbrauch_kwh", "type": "number", "required": True},
                {"name": "betrag_netto", "type": "number", "required": True},
                {"name": "betrag_brutto", "type": "number", "required": True},
                {"name": "rechnungsdatum", "type": "date", "required": True},
                {"name": "faelligkeitsdatum", "type": "date", "required": True},
                {"name": "bezahlt", "type": "boolean", "required": True},
                {"name": "bezahldatum", "type": "date", "required": False}
            ]
        }
    ]
}

# Beispiel 2: Einfache Todo-App
TODO_APP = {
    "app_name": "Todo Verwaltung",
    "app_description": "Einfache Todo-Liste",
    "tables": [
        {
            "name": "todos",
            "description": "Todo-Einträge",
            "attributes": [
                {"name": "titel", "type": "input", "required": True},
                {"name": "beschreibung", "type": "textarea", "required": False},
                {"name": "prioritaet", "type": "dropdown", "required": True, "options": {
                    "choices": ["niedrig", "mittel", "hoch"]
                }},
                {"name": "faelligkeitsdatum", "type": "date", "required": False},
                {"name": "erledigt", "type": "boolean", "required": True},
                {"name": "kategorie", "type": "dropdown", "required": False, "options": {
                    "choices": ["Arbeit", "Privat", "Einkaufen", "Gesundheit"]
                }}
            ]
        }
    ]
}

# Beispiel-Datensätze für Stromverträge
EXAMPLE_CUSTOMER_DATA = {
    "vorname": "Max",
    "nachname": "Mustermann",
    "email": "max.mustermann@email.com",
    "telefon": "+49 123 456789",
    "adresse": "Musterstraße 123, 12345 Musterstadt",
    "kundennummer": "K12345",
    "status": "aktiv"
}

EXAMPLE_CONTRACT_DATA = {
    "vertragsnummer": "V12345",
    "kunde_id": "1",  # Würde von der echten Kunden-ID ersetzt
    "tarif": "Ökostrom",
    "verbrauch_jahr": 3500,
    "preis_kwh": 0.32,
    "grundpreis_monat": 12.50,
    "vertragsbeginn": "2024-01-01",
    "vertragsende": "2025-12-31",
    "kuendigungsfrist": 3,
    "automatische_verlaengerung": True,
    "zaehlerstand_start": 45000,
    "zaehlerstand_aktuell": 47200,
    "status": "aktiv"
}

# Natürlichsprachliche Anweisungen (Beispiele)
NATURAL_LANGUAGE_EXAMPLES = [
    "Erstelle mir eine App zur Verwaltung von Stromverträgen für Kunden",
    "Füge eine neue Tabelle für Rechnungen hinzu",
    "Erstelle einen neuen Kunden: Max Mustermann, max.mustermann@email.com",
    "Liste alle aktiven Stromverträge auf",
    "Aktualisiere den Zählerstand für Vertrag V12345 auf 47500",
    "Zeige alle unbezahlten Rechnungen an",
    "Erstelle eine Rechnung für Vertrag V12345 für den Zeitraum Januar 2024"
]
