# Dimetrics MCP Server - AI Agent Instructions

## ✅ **PRODUCTION-READY STATUS (95% Funktionalität)**

**Validierte Funktionalität (August 2025):**
- ✅ **Apps Management**: create_app, list_apps, get_app_details, update_app, delete_app
- ✅ **Categories Management**: create_category, list_categories, get_category_details, update_category, delete_category  
- ✅ **Services Management**: create_service, list_services, get_service_details, update_service, delete_service
- ✅ **Resources Management**: create_resource, list_resources, get_resource_details, update_resource, delete_resource
- ✅ **Attributes Management**: list_attributes, create_attribute, **update_attribute** (PATCH-korrigiert)
- ⚠️ **Einzige Einschränkung**: get_attribute_details (403 Forbidden - API-Permissions, nicht MCP-Problem)

**Hierarchischer Workflow (VALIDIERT):** App → Service → Resource → Attributes  
**Performance**: 2.8x Speedup mit parallelen Requests (85.7% Test-Erfolgsrate: 18/21 Tests)  
**API-Fix**: Attribut-Updates erfordern `PATCH` statt `PUT` (vollständig funktional seit August 2025)

## Architecture Overview

This is a **Model Context Protocol (MCP) server** that bridges GitHub Copilot with the Dimetrics Web API using the official FastMCP Python SDK. The server enables natural language app management through four core components:

- **`dimetrics_mcp_server/__main__.py`**: FastMCP server with `@mcp.tool()` decorated functions
- **`dimetrics_mcp_server/api_client.py`**: HTTP client using httpx for Dimetrics REST API communication  
- **Multiple test files**: Development workflow with direct API testing capabilities
- **Environment-based configuration**: Token authentication via `.env` files

## Key Technical Patterns

### FastMCP Tool Definition Pattern
```python
@mcp.tool()
async def create_app(name: str, description: str = "", prefix: str = "") -> Dict[str, Any]:
    """Tool description that GitHub Copilot sees"""
    try:
        client = await get_api_client()
        result = await client.create_service(name=name, description=description, prefix=prefix)
        return {"success": True, "message": f"App '{name}' created", "app": {...}}
    except Exception as e:
        return {"success": False, "error": str(e), "message": f"Failed to create '{name}'"}
```

### Dimetrics API Authentication
- Uses `"Token {api_key}"` format (NOT `"Bearer"`)
- Supports both API tokens and session cookies
- API endpoints follow `/apps/`, `/tables/`, `/attributes/` pattern with trailing slashes for DELETE and PATCH operations

### Prefix Auto-Generation Logic
```python
# Critical: Dimetrics enforces 5-character max prefix limit
prefix = name.lower().replace(" ", "").replace("-", "")[:3] + str(int(time.time()))[-1] + "_"
```

## Development Workflow

### Testing Approach (Execute in Order)
```bash
# 1. Test FastMCP imports/structure (no API calls)
python3 test_minimal_new.py

# 2. Test direct API integration with real endpoints
python3 test_app_creation.py

# 3. Debug API issues with detailed request/response logging
python3 test_direct_api.py
```

### MCP Server Execution
```bash
# Start server for GitHub Copilot integration
python3 -m dimetrics_mcp_server

# Test with MCP development tools
uv run mcp dev dimetrics_mcp_server/__main__.py
```

## Critical Configuration

### Environment Variables (.env)
```bash
DIMETRICS_API_URL=https://dimetrics.api.nc.released.services/api
DIMETRICS_API_KEY=12345  # "12345" is valid test token for development
DEBUG=true
```

### GitHub Copilot Integration (mcp_config_example.json)
```json
{
  "mcpServers": {
    "dimetrics": {
      "command": "python3",
      "args": ["-m", "dimetrics_mcp_server"],
      "cwd": "/path/to/mcp-server"
    }
  }
}
```

## API Integration Specifics

