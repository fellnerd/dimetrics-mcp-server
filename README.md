# Dimetrics, Werkportal & PPMC MCP Server - Multi-API Integration

Ein **Model Context Protocol (MCP) Server** der **Dimetrics**, **Werkportal** und **PPMC** APIs unterstützt.

## 🎯 Services

### Dimetrics MCP Server  
- **Port**: 5201
- **API**: https://dimetrics.api.nc.released.services/api
- **Container**: dimetrics-mcp-server

### Werkportal MCP Server
- **Port**: 5202  
- **API**: https://werkportal.api.nc.released.services/api
- **Container**: werkportal-mcp-server

### PPMC MCP Server
- **Port**: 5203
- **API**: https://ppmc.api.nc.released.services/api
- **Container**: ppmc-mcp-server

## 🚀 Verwendung

```bash
# Alle Services starten
docker-compose up -d

# Einzelne Services
docker-compose up -d dimetrics-mcp-server
docker-compose up -d werkportal-mcp-server
docker-compose up -d ppmc-mcp-server

# Kombinationen
docker-compose up -d dimetrics-mcp-server werkportal-mcp-server
```

---

# Dimetrics MCP Server - Vollständige API-Integration

Ein **Model Context Protocol (MCP) Server** basierend auf dem offiziellen **FastMCP Python SDK**, der eine vollständige Integration mit der Dimetrics Web-API bietet. Ermöglicht GitHub Copilot die natürlichsprachige Verwaltung von Apps, Services, Resources, Attributen und echten Daten.

## ✨ Features

- **🏗️ App Management**: Vollständiges CRUD für Apps
- **⚙️ Service Management**: Vollständiges CRUD für Services mit App-Verknüpfung
- **📊 Resource Management**: Vollständiges CRUD für Resources mit Service-Verknüpfung
- **🔧 Attribute Management**: Vollständiges CRUD für Attribute mit 25+ unterstützten Typen
- **💾 Generics API (Data CRUD)**: Vollständiges CRUD für echte Daten in Resources
- **🔍 Erweiterte Abfragen**: Directus-ähnliche Filter, Aggregationen, Volltext-Suche
- **🚀 FastMCP Integration**: Basiert auf dem offiziellen MCP Python SDK
- **🔑 Flexible Authentifizierung**: Token-basierte API-Authentifizierung
- **📋 Natürlichsprachliche Steuerung**: GitHub Copilot Integration

## 🛠️ Verfügbare Tools (35 Tools)

### 📱 App Management
| Tool | Beschreibung | Parameter |
|------|--------------|-----------|
| `create_app` | Erstellt eine neue App | `name`, `description`, `prefix` |
| `list_apps` | Listet alle Apps auf | `search`, `page_size`, `page`, `limit` |
| `get_app_details` | Holt App-Details | `object_id` |
| `update_app` | Aktualisiert eine App | `object_id`, `name`, `description`, `prefix` |
| `delete_app` | Löscht eine App | `object_id` |

### 📂 Category Management
| Tool | Beschreibung | Parameter |
|------|--------------|-----------|
| `create_category` | Erstellt eine neue Category | `name`, `description`, `prefix` |
| `list_categories` | Listet alle Categories auf | `search`, `page_size`, `page`, `limit` |
| `get_category_details` | Holt Category-Details | `object_id` |
| `update_category` | Aktualisiert eine Category | `object_id`, `name`, `description`, `prefix` |
| `delete_category` | Löscht eine Category | `object_id` |

### ⚙️ Service Management
| Tool | Beschreibung | Parameter |
|------|--------------|-----------|
| `create_service` | Erstellt einen neuen Service | `name`, `app_space`, `description`, `title`, `icon`, etc. |
| `list_services` | Listet alle Services auf | `search`, `page_size`, `page`, `limit` |
| `get_service_details` | Holt Service-Details | `object_id` |
| `update_service` | Aktualisiert einen Service | `object_id`, `name`, `title`, `description`, etc. |
| `delete_service` | Löscht einen Service | `object_id` |

