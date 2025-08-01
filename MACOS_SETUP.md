# Dimetrics MCP Server - Mac Installation

## 🚀 Schnelle Installation auf macOS

### 1. Repository klonen
```bash
git clone <YOUR_REPO_URL> ~/source/mcp-server
cd ~/source/mcp-server
```

### 2. Python Dependencies installieren
```bash
# Mit pip
pip3 install -r requirements.txt

# Oder mit homebrew python (falls installiert)
/opt/homebrew/bin/pip3 install -r requirements.txt
```

### 3. Environment-Datei erstellen
```bash
cp .env.example .env
# .env bearbeiten falls andere API-Credentials benötigt werden
```

### 4. Server testen
```bash
python3 -m dimetrics_mcp_server --help
```

## 📝 VS Code Integration

### mcp.json Konfiguration
Erstellen/Bearbeiten Sie: `~/Library/Application Support/Code/User/mcp.json`

```json
{
  "servers": {
    "dimetrics": {
      "type": "stdio",
      "command": "python3",
      "args": ["-m", "dimetrics_mcp_server"],
      "cwd": "/Users/YOUR_USERNAME/source/mcp-server",
      "env": {
        "DIMETRICS_API_URL": "https://dimetrics.api.nc.released.services/api",
        "DIMETRICS_API_KEY": "12345",
        "DEBUG": "true"
      }
    }
  },
  "inputs": []
}
```

### VS Code neu starten
Nach der Konfiguration VS Code komplett neu starten.

## 🔧 Troubleshooting

### Python-Pfad finden
```bash
which python3
```

### Dependencies prüfen
```bash
python3 -c "import mcp, httpx, asyncio; print('✅ Alle Dependencies verfügbar')"
```

### Server manuell testen
```bash
cd ~/source/mcp-server
python3 -m dimetrics_mcp_server
# Mit Ctrl+C beenden
```

## 🛠️ Verfügbare Tools

Der MCP Server stellt 29 Tools zur Verfügung:

### Apps Management (5 Tools)
- `create_app` - Neue App erstellen
- `list_apps` - Apps auflisten
- `get_app_details` - App-Details abrufen
- `update_app` - App aktualisieren
- `delete_app` - App löschen

### Categories Management (5 Tools)
- `create_category` - Neue Category erstellen
- `list_categories` - Categories auflisten
- `get_category_details` - Category-Details abrufen
- `update_category` - Category aktualisieren
- `delete_category` - Category löschen

### Services Management (5 Tools)
- `create_service` - Neuen Service erstellen
- `list_services` - Services auflisten
- `get_service_details` - Service-Details abrufen
- `update_service` - Service aktualisieren
- `delete_service` - Service löschen

### Resources Management (5 Tools)
- `create_resource` - Neue Resource erstellen
- `list_resources` - Resources auflisten
- `get_resource_details` - Resource-Details abrufen
- `update_resource` - Resource aktualisieren
- `delete_resource` - Resource löschen

### Attributes Management (9 Tools)
- `list_attributes` - Attribute einer Resource auflisten
- `get_attribute_details` - Attribut-Details abrufen
- `create_attribute` - Neues Attribut erstellen
- `update_attribute` - Attribut aktualisieren (✅ PATCH-korrigiert)
- `delete_attribute` - Attribut löschen
- `create_attributes_bulk` - Mehrere Attribute gleichzeitig erstellen

## ✅ Produktions-Status

**95% Funktionalität erreicht** (August 2025):
- ✅ Alle CRUD-Operationen für Apps, Categories, Services, Resources
- ✅ Vollständiges Attribut-Management mit korrigierter Update-Funktionalität
- ⚠️ Einzige Einschränkung: `get_attribute_details` (403 Forbidden - API-Permissions)

## 🔥 GitHub Copilot Chat Beispiele

```
@dimetrics liste alle verfügbaren Apps auf

@dimetrics erstelle eine neue App namens "Projektmanagement"

@dimetrics erstelle einen Service "Tasks" in der App mit ID xyz

@dimetrics liste alle Attribute der Resource "tasks" auf
```