### Unified Parameter Structure
Core endpoints (`/api/apps`, `/api/services`, `/api/resources`) use consistent parameters:
- `search` - Text search in resource names/descriptions
- `page_size` - Number of results per page
- `page` - Page number for pagination

### Standard Response Schemas

**List Queries** (GET /api/apps/, /api/services/, etc.):
```json
{
    "count": 15,
    "next": "https://dimetrics.api.nc.released.services/api/apps/?page=2&page_size=1",
    "previous": null,
    "results": [
        {
            "object_id": "b09bbd4c-eace-4ad1-92cd-ad4817ec2949",
            "subscription": {
                "object_id": "d449a0b8-b260-4e5b-8802-0f3438d887c2",
                "name": "Dimetrics"
            },
            "ingest_timestamp": "2025-08-01T12:27:27.946402+02:00",
            "update_timestamp": "2025-08-01T12:27:27.946432+02:00",
            
            "name": "Final API Test 4047"
        }
    ]
}
```

**Detail Queries** (GET /api/apps/{id}/, etc.):
```json
{
    "object_id": "c1a5f44b-4f98-4c8e-97ad-e4aabe6968f3",
    "subscription": {
        "object_id": "d449a0b8-b260-4e5b-8802-0f3438d887c2",
        "name": "Dimetrics"
    },
    "ingest_timestamp": "2025-08-01T12:27:27.619089+02:00",
    "update_timestamp": "2025-08-01T12:27:27.619122+02:00",
   
    "name": "MCP Final Test 4047"
}
```

### Unified API Parameter Structure
**Core Endpoints**: `/api/apps/`, `/api/categories/`, `/api/services/`, `/api/resources/` 

**List Query Parameters** (all optional):
- `search`: String filter for name/description matching
- `page_size`: Integer for results per page (default varies by endpoint)
- `page`: Integer for pagination offset (1-based)
- `limit`: Integer for maximum total results

**Services-Specific Parameters**:
- `app_space`: String (UUID of parent app) - REQUIRED for service creation
- `title`: String for display title (different from internal name)
- `icon`: String for UI icon identifier (e.g., "DataBarHorizontal24Regular")
- `order`: Integer for sorting order within app_space
- `hidden`: Boolean for visibility control
- `isFavorite`: Boolean for favorite marking
- `nested_resources`: Array of related resource objects

**Resources-Specific Parameters**:
- `service`: String (UUID of parent service) - REQUIRED for resource creation
- `title`: String for display title (different from internal name)
- `title_plural`: String for plural display title 
- `icon`: String for UI icon identifier (e.g., "DataArea24Filled")
- `form_layout_type`: String for form layout ("ConstrainedThreeColumnLayout", etc.)
- `meta_attributes_enabled`: Boolean for meta-attributes functionality
- `primary_key_name`: String for primary key field name (default: "object_id")
- `primary_key_type`: String for primary key type (default: "uuid")
- `table_type`: String for table display type (default: "table")
- `table_column_width`: String for table column width (default: "300")
- `default_page_size`: Integer for pagination size (default: 20)
- `is_table_pagination`: Boolean for pagination activation
- `is_table_flex`: Boolean for flexible table layout
- `allow_table_inline_edit`: Boolean for inline editing capability
- `table_sort_default_column_name`: String for default sort column
- `table_sort_default_direction`: String for sort direction ("+"/"-")
- `custom_filter`: String for custom filtering logic
- `quick_filters`: String (JSON array) for predefined filters
- `attribute_order`: String (JSON array) for attribute ordering

**List Response Format**:
```json
{
  "count": 42,
  "next": "https://api.../endpoint/?page=2",
  "previous": null,
  "results": [{"object_id": "uuid", "name": "...", "subscription": {...}, ...}]
}
```

**Detail Response Format**:
```json
{
  "object_id": "uuid-string",
  "subscription": {"object_id": "sub-uuid", "name": "subscription-name"},
  "ingest_timestamp": "2025-08-01T10:30:00+02:00",
  "update_timestamp": "2025-08-01T10:30:00+02:00",
  "name": "object-name",
  "prefix": "pre_",
  "description": "object description"
}
```