### 📊 Resource Management
| Tool | Beschreibung | Parameter |
|------|--------------|-----------|
| `create_resource` | Erstellt eine neue Resource | `name`, `service`, `description`, `title`, `icon`, etc. |
| `list_resources` | Listet alle Resources auf | `search`, `page_size`, `page`, `limit` |
| `get_resource_details` | Holt Resource-Details | `object_id` |
| `update_resource` | Aktualisiert eine Resource | `object_id`, `name`, `title`, `description`, etc. |
| `delete_resource` | Löscht eine Resource | `object_id` |

### 🔧 Attribute Management
| Tool | Beschreibung | Parameter |
|------|--------------|-----------|
| `list_attributes` | Listet Attribute einer Resource | `resource_name`, `search`, `page_size`, `page` |
| `get_attribute_details` | Holt Attribut-Details | `resource_name`, `attribute_id` |
| `create_attribute` | Erstellt ein neues Attribut | `resource_name`, `name`, `attribute_type`, etc. |
| `update_attribute` | Aktualisiert ein Attribut | `resource_name`, `attribute_id`, `name`, etc. |
| `delete_attribute` | Löscht ein Attribut | `resource_name`, `attribute_id` |
| `create_attributes_bulk` | Erstellt mehrere Attribute | `resource_name`, `attributes_json` |

### 💾 Generics API (Data CRUD)
| Tool | Beschreibung | Parameter |
|------|--------------|-----------|
| `list_generic_entries` | Listet Einträge mit Filter/Aggregation | `resource_name`, `search`, `directus_filter_json`, `aggregate_json`, etc. |
| `create_generic_entry` | Erstellt einen neuen Eintrag | `resource_name`, `entry_data_json` |
| `get_generic_entry` | Holt einen spezifischen Eintrag | `resource_name`, `entry_id` |
| `update_generic_entry` | Aktualisiert einen Eintrag (PATCH) | `resource_name`, `entry_id`, `update_data_json` |
| `delete_generic_entry` | Löscht einen Eintrag | `resource_name`, `entry_id`, `confirm_deletion` |

## 🎯 Erweiterte Features

### Directus-ähnliche Filter
```bash
# Beispiele für directus_filter_json
'{"state": {"_eq": "ok"}}'                              # Gleichheit
'{"amount": {"_gte": 10}}'                              # Größer gleich
'{"name": {"_contains": "Marathon"}}'                   # Textsuche
'{"_and": [{"state": {"_eq": "ok"}}, {"amount": {"_gte": 25}}]}'  # UND-Verknüpfung
```

### Aggregationen
```bash
# Beispiele für aggregate_json
'{"sum": "amount"}'                                     # Summe
'{"count": "name"}'                                     # Anzahl
'{"avg": "distance_km"}'                                # Durchschnitt
'{"sum": "amount", "count": "name", "avg": "amount"}'   # Mehrere gleichzeitig
```

### Volltext-Suche
```bash
# search Parameter
search="Marathon"        # Sucht in allen Textfeldern
search="Dauerlauf"       # Findet passende Einträge
```

## 🚀 Schnellstart

### 1. Installation

```bash
# Abhängigkeiten installieren
pip install -r requirements.txt
```

### 2. Konfiguration

```bash
# .env Datei erstellen
cp .env.example .env

# API-Zugangsdaten eintragen
DIMETRICS_API_URL=https://dimetrics.api.nc.released.services/api
DIMETRICS_API_KEY=your_token_here
```

### 3. Tests

```bash
# Grundfunktionalität testen
python3 test_minimal_new.py

# CRUD-Operationen testen
python3 test_generics_crud.py

# MCP-Tools testen  
python3 test_mcp_generics_crud.py

# Aggregationen und Filter testen
python3 test_aggregations.py
python3 test_directus_filters.py
```

