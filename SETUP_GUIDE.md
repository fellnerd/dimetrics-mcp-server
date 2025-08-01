# Dimetrics MCP Server - Detaillierte Anleitung

## Übersicht

Dieser MCP Server ermöglicht es GitHub Copilot, über natürliche Sprache mit der Dimetrics Web-API zu interagieren. Sie können Anweisungen wie "Erstelle mir eine App zur Verwaltung von Stromverträgen" geben, und der Server führt automatisch die entsprechenden API-Aufrufe durch.

## Funktionen

### 🏗️ Service (App) Management
- `create_app` - Erstellt neue Apps/Services
- `list_apps` - Listet alle verfügbaren Apps auf
- `delete_app` - Löscht Apps

### 📊 Tabellen Management  
- `create_table` - Erstellt neue Tabellen in Apps
- `list_tables` - Listet Tabellen auf
- Unterstützt dynamische Tabellenstrukturen

### 🔧 Attribut Management
- `create_attribute` - Definiert Spalten/Felder in Tabellen
- `list_attributes` - Zeigt Tabellenstruktur an
- Unterstützte Typen:
  - `input` - Texteingabe
  - `textarea` - Mehrzeiliger Text
  - `dropdown` - Auswahlmenü
  - `boolean` - Ja/Nein Checkbox
  - `number` - Zahlen
  - `date` - Datum
  - `relation` - Verknüpfung zu anderen Tabellen

### 💾 Daten Management (CRUD)
- `create_record` - Neue Datensätze anlegen
- `list_records` - Datensätze anzeigen
- `update_record` - Datensätze bearbeiten
- `delete_record` - Datensätze löschen

### 🚀 High-Level Tools
- `create_complete_app` - Erstellt komplette Apps mit Tabellen und Attributen in einem Zug

## Installation

### 1. Abhängigkeiten installieren

```bash
# Automatische Installation
./install.sh

# Oder manuell:
pip install -r requirements.txt
```

### 2. API-Zugangsdaten konfigurieren

```bash
# .env Datei erstellen
cp .env.example .env

# Bearbeiten Sie .env mit Ihren Dimetrics-Zugangsdaten:
# Entweder API-Key:
DIMETRICS_API_KEY=ihr_api_schluessel

# Oder Session-Cookie:
DIMETRICS_SESSION_COOKIE=ihr_session_cookie
```

### 3. MCP Client konfigurieren

Fügen Sie folgende Konfiguration zu Ihrer MCP-Client-Konfiguration hinzu (z.B. in VS Code):

```json
{
  "mcpServers": {
    "dimetrics": {
      "command": "python",
      "args": ["-m", "dimetrics_mcp_server"],
      "cwd": "/home/user/source/mcp-server",
      "env": {
        "DIMETRICS_API_URL": "https://app.dimetrics.io/api",
        "DIMETRICS_API_KEY": "ihr_api_schluessel"
      }
    }
  }
}
```

## Verwendung

### Server starten

```bash
python -m dimetrics_mcp_server
```

### Beispiel-Anweisungen für GitHub Copilot

```
"Erstelle mir eine App zur Verwaltung von Stromverträgen für Kunden"

"Füge eine Tabelle für Kundendaten hinzu mit Feldern für Name, Email und Telefon"

"Erstelle einen neuen Kunden: Max Mustermann, max.mustermann@email.com"

"Liste alle aktiven Stromverträge auf"

"Aktualisiere den Zählerstand für Vertrag V12345"
```

## API-Endpunkte (Dimetrics)

Der MCP Server geht von folgender API-Struktur aus (ähnlich Directus CMS):

### Services (Apps)
- `GET /services` - Liste Services
- `POST /services` - Erstelle Service
- `GET /services/{id}` - Service Details
- `PUT /services/{id}` - Service aktualisieren
- `DELETE /services/{id}` - Service löschen

### Tabellen
- `GET /tables` - Liste Tabellen
- `POST /tables` - Erstelle Tabelle
- `GET /tables/{id}` - Tabellen Details
- `PUT /tables/{id}` - Tabelle aktualisieren
- `DELETE /tables/{id}` - Tabelle löschen

### Attribute
- `GET /tables/{table_id}/attributes` - Liste Attribute
- `POST /tables/{table_id}/attributes` - Erstelle Attribut
- `PUT /tables/{table_id}/attributes/{id}` - Attribut aktualisieren
- `DELETE /tables/{table_id}/attributes/{id}` - Attribut löschen

### Daten (CRUD)
- `GET /tables/{table_id}/records` - Liste Datensätze
- `POST /tables/{table_id}/records` - Erstelle Datensatz
- `GET /tables/{table_id}/records/{id}` - Datensatz Details
- `PUT /tables/{table_id}/records/{id}` - Datensatz aktualisieren
- `DELETE /tables/{table_id}/records/{id}` - Datensatz löschen

## Troubleshooting

### Häufige Probleme

1. **Authentifizierung fehlgeschlagen**
   - Prüfen Sie Ihre API-Zugangsdaten in der .env Datei
   - Stellen Sie sicher, dass die API-URL korrekt ist

2. **MCP Server startet nicht**
   - Prüfen Sie ob alle Abhängigkeiten installiert sind: `pip install -r requirements.txt`
   - Prüfen Sie die Logs für detaillierte Fehlermeldungen

3. **Tools werden nicht erkannt**
   - Stellen Sie sicher, dass der MCP Client korrekt konfiguriert ist
   - Prüfen Sie die Pfade in der MCP-Konfiguration

### Debug-Modus

Aktivieren Sie Debug-Logs in der .env:

```
DEBUG=true
```

### Tests ausführen

```bash
python test_server.py
```

## Anpassungen

### Neue Tools hinzufügen

Bearbeiten Sie `dimetrics_mcp_server/tools.py` und fügen Sie neue `@server.call_tool()` Funktionen hinzu.

### API-Endpunkte anpassen

Bearbeiten Sie `dimetrics_mcp_server/api_client.py` um die API-Aufrufe an Ihre spezifische Dimetrics-Installation anzupassen.

### Neue Attributtypen

Erweitern Sie die Attribut-Erstellung in den Tools um neue Datentypen, die Ihre Dimetrics-API unterstützt.

## Beispiel: Komplette Stromvertrags-App

```python
# Wird automatisch vom create_complete_app Tool verwendet
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
                # ... weitere Attribute
            ]
        },
        # ... weitere Tabellen
    ]
}
```

## Support

Bei Problemen oder Fragen:

1. Prüfen Sie die Logs des MCP Servers
2. Testen Sie die API-Verbindung direkt mit curl oder einem API-Client
3. Prüfen Sie die Dimetrics-API-Dokumentation für eventuelle Änderungen
4. Stellen Sie sicher, dass Ihre Dimetrics-Installation die erwarteten Endpunkte bereitstellt