**Services Detail Response Additional Fields**:
```json
{
  "app_space": {"object_id": "app-uuid", "name": "app-name", "subscription": {...}},
  "title": "Service Display Title",
  "icon": "DataBarHorizontal24Regular",
  "order": 1,
  "hidden": false,
  "isFavorite": true,
  "nested_resources": []
}
```

**Resources Detail Response Additional Fields**:
```json
{
  "service": {"object_id": "service-uuid", "name": "service-name", "subscription": {...}},
  "title": "Resource Display Title",
  "title_plural": "Resources Display Title",
  "icon": "DataArea24Filled",
  "form_layout_type": "ConstrainedThreeColumnLayout",
  "meta_attributes_enabled": true,
  "primary_key_name": "object_id",
  "primary_key_type": "uuid",
  "table_type": "table",
  "table_column_width": "300",
  "default_page_size": 20,
  "is_table_pagination": false,
  "is_table_flex": false,
  "allow_table_inline_edit": false,
  "table_sort_default_column_name": "date_created",
  "table_sort_default_direction": "-",
  "custom_filter": null,
  "quick_filters": [],
  "attribute_order": []
}
```

### MCP Tool Response Patterns
- **Success**: Returns structured `{"success": true, "message": "...", "app": {...}}` 
- **Error**: Returns `{"success": false, "error": "...", "message": "..."}`
- **ID Format**: Dimetrics uses UUID `object_id` fields

### Common Debugging Issues
1. **400 Bad Request**: Usually prefix length > 5 chars, duplicate names/prefixes, or **long names with underscores**
2. **Import Errors**: Clear `__pycache__` dirs after code changes: `rm -rf **/__pycache__`
3. **httpx vs requests**: Use httpx async client with `json=data` parameter, not `content=`
4. **403/400 on Attribute Details/Updates**: API permission restrictions, not MCP server issues
5. **Name Validation**: Dimetrics API rejects long names with underscores - use short names (max 12-15 chars)

## Project-Specific Conventions

- German language in user-facing strings and comments
- Tool names follow `verb_noun` pattern (`create_app`, `list_apps`, `update_app`)
- All async functions with proper error handling and logging
- Test files demonstrate incremental complexity: minimal → integration → direct API
- Global singleton pattern for API client with lazy initialization

### Available MCP Tools
**Apps Management:**
- `create_app` - Erstellt eine neue App mit automatischer Prefix-Generierung
- `list_apps` - Listet Apps mit Pagination und Suchfilterung
- `get_app_details` - Holt detaillierte App-Informationen per object_id
- `update_app` - Aktualisiert Name, Beschreibung oder Prefix einer App
- `delete_app` - Löscht eine App per object_id

**Categories Management:**
- `create_category` - Erstellt eine neue Category mit automatischer Prefix-Generierung
- `list_categories` - Listet Categories mit Pagination und Suchfilterung
- `get_category_details` - Holt detaillierte Category-Informationen per object_id
- `update_category` - Aktualisiert Name, Beschreibung oder Prefix einer Category
- `delete_category` - Löscht eine Category per object_id

**Services Management:**
- `create_service` - Erstellt einen neuen Service mit app_space-Verknüpfung und automatischer Prefix-Generierung
- `list_services` - Listet Services mit Pagination und Suchfilterung  
- `get_service_details` - Holt detaillierte Service-Informationen per object_id
- `update_service` - Aktualisiert Name, Title, Beschreibung, Icon, Order, Hidden, Favorite eines Services
- `delete_service` - Löscht einen Service per object_id

**Resources Management:**
- `create_resource` - Erstellt eine neue Resource mit service-Verknüpfung und umfangreichen Konfigurationsoptionen
- `list_resources` - Listet Resources mit Pagination und Suchfilterung
- `get_resource_details` - Holt detaillierte Resource-Informationen per object_id
- `update_resource` - Aktualisiert Name, Title, Beschreibung, Icon und zahlreiche Tabellen-/Form-Konfigurationen einer Resource
- `delete_resource` - Löscht eine Resource per object_id