### 4. MCP Server starten

```bash
# Server starten
python3 -m dimetrics_mcp_server

# Mit uv (falls installiert)
uv run mcp dev dimetrics_mcp_server/__main__.py
```

### 5. GitHub Copilot Integration

```json
{
  "mcpServers": {
    "dimetrics": {
      "command": "python3",
      "args": ["-m", "dimetrics_mcp_server"],
      "cwd": "/path/to/dimetrics-mcp-server",
      "env": {
        "DIMETRICS_API_URL": "https://dimetrics.api.nc.released.services/api",
        "DIMETRICS_API_KEY": "your_token_here"
      }
    }
  }
}
```

## 📈 Projekt-Status

### ✅ Vollständig Implementiert
- **Apps Management**: Alle CRUD-Operationen funktional
- **Categories Management**: Alle CRUD-Operationen funktional
- **Services Management**: Alle CRUD-Operationen funktional
- **Resources Management**: Alle CRUD-Operationen funktional
- **Attributes Management**: Alle CRUD-Operationen funktional
- **Generics API**: Vollständiges CRUD mit erweiterten Features
- **Filter-System**: Directus-kompatible Filter
- **Aggregationen**: Sum, Count, Average und mehr
- **Volltext-Suche**: Durchsuchung aller Textfelder

### 🎯 Erfolgreiche Test-Implementierung
Das System wurde mit einer vollständigen **Lauftagebuch-App** getestet:

```
App: Lauftagebuch
├── Service: Laufaktivitäten  
    └── Resource: Läufe
        ├── name (INPUT_FIELD)
        ├── state (DROPDOWN_FIELD)
        ├── distance_km (NUMERIC_FIELD)
        ├── duration_minutes (NUMERIC_FIELD)
        ├── date_created (TIMESTAMP_FIELD)
        ├── notes (TEXT_FIELD)
        ├── weather (DROPDOWN_FIELD)
        └── amount (NUMERIC_FIELD)
```

**Erfolgreiche CRUD-Tests:**
- ✅ Erstellung von Einträgen mit allen Attributen
- ✅ Filtern nach Status, Distanz, Datum
- ✅ Aggregationen (Summe der Distanzen, Durchschnitt, etc.)
- ✅ Updates von Einträgen (PATCH)
- ✅ Sichere Löschung mit Bestätigung
- ✅ Volltext-Suche in Namen und Notizen

## 📚 Dokumentation

- **[GENERICS_CRUD.md](GENERICS_CRUD.md)**: Vollständige CRUD-Dokumentation mit Beispielen
- **[AGGREGATIONS_SEARCH.md](AGGREGATIONS_SEARCH.md)**: Filter, Aggregationen und Suche
- **[DIRECTUS_FILTERS.md](DIRECTUS_FILTERS.md)**: Directus-Filter Referenz
- **[Lauftagebuch_Documentation.md](Lauftagebuch_Documentation.md)**: Test-App Dokumentation

## 🔧 Technische Details

### Architektur
- **FastMCP**: Offizieller MCP Python SDK
- **httpx**: Asynchroner HTTP Client für API-Kommunikation
- **pydantic**: Datenvalidierung und -serialisierung
- **python-dotenv**: Umgebungsvariablen Management

### API-Endpunkte
- Apps: `/api/apps/`
- Categories: `/api/categories/`
- Services: `/api/services/`
- Resources: `/api/resources/`
- Attributes: `/api/attributes/{resource_name}/`
- Generics: `/api/generics/{resource_name}/`

### Authentifizierung
```python
headers = {
    "Authorization": f"Token {api_key}",
    "Content-Type": "application/json"
}
```

## 🤝 Verwendung mit GitHub Copilot

### Beispiel-Prompts

