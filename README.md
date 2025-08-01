# Dimetrics MCP Server (FastMCP-basiert)

Ein Model Context Protocol (MCP) Server basierend auf dem offiziellen **FastMCP Python SDK**, der mit der Dimetrics Web-API interagiert und es GitHub Copilot ermöglicht, über natürliche Sprache Apps zu verwalten.

## ✨ Features

- **🏗️ App Management**: Erstellen, Auflisten, Details abrufen und Löschen von Apps
- **🚀 FastMCP Integration**: Basiert auf dem offiziellen MCP Python SDK
- **🔑 Flexible Authentifizierung**: Token-basierte API-Authentifizierung
- **📋 Natürlichsprachliche Steuerung**: GitHub Copilot Integration

## 🛠️ Verfügbare Tools

| Tool | Beschreibung | Parameter |
|------|--------------|-----------|
| `create_app` | Erstellt eine neue App | `name`, `description`, `prefix` |
| `list_apps` | Listet alle Apps auf | `search` (optional) |
| `get_app_details` | Holt App-Details | `object_id` |
| `delete_app` | Löscht eine App | `object_id` |

## � Schnellstart

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

### 3. Test

```bash
# Grundfunktionalität testen
python3 test_minimal_new.py

# Echte API testen (API Key erforderlich)
python3 test_dimetrics_api.py
```

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