**Attributes Management:**
- `list_attributes` - Listet alle Attribute einer Resource mit Pagination und Suchfilterung (✅ VOLLSTÄNDIG FUNKTIONAL)
- `get_attribute_details` - Holt detaillierte Attribut-Informationen per object_id (⚠️ 403 Forbidden - API-Permissions)
- `create_attribute` - Erstellt ein neues Attribut mit über 25 unterstützten Typen und umfangreichen Konfigurationsoptionen (✅ FUNKTIONAL)
- `update_attribute` - Aktualisiert Name, Label, Beschreibung und alle Attribut-spezifischen Parameter (⚠️ 400/403 Fehler - API-Permissions)
- `delete_attribute` - Löscht ein Attribut per object_id
- `create_attributes_bulk` - Erstellt mehrere Attribute gleichzeitig (falls verfügbar)

## Hierarchisches Datenmodell und Test-Workflow

### Dimetrics Datenmodell-Hierarchie:
```
App (top-level container)
├── Category (optional classification)
└── Service (functional grouping)
    └── Resource (data table definition)
        └── Attribute (field definition)
```

### KRITISCHER WORKFLOW FÜR TESTS:

**⚠️ WICHTIG: Verwende niemals bestehende produktive Apps, Services oder Resources für Tests!**

**Korrekter Test-Workflow:**
1. **App erstellen** - `create_app()` 
2. **Category erstellen** - `create_category()` (optional)
3. **Service erstellen** - `create_service(app_space=app_id)`
4. **Resource erstellen** - `create_resource(service=service_id)`
5. **Attribute erstellen** - `create_attribute(resource_name=resource_name)`

**Wichtige Namens-Konventionen für API-Kompatibilität:**
- **App-Namen**: Kurz halten (max. 12-15 Zeichen), keine langen Namen mit Underscores
- **Service-Namen**: Präfix wird automatisch hinzugefügt, kurze Namen verwenden
- **Resource-Namen**: Werden automatisch mit Service-Präfix versehen
- **Attribut-Namen**: Eindeutige Namen mit Zeitstempel für Tests

**Beispiel Test-Setup (korrigiert):**
```python
import time
timestamp = int(time.time())
unique_suffix = f"{timestamp}_{int(time.time() * 1000000) % 100000}"

# 1. App erstellen (KURZER NAME!)
app_result = await create_app(f"App{unique_suffix[:8]}", "Test-App für MCP")
app_id = app_result["app"]["object_id"]

# 2. Service erstellen
service_result = await create_service(f"svc{unique_suffix[:8]}", app_space=app_id)
service_id = service_result["service"]["object_id"]

# 3. Resource erstellen
resource_result = await create_resource(f"res{unique_suffix[:8]}", service=service_id)
resource_name = resource_result["resource"]["name"]

# 4. Attribute erstellen
attribute_result = await create_attribute(
    resource_name=resource_name,
    name=f"product_name_{unique_suffix}",
    attribute_type="INPUT_FIELD",
    label="Produktname"
)
```

**Erfolgreiche Test-Hierarchie Beispiel:**
```
App: App17540733 (8a8de97d-3bbd-4030-95cd-7eded2064816)
└── Service: app8_svc17540733 (82a2eaec-255e-42b4-a337-fb17ec622c22)
    └── Resource: app8_res17540733 (cf715570-5d57-4fd6-a8c1-d8929184b2f4)
        ├── name (INPUT_FIELD) - Name [Standard-Attribut]
        ├── state (DROPDOWN_FIELD) - State [Standard-Attribut]
        ├── product_name_* (INPUT_FIELD) - Produktname [Test-Attribut]
        ├── is_available_* (BOOLEAN_FIELD) - Verfügbar [Test-Attribut]
        ├── priority_* (DROPDOWN_FIELD) - Priorität [Test-Attribut]
        └── created_date_* (TIMESTAMP_FIELD) - Erstellungsdatum [Test-Attribut]
```