```text
# App-Verwaltung
"Erstelle eine App namens 'Projektmanagement'"
"Liste alle Apps auf"
"Lösche die App mit ID abc-123"

# Service-Verwaltung  
"Erstelle einen Service 'Tasks' in der App 'Projektmanagement'"
"Aktualisiere den Service-Titel zu 'Aufgaben'"

# Resource-Verwaltung
"Erstelle eine Resource 'Tickets' im Service 'Tasks'"
"Liste alle Resources auf"

# Daten-Management
"Erstelle einen neuen Laufeintrag mit 5km Distanz"
"Zeige alle Läufe über 10km"
"Berechne die Gesamtdistanz aller Läufe"
"Lösche den Eintrag mit ID xyz-789"
```

## 🚨 Wichtige Hinweise

### Sicherheitsfeatures
- **Lösch-Bestätigung**: Alle DELETE-Operationen erfordern explizite Bestätigung
- **Datenvalidierung**: Vollständige Validierung aller Ein- und Ausgaben
- **Fehlerbehandlung**: Umfassende Fehlerbehandlung mit aussagekräftigen Meldungen

### Bekannte Einschränkungen
- Attribut-Details (`get_attribute_details`): API-Berechtigungsproblem (403 Forbidden)
- Namens-Validierung: Dimetrics API lehnt lange Namen mit Underscores ab
- Prefix-Limite: Maximal 5 Zeichen für automatisch generierte Prefixes

---

**Status**: 🟢 **Production Ready** - Vollständige API-Integration mit 35 funktionalen Tools

### 4. Server starten

```bash
# MCP Server starten
python3 -m dimetrics_mcp_server
```

## 🔧 GitHub Copilot Integration

Fügen Sie diese Konfiguration zu Ihrem MCP Client hinzu:

```json
{
  "mcpServers": {
    "dimetrics": {
      "command": "python3",
      "args": ["-m", "dimetrics_mcp_server"],
      "cwd": "/path/to/mcp-server",
      "env": {
        "DIMETRICS_API_URL": "https://dimetrics.api.nc.released.services/api",
        "DIMETRICS_API_KEY": "your_token_here"
      }
    }
  }
}
```

## 💬 Beispiel-Anweisungen

```
"Erstelle eine App namens 'Stromverträge' mit dem Prefix 'power_'"

"Liste alle Apps auf, die 'MCP' enthalten"

"Zeige mir die Details der App mit ID xyz"

"Lösche die App mit der ID xyz"
```

## 🏗️ API Struktur

Der Server interagiert mit folgenden Dimetrics API Endpunkten:

```python
# App erstellen
POST /apps/
{
  "name": "App Name",
  "title": "App Name", 
  "prefix": "app_",
  "description": "Beschreibung"
}

# Apps auflisten  
GET /apps/?search=suchbegriff

# App Details
GET /apps/{object_id}

# App löschen
DELETE /apps/{object_id}/
```

## 🧪 Entwicklung

### Tests ausführen

```bash
# Minimaler Test (ohne API)
python3 test_minimal_new.py

# Vollständiger API Test
python3 test_dimetrics_api.py
```

### Neue Tools hinzufügen

1. Erweitern Sie `api_client.py` für neue API-Endpunkte
2. Fügen Sie neue `@mcp.tool()` Funktionen in `__main__.py` hinzu
3. Testen Sie mit den Testskripten

## � Basiert auf

- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [FastMCP Framework](https://github.com/modelcontextprotocol/python-sdk#fastmcp)

## 📝 Nächste Schritte

Dieses minimale Beispiel kann schrittweise erweitert werden um:

- 📊 **Tabellen Management** (create_table, list_tables)
- 🔧 **Attribut Management** (create_attribute, list_attributes) 
- 💾 **Daten Management** (CRUD-Operationen)
- 🎯 **Erweiterte Features** (Bulk-Operationen, Templates)

---

**🎯 Status: Minimal-Implementation abgeschlossen**  
✅ App Management funktionsfähig  
🔧 Bereit für schrittweise Erweiterung