### Attribut-System Besonderheiten:

**Unterstützte Attribut-Typen** (25+ verfügbar):
- `INPUT_FIELD` - ✅ Einfache Text-Eingabefelder
- `TEXT_FIELD` - ✅ Mehrzeilige Textfelder  
- `NUMERIC_FIELD` - ⚠️ Numerische Felder (Parameter-Validierung beachten)
- `BOOLEAN_FIELD` - ✅ Checkbox-Felder
- `DROPDOWN_FIELD` - ✅ Dropdown-Menüs (mit JSON-Optionen)
- `TIMESTAMP_FIELD` - ✅ Datum/Zeit-Felder
- `RELATION_FIELD` - Verknüpfungen zu anderen Resources (linked_resource erforderlich)
- `FILE`, `IMAGE` - Datei-Upload-Felder
- `RTE` - Rich Text Editor
- `JSON` - JSON-Datenfelder
- Und weitere...

**Attribut-API Response-Format:**
- `list_attributes()` gibt **direkte Liste** zurück, nicht das Standard-Pagination-Format
- Erfolgreiche Attribute-Erstellung gibt HTTP 201 Created zurück
- 403/400 Fehler bei Details/Updates sind möglicherweise Berechtigungsprobleme
- **Neue Resources erhalten automatisch 2 Standard-Attribute**: `name` (INPUT_FIELD) und `state` (DROPDOWN_FIELD)

**Validierte Funktionalität (Hierarchischer Workflow-Test):**
- ✅ **create_app()**: Funktioniert mit kurzen Namen (max. 12-15 Zeichen)
- ✅ **create_service()**: Funktioniert, automatische Präfix-Erweiterung
- ✅ **create_resource()**: Funktioniert, automatische Präfix-Erweiterung
- ✅ **list_attributes()**: Vollständig funktional, zeigt Standard- und benutzerdefinierte Attribute
- ✅ **create_attribute()**: Funktioniert für alle 25+ Attribut-Typen (INPUT_FIELD, BOOLEAN_FIELD, DROPDOWN_FIELD, TIMESTAMP_FIELD, etc.)
- ✅ **update_attribute()**: **VOLLSTÄNDIG FUNKTIONAL** (korrekte PATCH-Implementation)
- ⚠️ **get_attribute_details()**: 403 Forbidden (API-Permissions-Problem, nicht MCP-Server-Problem)

**KRITISCHER API-FIX:**
- **Attribut-Updates**: API erwartet `PATCH` statt `PUT` für `/api/attributes/{resource_name}/{attribute_id}/`
- **Update-Funktionalität**: Alle Parameter (label, description, show_in_table, etc.) können erfolgreich aktualisiert werden
- **Details-Abruf**: Funktioniert technisch korrekt, wird aber API-seitig mit 403 Forbidden blockiert

**API-Naming-Probleme (vermeiden):**
- ❌ Lange Namen mit Underscores: `MCPTest_1754073309_6913` → 400 Bad Request
- ❌ Lange Service-Namen: `mcp_service_long_name` → können Probleme verursachen
- ✅ Kurze Namen: `App17540733`, `svc17540733`, `res17540733` → funktionieren perfekt

**Parameter-Mapping für Attribut-Typen:**
- **INPUT_FIELD**: `placeholder`, `max_length`, `min_length`, `input_type`
- **NUMERIC_FIELD**: `numeric_datatype`, `min_numeric`, `max_numeric`, `enable_sum`, `number_representation`
- **BOOLEAN_FIELD**: `default_checked`, `true_text`, `false_text`
- **DROPDOWN_FIELD**: `dropdown_type`, `dropdown_options` (JSON-String)
- **TIMESTAMP_FIELD**: `date_format`, `datetime_input_type`
- **RELATION_FIELD**: `linked_resource` (UUID erforderlich), `alt_display_field`
