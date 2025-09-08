"""
Dimetrics MCP Server - Minimales Beispiel mit FastMCP.
"""

import os
import asyncio
import logging
from typing import Dict, Any
from dotenv import load_dotenv

# FastMCP Import
from mcp.server.fastmcp import FastMCP

from .api_client import DimetricsAPIClient

# Lade Umgebungsvariablen
load_dotenv()

# Logging konfigurieren
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Globaler API Client
api_client: DimetricsAPIClient = None

# FastMCP Server erstellen
mcp = FastMCP("Dimetrics MCP Server")

@mcp.tool()
async def health_check() -> Dict[str, Any]:
    """Health Check für den MCP Server."""
    try:
        client = await get_api_client()
        # Einfacher API-Test
        return {
            "status": "healthy",
            "message": "MCP Server läuft und API-Verbindung ist verfügbar",
            "timestamp": str(asyncio.get_event_loop().time()),
            "api_configured": bool(client)
        }
    except Exception as e:
        return {
            "status": "unhealthy", 
            "error": str(e),
            "message": "MCP Server läuft, aber API-Verbindung fehlgeschlagen"
        }

async def get_api_client() -> DimetricsAPIClient:
    """Gibt den konfigurierten API Client zurück."""
    global api_client
    
    if api_client is None:
        base_url = os.getenv("DIMETRICS_API_URL", "https://app.dimetrics.io/api")
        api_key = os.getenv("DIMETRICS_API_KEY")
        session_cookie = os.getenv("DIMETRICS_SESSION_COOKIE")
        
        if not api_key and not session_cookie:
            logger.warning("Keine Authentifizierung konfiguriert - verwende Mock-Modus")
        
        api_client = DimetricsAPIClient(
            base_url=base_url,
            api_key=api_key,
            session_cookie=session_cookie
        )
    
    return api_client

@mcp.tool()
async def create_app(name: str, description: str = "", prefix: str = "") -> Dict[str, Any]:
    """
    Erstellt eine neue App (Service) in Dimetrics.
    
    Args:
        name: Name der App
        description: Beschreibung der App
        prefix: Prefix für die App (optional, wird automatisch generiert wenn leer)
    
    Returns:
        Erstellte App-Informationen
    """
    try:
        client = await get_api_client()
        result = await client.create_app(name=name, description=description, prefix=prefix)
        
        return {
            "success": True,
            "message": f"App '{name}' erfolgreich erstellt",
            "app": {
                "object_id": result.get("object_id"),
                "name": result.get("name"),
                "prefix": result.get("prefix"),
                "description": result.get("description"),
                "icon": result.get("icon"),
                "ingest_timestamp": result.get("ingest_timestamp"),
                "update_timestamp": result.get("update_timestamp")
            }
        }
    except Exception as e:
        logger.error(f"Fehler beim Erstellen der App: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Erstellen der App '{name}'"
        }

@mcp.tool()
async def list_apps(
    search: str = "", 
    page_size: int = 0, 
    page: int = 0, 
    limit: int = 0
) -> Dict[str, Any]:
    """
    Listet alle verfügbaren Apps auf mit erweiterten Filteroptionen.
    
    Args:
        search: Optionaler Suchbegriff für Filtering
        page_size: Anzahl der Ergebnisse pro Seite (0 = Standard)
        page: Seitennummer (0 = keine Pagination)
        limit: Maximale Anzahl der Ergebnisse (0 = kein Limit)
    
    Returns:
        Liste aller Apps mit Pagination-Informationen
    """
    try:
        client = await get_api_client()
        
        # Parameter nur setzen wenn sie nicht 0 sind
        kwargs = {}
        if search:
            kwargs["search"] = search
        if page_size > 0:
            kwargs["page_size"] = page_size
        if page > 0:
            kwargs["page"] = page
        if limit > 0:
            kwargs["limit"] = limit
        
        result = await client.list_services(**kwargs)
        
        return {
            "success": True,
            "count": result.get("count", 0),
            "next": result.get("next"),
            "previous": result.get("previous"),
            "apps": [
                {
                    "object_id": app.get("object_id"),
                    "name": app.get("name"),
                    "prefix": app.get("prefix"),
                    "description": app.get("description", ""),
                    "icon": app.get("icon"),
                    "subscription": app.get("subscription", {}),
                    "ingest_timestamp": app.get("ingest_timestamp"),
                    "update_timestamp": app.get("update_timestamp")
                }
                for app in result.get("results", [])
            ]
        }
    except Exception as e:
        logger.error(f"Fehler beim Auflisten der Apps: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Fehler beim Auflisten der Apps"
        }

@mcp.tool()
async def get_app_details(object_id: str) -> Dict[str, Any]:
    """
    Holt Details einer spezifischen App.
    
    Args:
        object_id: object_id der App (UUID)
    
    Returns:
        App-Details
    """
    try:
        client = await get_api_client()
        app = await client.get_service(object_id)
        
        return {
            "success": True,
            "app": {
                "object_id": app.get("object_id"),
                "name": app.get("name"),
                "prefix": app.get("prefix"),
                "description": app.get("description", ""),
                "icon": app.get("icon"),
                "ingest_timestamp": app.get("ingest_timestamp"),
                "update_timestamp": app.get("update_timestamp"),
                "subscription": app.get("subscription", {})
            }
        }
    except Exception as e:
        logger.error(f"Fehler beim Abrufen der App-Details: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Abrufen der Details für App '{object_id}'"
        }

@mcp.tool()
async def delete_app(object_id: str) -> Dict[str, Any]:
    """
    Löscht eine App.
    
    Args:
        object_id: object_id der zu löschenden App (UUID)
    
    Returns:
        Löschstatus
    """
    try:
        client = await get_api_client()
        success = await client.delete_service(object_id)
        
        return {
            "success": success,
            "message": f"App '{object_id}' erfolgreich gelöscht" if success else f"App '{object_id}' konnte nicht gelöscht werden"
        }
    except Exception as e:
        logger.error(f"Fehler beim Löschen der App: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Löschen der App '{object_id}'"
        }

@mcp.tool()
async def update_app(
    object_id: str, 
    name: str = None, 
    description: str = None, 
    prefix: str = None
) -> Dict[str, Any]:
    """
    Aktualisiert eine bestehende App.
    
    Args:
        object_id: object_id der zu aktualisierenden App (UUID)
        name: Neuer Name der App (optional)
        description: Neue Beschreibung der App (optional)
        prefix: Neuer Prefix der App (optional, max 5 Zeichen)
    
    Returns:
        Aktualisierte App-Informationen
    """
    try:
        client = await get_api_client()
        result = await client.update_service(
            app_id=object_id,
            name=name,
            description=description,
            prefix=prefix
        )
        
        return {
            "success": True,
            "message": f"App '{object_id}' erfolgreich aktualisiert",
            "app": {
                "object_id": result.get("object_id"),
                "name": result.get("name"),
                "prefix": result.get("prefix"),
                "description": result.get("description"),
                "icon": result.get("icon"),
                "ingest_timestamp": result.get("ingest_timestamp"),
                "update_timestamp": result.get("update_timestamp"),
                "subscription": result.get("subscription", {})
            }
        }
    except Exception as e:
        logger.error(f"Fehler beim Aktualisieren der App: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Aktualisieren der App '{object_id}'"
        }

# Categories Tools
@mcp.tool()
async def create_category(name: str, description: str = "", prefix: str = "") -> Dict[str, Any]:
    """
    Erstellt eine neue Category in Dimetrics.
    
    Args:
        name: Name der Category
        description: Beschreibung der Category
        prefix: Prefix für die Category (optional, wird automatisch generiert wenn leer)
    
    Returns:
        Erstellte Category-Informationen
    """
    try:
        client = await get_api_client()
        result = await client.create_category(name=name, description=description, prefix=prefix)
        
        return {
            "success": True,
            "message": f"Category '{name}' erfolgreich erstellt",
            "category": {
                "object_id": result.get("object_id"),
                "name": result.get("name"),
                "prefix": result.get("prefix"),
                "description": result.get("description"),
                "icon": result.get("icon"),
                "ingest_timestamp": result.get("ingest_timestamp"),
                "update_timestamp": result.get("update_timestamp")
            }
        }
    except Exception as e:
        logger.error(f"Fehler beim Erstellen der Category: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Erstellen der Category '{name}'"
        }

@mcp.tool()
async def list_categories(
    search: str = "", 
    page_size: int = 0, 
    page: int = 0, 
    limit: int = 0
) -> Dict[str, Any]:
    """
    Listet alle verfügbaren Categories auf mit erweiterten Filteroptionen.
    
    Args:
        search: Optionaler Suchbegriff für Filtering
        page_size: Anzahl der Ergebnisse pro Seite (0 = Standard)
        page: Seitennummer (0 = keine Pagination)
        limit: Maximale Anzahl der Ergebnisse (0 = kein Limit)
    
    Returns:
        Liste aller Categories mit Pagination-Informationen
    """
    try:
        client = await get_api_client()
        
        # Parameter nur setzen wenn sie nicht 0 sind
        kwargs = {}
        if search:
            kwargs["search"] = search
        if page_size > 0:
            kwargs["page_size"] = page_size
        if page > 0:
            kwargs["page"] = page
        if limit > 0:
            kwargs["limit"] = limit
        
        result = await client.list_categories(**kwargs)
        
        return {
            "success": True,
            "count": result.get("count", 0),
            "next": result.get("next"),
            "previous": result.get("previous"),
            "categories": [
                {
                    "object_id": category.get("object_id"),
                    "name": category.get("name"),
                    "prefix": category.get("prefix"),
                    "description": category.get("description", ""),
                    "icon": category.get("icon"),
                    "subscription": category.get("subscription", {}),
                    "ingest_timestamp": category.get("ingest_timestamp"),
                    "update_timestamp": category.get("update_timestamp")
                }
                for category in result.get("results", [])
            ]
        }
    except Exception as e:
        logger.error(f"Fehler beim Auflisten der Categories: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Fehler beim Auflisten der Categories"
        }

@mcp.tool()
async def get_category_details(object_id: str) -> Dict[str, Any]:
    """
    Holt Details einer spezifischen Category.
    
    Args:
        object_id: object_id der Category (UUID)
    
    Returns:
        Category-Details
    """
    try:
        client = await get_api_client()
        category = await client.get_category(object_id)
        
        return {
            "success": True,
            "category": {
                "object_id": category.get("object_id"),
                "name": category.get("name"),
                "prefix": category.get("prefix"),
                "description": category.get("description", ""),
                "icon": category.get("icon"),
                "ingest_timestamp": category.get("ingest_timestamp"),
                "update_timestamp": category.get("update_timestamp"),
                "subscription": category.get("subscription", {})
            }
        }
    except Exception as e:
        logger.error(f"Fehler beim Abrufen der Category-Details: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Abrufen der Details für Category '{object_id}'"
        }

@mcp.tool()
async def update_category(
    object_id: str, 
    name: str = None, 
    description: str = None, 
    prefix: str = None
) -> Dict[str, Any]:
    """
    Aktualisiert eine bestehende Category.
    
    Args:
        object_id: object_id der zu aktualisierenden Category (UUID)
        name: Neuer Name der Category (optional)
        description: Neue Beschreibung der Category (optional)
        prefix: Neuer Prefix der Category (optional, max 5 Zeichen)
    
    Returns:
        Aktualisierte Category-Informationen
    """
    try:
        client = await get_api_client()
        result = await client.update_category(
            category_id=object_id,
            name=name,
            description=description,
            prefix=prefix
        )
        
        return {
            "success": True,
            "message": f"Category '{object_id}' erfolgreich aktualisiert",
            "category": {
                "object_id": result.get("object_id"),
                "name": result.get("name"),
                "prefix": result.get("prefix"),
                "description": result.get("description"),
                "icon": result.get("icon"),
                "ingest_timestamp": result.get("ingest_timestamp"),
                "update_timestamp": result.get("update_timestamp"),
                "subscription": result.get("subscription", {})
            }
        }
    except Exception as e:
        logger.error(f"Fehler beim Aktualisieren der Category: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Aktualisieren der Category '{object_id}'"
        }

@mcp.tool()
async def delete_category(object_id: str) -> Dict[str, Any]:
    """
    Löscht eine Category.
    
    Args:
        object_id: object_id der zu löschenden Category (UUID)
    
    Returns:
        Löschstatus
    """
    try:
        client = await get_api_client()
        success = await client.delete_category(object_id)
        
        return {
            "success": success,
            "message": f"Category '{object_id}' erfolgreich gelöscht" if success else f"Category '{object_id}' konnte nicht gelöscht werden"
        }
    except Exception as e:
        logger.error(f"Fehler beim Löschen der Category: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Löschen der Category '{object_id}'"
        }

# Services Tools
@mcp.tool()
async def create_service(
    name: str, 
    app_space: str, 
    title: str = "", 
    description: str = "", 
    category: str = "",
    icon: str = "DataBarHorizontal24Regular",
    order: int = 0,
    hidden: bool = False,
    isFavorite: bool = False
) -> Dict[str, Any]:
    """
    Erstellt einen neuen Service in Dimetrics.
    
    Args:
        name: Name des Services (unique identifier)
        app_space: object_id der App zu der der Service gehört (Pflichtfeld)
        title: Anzeigename des Services (optional, default = name)
        description: Beschreibung des Services
        category: object_id der Category (optional)
        icon: Icon für den Service (default: DataBarHorizontal24Regular)
        order: Reihenfolge/Sortierung (default: 0)
        hidden: Ob der Service versteckt ist (default: False)
        isFavorite: Ob der Service als Favorit markiert ist (default: False)
    
    Returns:
        Erstellte Service-Informationen
    """
    try:
        client = await get_api_client()
        result = await client.create_service_endpoint(
            name=name,
            app_space=app_space,
            title=title or name,
            description=description,
            category=category if category else None,
            icon=icon,
            order=order,
            hidden=hidden,
            isFavorite=isFavorite
        )
        
        return {
            "success": True,
            "message": f"Service '{name}' erfolgreich erstellt",
            "service": {
                "object_id": result.get("object_id"),
                "name": result.get("name"),
                "title": result.get("title"),
                "description": result.get("description"),
                "app_space": result.get("app_space"),
                "category": result.get("category"),
                "icon": result.get("icon"),
                "order": result.get("order"),
                "hidden": result.get("hidden"),
                "isFavorite": result.get("isFavorite"),
                "nested_resources": result.get("nested_resources", []),
                "ingest_timestamp": result.get("ingest_timestamp"),
                "update_timestamp": result.get("update_timestamp")
            }
        }
    except Exception as e:
        logger.error(f"Fehler beim Erstellen des Services: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Erstellen des Services '{name}'"
        }

@mcp.tool()
async def list_services(
    search: str = "", 
    page_size: int = 0, 
    page: int = 0, 
    limit: int = 0
) -> Dict[str, Any]:
    """
    Listet alle verfügbaren Services auf mit erweiterten Filteroptionen.
    
    Args:
        search: Optionaler Suchbegriff für Filtering
        page_size: Anzahl der Ergebnisse pro Seite (0 = Standard)
        page: Seitennummer (0 = keine Pagination)
        limit: Maximale Anzahl der Ergebnisse (0 = kein Limit)
    
    Returns:
        Liste aller Services mit Pagination-Informationen
    """
    try:
        client = await get_api_client()
        
        # Parameter nur setzen wenn sie nicht 0 sind
        kwargs = {}
        if search:
            kwargs["search"] = search
        if page_size > 0:
            kwargs["page_size"] = page_size
        if page > 0:
            kwargs["page"] = page
        if limit > 0:
            kwargs["limit"] = limit
        
        result = await client.list_services_endpoint(**kwargs)
        
        return {
            "success": True,
            "count": result.get("count", 0),
            "next": result.get("next"),
            "previous": result.get("previous"),
            "services": [
                {
                    "object_id": service.get("object_id"),
                    "name": service.get("name"),
                    "title": service.get("title"),
                    "description": service.get("description", ""),
                    "app_space": service.get("app_space"),
                    "category": service.get("category"),
                    "icon": service.get("icon"),
                    "order": service.get("order"),
                    "hidden": service.get("hidden"),
                    "isFavorite": service.get("isFavorite"),
                    "nested_resources": service.get("nested_resources", []),
                    "subscription": service.get("subscription", {}),
                    "ingest_timestamp": service.get("ingest_timestamp"),
                    "update_timestamp": service.get("update_timestamp")
                }
                for service in result.get("results", [])
            ]
        }
    except Exception as e:
        logger.error(f"Fehler beim Auflisten der Services: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Fehler beim Auflisten der Services"
        }

@mcp.tool()
async def get_service_details(object_id: str) -> Dict[str, Any]:
    """
    Holt Details eines spezifischen Services.
    
    Args:
        object_id: object_id des Services (UUID)
    
    Returns:
        Service-Details
    """
    try:
        client = await get_api_client()
        service = await client.get_service_endpoint(object_id)
        
        return {
            "success": True,
            "service": {
                "object_id": service.get("object_id"),
                "name": service.get("name"),
                "title": service.get("title"),
                "description": service.get("description", ""),
                "app_space": service.get("app_space"),
                "category": service.get("category"),
                "icon": service.get("icon"),
                "order": service.get("order"),
                "hidden": service.get("hidden"),
                "isFavorite": service.get("isFavorite"),
                "nested_resources": service.get("nested_resources", []),
                "subscription": service.get("subscription", {}),
                "ingest_timestamp": service.get("ingest_timestamp"),
                "update_timestamp": service.get("update_timestamp")
            }
        }
    except Exception as e:
        logger.error(f"Fehler beim Abrufen der Service-Details: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Abrufen der Details für Service '{object_id}'"
        }

@mcp.tool()
async def update_service(
    object_id: str, 
    name: str = None, 
    title: str = None,
    description: str = None, 
    category: str = None,
    app_space: str = None,
    icon: str = None,
    order: int = None,
    hidden: bool = None,
    isFavorite: bool = None
) -> Dict[str, Any]:
    """
    Aktualisiert einen bestehenden Service.
    
    Args:
        object_id: object_id des zu aktualisierenden Services (UUID)
        name: Neuer Name des Services (optional)
        title: Neuer Titel des Services (optional)
        description: Neue Beschreibung des Services (optional)
        category: Neue Category ID (optional)
        app_space: Neue App Space ID (optional)
        icon: Neues Icon (optional)
        order: Neue Reihenfolge (optional)
        hidden: Neuer Hidden Status (optional)
        isFavorite: Neuer Favorite Status (optional)
    
    Returns:
        Aktualisierte Service-Informationen
    """
    try:
        client = await get_api_client()
        result = await client.update_service_endpoint(
            service_id=object_id,
            name=name,
            title=title,
            description=description,
            category=category,
            app_space=app_space,
            icon=icon,
            order=order,
            hidden=hidden,
            isFavorite=isFavorite
        )
        
        return {
            "success": True,
            "message": f"Service '{object_id}' erfolgreich aktualisiert",
            "service": {
                "object_id": result.get("object_id"),
                "name": result.get("name"),
                "title": result.get("title"),
                "description": result.get("description"),
                "app_space": result.get("app_space"),
                "category": result.get("category"),
                "icon": result.get("icon"),
                "order": result.get("order"),
                "hidden": result.get("hidden"),
                "isFavorite": result.get("isFavorite"),
                "nested_resources": result.get("nested_resources", []),
                "subscription": result.get("subscription", {}),
                "ingest_timestamp": result.get("ingest_timestamp"),
                "update_timestamp": result.get("update_timestamp")
            }
        }
    except Exception as e:
        logger.error(f"Fehler beim Aktualisieren des Services: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Aktualisieren des Services '{object_id}'"
        }

@mcp.tool()
async def delete_service(object_id: str) -> Dict[str, Any]:
    """
    Löscht einen Service.
    
    Args:
        object_id: object_id des zu löschenden Services (UUID)
    
    Returns:
        Löschstatus
    """
    try:
        client = await get_api_client()
        success = await client.delete_service_endpoint(object_id)
        
        return {
            "success": success,
            "message": f"Service '{object_id}' erfolgreich gelöscht" if success else f"Service '{object_id}' konnte nicht gelöscht werden"
        }
    except Exception as e:
        logger.error(f"Fehler beim Löschen des Services: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Löschen des Services '{object_id}'"
        }

# Resources Tools
@mcp.tool()
async def create_resource(
    name: str, 
    service: str, 
    title: str = "", 
    title_plural: str = "",
    description: str = "",
    icon: str = "DataArea24Filled",
    form_layout_type: str = "ConstrainedThreeColumnLayout",
    meta_attributes_enabled: bool = True,
    database_connection: str = "",
    primary_key_name: str = "object_id",
    primary_key_type: str = "uuid",
    table_type: str = "table",
    table_column_width: str = "300",
    default_page_size: int = 20,
    is_table_pagination: bool = False,
    is_table_flex: bool = False,
    allow_table_inline_edit: bool = False,
    table_sort_default_column_name: str = "date_created",
    table_sort_default_direction: str = "-",
    custom_filter: str = "",
    quick_filters: str = "[]",
    attribute_order: str = "[]"
) -> Dict[str, Any]:
    """
    Erstellt eine neue Resource in Dimetrics.
    
    Args:
        name: Name der Resource (unique identifier)
        service: object_id des Services zu dem die Resource gehört (Pflichtfeld)
        title: Anzeigename der Resource (optional, default = name)
        title_plural: Plural-Anzeigename (optional, default = title)
        description: Beschreibung der Resource
        icon: Icon für die Resource (default: DataArea24Filled)
        form_layout_type: Layout-Typ (default: ConstrainedThreeColumnLayout)
        meta_attributes_enabled: Meta-Attribute aktiviert (default: True)
        database_connection: Database Connection String (optional)
        primary_key_name: Name des Primary Keys (default: object_id)
        primary_key_type: Typ des Primary Keys (default: uuid)
        table_type: Tabellen-Typ (default: table)
        table_column_width: Spaltenbreite (default: 300)
        default_page_size: Standard-Seitengröße (default: 20)
        is_table_pagination: Pagination aktiviert (default: False)
        is_table_flex: Flex-Layout aktiviert (default: False)
        allow_table_inline_edit: Inline-Editing erlaubt (default: False)
        table_sort_default_column_name: Standard-Sort-Spalte (default: date_created)
        table_sort_default_direction: Sort-Richtung (default: -)
        custom_filter: Custom Filter (optional)
        quick_filters: Quick Filters JSON (default: [])
        attribute_order: Attribut-Reihenfolge JSON (default: [])
    
    Returns:
        Erstellte Resource-Informationen
    """
    try:
        client = await get_api_client()
        result = await client.create_resource_endpoint(
            name=name,
            service=service,
            title=title,
            title_plural=title_plural,
            description=description,
            form_layout_type=form_layout_type,
            meta_attributes_enabled=meta_attributes_enabled,
            database_connection=database_connection,
            primary_key_name=primary_key_name,
            primary_key_type=primary_key_type,
            table_type=table_type,
            table_column_width=table_column_width,
            default_page_size=default_page_size,
            is_table_pagination=is_table_pagination,
            is_table_flex=is_table_flex,
            allow_table_inline_edit=allow_table_inline_edit,
            table_sort_default_column_name=table_sort_default_column_name
        )
        
        return {
            "success": True,
            "message": f"Resource '{name}' erfolgreich erstellt",
            "resource": {
                "object_id": result.get("object_id"),
                "name": result.get("name"),
                "title": result.get("title"),
                "title_plural": result.get("title_plural"),
                "description": result.get("description"),
                "service": result.get("service"),
                "icon": result.get("icon"),
                "form_layout_type": result.get("form_layout_type"),
                "meta_attributes_enabled": result.get("meta_attributes_enabled"),
                "primary_key_name": result.get("primary_key_name"),
                "primary_key_type": result.get("primary_key_type"),
                "table_type": result.get("table_type"),
                "default_page_size": result.get("default_page_size"),
                "is_table_pagination": result.get("is_table_pagination"),
                "is_table_flex": result.get("is_table_flex"),
                "allow_table_inline_edit": result.get("allow_table_inline_edit"),
                "ingest_timestamp": result.get("ingest_timestamp"),
                "update_timestamp": result.get("update_timestamp")
            }
        }
    except Exception as e:
        logger.error(f"Fehler beim Erstellen der Resource: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Erstellen der Resource '{name}'"
        }

@mcp.tool()
async def list_resources(
    search: str = "", 
    page_size: int = 0, 
    page: int = 0, 
    limit: int = 0
) -> Dict[str, Any]:
    """
    Listet alle verfügbaren Resources auf mit erweiterten Filteroptionen.
    
    Args:
        search: Optionaler Suchbegriff für Filtering
        page_size: Anzahl der Ergebnisse pro Seite (0 = Standard)
        page: Seitennummer (0 = keine Pagination)
        limit: Maximale Anzahl der Ergebnisse (0 = kein Limit)
    
    Returns:
        Liste aller Resources mit Pagination-Informationen
    """
    try:
        client = await get_api_client()
        
        # Parameter nur setzen wenn sie nicht 0 sind
        kwargs = {}
        if search:
            kwargs["search"] = search
        if page_size > 0:
            kwargs["page_size"] = page_size
        if page > 0:
            kwargs["page"] = page
        if limit > 0:
            kwargs["limit"] = limit
        
        result = await client.list_resources_endpoint(**kwargs)
        
        return {
            "success": True,
            "count": result.get("count", 0),
            "next": result.get("next"),
            "previous": result.get("previous"),
            "resources": [
                {
                    "object_id": resource.get("object_id"),
                    "name": resource.get("name"),
                    "title": resource.get("title"),
                    "title_plural": resource.get("title_plural"),
                    "description": resource.get("description", ""),
                    "service": resource.get("service"),
                    "icon": resource.get("icon"),
                    "table_type": resource.get("table_type"),
                    "meta_attributes_enabled": resource.get("meta_attributes_enabled"),
                    "subscription": resource.get("subscription", {}),
                    "ingest_timestamp": resource.get("ingest_timestamp"),
                    "update_timestamp": resource.get("update_timestamp")
                }
                for resource in result.get("results", [])
            ]
        }
    except Exception as e:
        logger.error(f"Fehler beim Auflisten der Resources: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Fehler beim Auflisten der Resources"
        }

@mcp.tool()
async def get_resource_details(object_id: str) -> Dict[str, Any]:
    """
    Holt Details einer spezifischen Resource.
    
    Args:
        object_id: object_id der Resource (UUID)
    
    Returns:
        Resource-Details
    """
    try:
        client = await get_api_client()
        resource = await client.get_resource_endpoint(object_id)
        
        return {
            "success": True,
            "resource": {
                "object_id": resource.get("object_id"),
                "name": resource.get("name"),
                "title": resource.get("title"),
                "title_plural": resource.get("title_plural"),
                "description": resource.get("description", ""),
                "service": resource.get("service"),
                "icon": resource.get("icon"),
                "form_layout_type": resource.get("form_layout_type"),
                "meta_attributes_enabled": resource.get("meta_attributes_enabled"),
                "primary_key_name": resource.get("primary_key_name"),
                "primary_key_type": resource.get("primary_key_type"),
                "table_type": resource.get("table_type"),
                "table_column_width": resource.get("table_column_width"),
                "default_page_size": resource.get("default_page_size"),
                "is_table_pagination": resource.get("is_table_pagination"),
                "is_table_flex": resource.get("is_table_flex"),
                "allow_table_inline_edit": resource.get("allow_table_inline_edit"),
                "table_sort_default_column_name": resource.get("table_sort_default_column_name"),
                "table_sort_default_direction": resource.get("table_sort_default_direction"),
                "subscription": resource.get("subscription", {}),
                "ingest_timestamp": resource.get("ingest_timestamp"),
                "update_timestamp": resource.get("update_timestamp")
            }
        }
    except Exception as e:
        logger.error(f"Fehler beim Abrufen der Resource-Details: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Abrufen der Details für Resource '{object_id}'"
        }

@mcp.tool()
async def update_resource(
    object_id: str, 
    name: str = None, 
    title: str = None,
    title_plural: str = None,
    description: str = None, 
    icon: str = None,
    form_layout_type: str = None,
    meta_attributes_enabled: bool = None,
    database_connection: str = None,
    primary_key_name: str = None,
    primary_key_type: str = None,
    table_type: str = None,
    table_column_width: str = None,
    default_page_size: int = None,
    is_table_pagination: bool = None,
    is_table_flex: bool = None,
    allow_table_inline_edit: bool = None,
    table_sort_default_column_name: str = None,
    table_sort_default_direction: str = None,
    custom_filter: str = None,
    quick_filters: str = None,
    attribute_order: str = None
) -> Dict[str, Any]:
    """
    Aktualisiert eine bestehende Resource.
    
    Args:
        object_id: object_id der zu aktualisierenden Resource (UUID)
        name: Neuer Name der Resource (optional)
        title: Neuer Titel der Resource (optional)
        title_plural: Neuer Plural-Titel (optional)
        description: Neue Beschreibung der Resource (optional)
        icon: Neues Icon (optional)
        form_layout_type: Neuer Layout-Typ (optional)
        meta_attributes_enabled: Meta-Attribute Status (optional)
        database_connection: Database Connection (optional)
        primary_key_name: Primary Key Name (optional)
        primary_key_type: Primary Key Type (optional)
        table_type: Tabellen-Typ (optional)
        table_column_width: Spaltenbreite (optional)
        default_page_size: Standard-Seitengröße (optional)
        is_table_pagination: Pagination Status (optional)
        is_table_flex: Flex-Layout Status (optional)
        allow_table_inline_edit: Inline-Edit Status (optional)
        table_sort_default_column_name: Sort-Spalte (optional)
        table_sort_default_direction: Sort-Richtung (optional)
        custom_filter: Custom Filter (optional)
        quick_filters: Quick Filters (optional)
        attribute_order: Attribut-Reihenfolge (optional)
    
    Returns:
        Aktualisierte Resource-Informationen
    """
    try:
        client = await get_api_client()
        result = await client.update_resource_endpoint(
            resource_id=object_id,
            name=name,
            title=title,
            title_plural=title_plural,
            description=description,
            form_layout_type=form_layout_type,
            meta_attributes_enabled=meta_attributes_enabled,
            database_connection=database_connection,
            primary_key_name=primary_key_name,
            primary_key_type=primary_key_type,
            table_type=table_type,
            table_column_width=table_column_width,
            default_page_size=default_page_size,
            is_table_pagination=is_table_pagination,
            is_table_flex=is_table_flex,
            allow_table_inline_edit=allow_table_inline_edit,
            table_sort_default_column_name=table_sort_default_column_name
        )
        
        return {
            "success": True,
            "message": f"Resource '{object_id}' erfolgreich aktualisiert",
            "resource": {
                "object_id": result.get("object_id"),
                "name": result.get("name"),
                "title": result.get("title"),
                "title_plural": result.get("title_plural"),
                "description": result.get("description"),
                "service": result.get("service"),
                "icon": result.get("icon"),
                "form_layout_type": result.get("form_layout_type"),
                "meta_attributes_enabled": result.get("meta_attributes_enabled"),
                "primary_key_name": result.get("primary_key_name"),
                "primary_key_type": result.get("primary_key_type"),
                "table_type": result.get("table_type"),
                "subscription": result.get("subscription", {}),
                "ingest_timestamp": result.get("ingest_timestamp"),
                "update_timestamp": result.get("update_timestamp")
            }
        }
    except Exception as e:
        logger.error(f"Fehler beim Aktualisieren der Resource: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Aktualisieren der Resource '{object_id}'"
        }

@mcp.tool()
async def delete_resource(object_id: str) -> Dict[str, Any]:
    """
    Löscht eine Resource.
    
    Args:
        object_id: object_id der zu löschenden Resource (UUID)
    
    Returns:
        Löschstatus
    """
    try:
        client = await get_api_client()
        success = await client.delete_resource_endpoint(object_id)
        
        return {
            "success": success,
            "message": f"Resource '{object_id}' erfolgreich gelöscht" if success else f"Resource '{object_id}' konnte nicht gelöscht werden"
        }
    except Exception as e:
        logger.error(f"Fehler beim Löschen der Resource: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Löschen der Resource '{object_id}'"
        }

# Ressourcen für Übersicht
@mcp.resource("dimetrics://apps")
def list_apps_resource() -> str:
    """
    Ressource für die Übersicht aller Apps.
    
    Returns:
        JSON-String mit App-Informationen
    """
    # Diese Ressource wird asynchron von list_apps() Tool verwendet
    return "Verwenden Sie das 'list_apps' Tool um aktuelle App-Informationen abzurufen."

@mcp.resource("dimetrics://categories")
def list_categories_resource() -> str:
    """
    Ressource für die Übersicht aller Categories.
    
    Returns:
        JSON-String mit Category-Informationen
    """
    # Diese Ressource wird asynchron von list_categories() Tool verwendet
    return "Verwenden Sie das 'list_categories' Tool um aktuelle Category-Informationen abzurufen."

@mcp.resource("dimetrics://services")
def list_services_resource() -> str:
    """
    Ressource für die Übersicht aller Services.
    
    Returns:
        JSON-String mit Service-Informationen
    """
    # Diese Ressource wird asynchron von list_services() Tool verwendet
    return "Verwenden Sie das 'list_services' Tool um aktuelle Service-Informationen abzurufen."

@mcp.resource("dimetrics://resources")
def list_resources_resource() -> str:
    """
    Ressource für die Übersicht aller Resources.
    
    Returns:
        JSON-String mit Resource-Informationen
    """
    # Diese Ressource wird asynchron von list_resources() Tool verwendet
    return "Verwenden Sie das 'list_resources' Tool um aktuelle Resource-Informationen abzurufen."

# Hauptfunktion zum Starten des Servers
def main():
    """Startet den FastMCP Server."""
    logger.info("🚀 Starte Dimetrics MCP Server (Minimal-Version)...")
    logger.info("📋 Verfügbare Tools:")
    logger.info("  Apps:")
    logger.info("    • create_app - Erstellt eine neue App")
    logger.info("    • list_apps - Listet alle Apps auf")
    logger.info("    • get_app_details - Holt App-Details")
    logger.info("    • update_app - Aktualisiert eine App")
    logger.info("    • delete_app - Löscht eine App")
    logger.info("  Categories:")
    logger.info("    • create_category - Erstellt eine neue Category")
    logger.info("    • list_categories - Listet alle Categories auf")
    logger.info("    • get_category_details - Holt Category-Details")
    logger.info("    • update_category - Aktualisiert eine Category")
    logger.info("    • delete_category - Löscht eine Category")
    logger.info("  Services:")
    logger.info("    • create_service - Erstellt einen neuen Service")
    logger.info("    • list_services - Listet alle Services auf")
    logger.info("    • get_service_details - Holt Service-Details")
    logger.info("    • update_service - Aktualisiert einen Service")
    logger.info("    • delete_service - Löscht einen Service")
    logger.info("  Resources:")
    logger.info("    • create_resource - Erstellt eine neue Resource")
    logger.info("    • list_resources - Listet alle Resources auf")
    logger.info("    • get_resource_details - Holt Resource-Details")
    logger.info("    • update_resource - Aktualisiert eine Resource")
    logger.info("    • delete_resource - Löscht eine Resource")
    
    logger.info("🏷️  Attribute Management:")
    logger.info("    • list_attributes - Listet Attribute einer Resource")
    logger.info("    • get_attribute_details - Holt Attribut-Details") 
    logger.info("    • create_attribute - Erstellt ein neues Attribut")
    logger.info("    • update_attribute - Aktualisiert ein Attribut")
    logger.info("    • delete_attribute - Löscht ein Attribut")
    logger.info("    • create_attributes_bulk - Erstellt mehrere Attribute gleichzeitig")
    
    logger.info("📊 Generics API (Resource Data):")
    logger.info("    • list_generic_entries - Listet Einträge einer Resource auf (echte Daten) mit Aggregationen und Search")
    logger.info("    • create_generic_entry - Erstellt einen neuen Eintrag in einer Resource")
    logger.info("    • get_generic_entry - Holt einen spezifischen Eintrag aus einer Resource")
    logger.info("    • update_generic_entry - Aktualisiert einen Eintrag in einer Resource (PATCH)")
    logger.info("    • delete_generic_entry - Löscht einen Eintrag aus einer Resource")
    
    # Server starten
    mcp.run()


# ===== ATTRIBUTE MANAGEMENT TOOLS =====

@mcp.tool()
async def list_attributes(resource_name: str, search: str = "", page_size: int = 50, page: int = 1) -> Dict[str, Any]:
    """
    Listet alle Attribute einer Resource auf.
    
    Args:
        resource_name: Name der Resource für die Attribute aufgelistet werden sollen
        search: Optionaler Suchbegriff für Attribut-Namen oder -Beschreibungen
        page_size: Anzahl der Ergebnisse pro Seite (Standard: 50)
        page: Seitennummer für Pagination (Standard: 1)
    
    Returns:
        Liste der gefundenen Attribute mit Pagination-Informationen
    """
    try:
        client = await get_api_client()
        result = await client.list_attributes(
            resource_name=resource_name,
            search=search if search else None,
            page_size=page_size,
            page=page
        )
        
        attributes = []
        # Attribute API gibt direkt eine Liste zurück, nicht ein Dict mit results
        if isinstance(result, list):
            for attr in result:
                attributes.append({
                    "object_id": attr.get("object_id"),
                    "name": attr.get("name"),
                    "type": attr.get("type"),
                    "label": attr.get("label"),
                    "description": attr.get("description", ""),
                    "required": attr.get("required", False),
                    "readonly": attr.get("readonly", False),
                    "unique": attr.get("unique", False),
                    "show_in_table": attr.get("show_in_table", True),
                    "enable_sum": attr.get("enable_sum", False),
                    "field_order": attr.get("field_order"),
                    "form_layout_location": attr.get("form_layout_location", "Main"),
                    "form_layout_col": attr.get("form_layout_col", "12"),
                    "resource": attr.get("resource", {})
                })
        elif isinstance(result, dict) and "results" in result:
            # Fallback für Standard-Pagination-Format
            for attr in result["results"]:
                attributes.append({
                    "object_id": attr.get("object_id"),
                    "name": attr.get("name"),
                    "type": attr.get("type"),
                    "label": attr.get("label"),
                    "description": attr.get("description", ""),
                    "required": attr.get("required", False),
                    "readonly": attr.get("readonly", False),
                    "unique": attr.get("unique", False),
                    "show_in_table": attr.get("show_in_table", True),
                    "enable_sum": attr.get("enable_sum", False),
                    "field_order": attr.get("field_order"),
                    "form_layout_location": attr.get("form_layout_location", "Main"),
                    "form_layout_col": attr.get("form_layout_col", "12"),
                    "resource": attr.get("resource", {})
                })
        
        return {
            "success": True,
            "count": len(attributes),
            "next": result.get("next") if isinstance(result, dict) else None,
            "previous": result.get("previous") if isinstance(result, dict) else None,
            "attributes": attributes,
            "message": f"Gefundene Attribute für Resource '{resource_name}': {len(attributes)}"
        }
        
    except Exception as e:
        logger.error(f"Fehler beim Auflisten der Attribute: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Auflisten der Attribute für Resource '{resource_name}'"
        }

@mcp.tool()
async def get_attribute_details(resource_name: str, attribute_id: str) -> Dict[str, Any]:
    """
    Holt detaillierte Informationen zu einem Attribut.
    
    Args:
        resource_name: Name der Resource
        attribute_id: UUID des Attributs
    
    Returns:
        Detaillierte Attribut-Informationen
    """
    try:
        client = await get_api_client()
        result = await client.get_attribute_details(resource_name, attribute_id)
        
        return {
            "success": True,
            "attribute": {
                "object_id": result.get("object_id"),
                "name": result.get("name"),
                "type": result.get("type"),
                "label": result.get("label"),
                "description": result.get("description", ""),
                "required": result.get("required", False),
                "readonly": result.get("readonly", False),
                "unique": result.get("unique", False),
                "show_in_table": result.get("show_in_table", True),
                "enable_sum": result.get("enable_sum", False),
                "field_order": result.get("field_order"),
                "form_layout_location": result.get("form_layout_location", "Main"),
                "form_layout_col": result.get("form_layout_col", "12"),
                "resource": result.get("resource", {}),
                "ingest_timestamp": result.get("ingest_timestamp"),
                "update_timestamp": result.get("update_timestamp")
            },
            "message": f"Details für Attribut '{result.get('name')}' erfolgreich abgerufen"
        }
        
    except Exception as e:
        logger.error(f"Fehler beim Abrufen der Attribut-Details: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Abrufen der Details für Attribut ID '{attribute_id}'"
        }

@mcp.tool()
async def create_attribute(
    resource_name: str,
    name: str,
    attribute_type: str,
    label: str,
    description: str = "",
    required: bool = False,
    readonly: bool = False,
    unique: bool = False,
    show_in_table: bool = True,
    enable_sum: bool = False,
    field_order: int = None,
    form_layout_location: str = "Main",
    form_layout_col: str = "12",
    # Typ-spezifische Parameter
    placeholder: str = None,
    max_length: int = None,
    min_length: int = None,
    default_value: str = None,
    mask: str = None,
    input_type: str = "text",
    numeric_datatype: str = "integer",
    min_numeric: float = None,
    max_numeric: float = None,
    is_auto_increment: bool = False,
    number_representation: str = "default",
    default_checked: bool = False,
    true_text: str = "Ja",
    false_text: str = "Nein",
    dropdown_type: str = "string",
    dropdown_options: str = None,
    linked_resource: str = None,
    alt_display_field: str = None,
    hide_child_resource: bool = False,
    date_format: str = "YYYY-MM-DD",
    datetime_input_type: str = "date"
) -> Dict[str, Any]:
    """
    Erstellt ein neues Attribut für eine Resource.
    
    Args:
        resource_name: Name der Resource
        name: Technischer Name des Attributs (nur Buchstaben, Zahlen, Unterstriche)
        attribute_type: Typ des Attributs (INPUT_FIELD, TEXT_FIELD, NUMERIC_FIELD, BOOLEAN_FIELD, SLIDER_FIELD, 
                       DROPDOWN_FIELD, DROPDOWN_MULTI_FIELD, RELATION_FIELD, RELATION_FIELD_MULTI, 
                       TIMESTAMP_FIELD, STATE_FIELD, ICON_SELECT, ACTION, FILE, FILES, IMAGE, INFO, LINK, 
                       MEMBER, MEMBER_MULTI, LIST_FIELD, IFRAME, TIMELINE, RTE, JSON)
        label: Anzeigename des Attributs
        description: Beschreibung des Attributs
        required: Ob das Feld erforderlich ist
        readonly: Ob das Feld nur lesbar ist
        unique: Ob der Wert eindeutig sein muss
        show_in_table: Ob das Feld in Tabellen angezeigt wird
        enable_sum: Ob Summen-Aggregation aktiviert ist (nur für numerische Felder)
        field_order: Reihenfolge der Felder
        form_layout_location: Layout-Bereich im Formular (Main, Meta, Advanced)
        form_layout_col: Spaltenbreite im Formular (1, 2, 3, 4, 6, 12)
        
        # Text-Feld Parameter
        placeholder: Platzhalter-Text für Eingabefelder
        max_length: Maximale Länge für Text-Felder
        min_length: Minimale Länge für Text-Felder
        default_value: Standard-Wert
        mask: Input-Maske für Text-Felder
        input_type: HTML Input-Typ (text, email, password, tel, url, search)
        
        # Numerische Feld Parameter
        numeric_datatype: Datentyp (integer, bigint, decimal, real)
        min_numeric: Minimaler numerischer Wert
        max_numeric: Maximaler numerischer Wert
        is_auto_increment: Ob Auto-Increment aktiviert ist
        number_representation: Darstellung (default, currency, percentage)
        
        # Boolean-Feld Parameter
        default_checked: Standard-Checkbox-Status
        true_text: Text für true-Wert
        false_text: Text für false-Wert
        
        # Dropdown-Parameter
        dropdown_type: Dropdown-Typ (string, number)
        dropdown_options: JSON-String mit Dropdown-Optionen [{"text": "...", "value": "..."}]
        
        # Relation-Parameter
        linked_resource: UUID der verknüpften Resource (für RELATION_FIELD)
        alt_display_field: Alternatives Anzeigefeld
        hide_child_resource: Ob die verknüpfte Resource versteckt werden soll
        
        # Timestamp-Parameter
        date_format: Datumsformat (YYYY-MM-DD, DD.MM.YYYY, MM/DD/YYYY, ISO)
        datetime_input_type: Input-Typ (date, datetime-local, time)
    
    Returns:
        Erstelltes Attribut mit Details
    """
    try:
        client = await get_api_client()
        
        # Basis-Parameter zusammenstellen
        kwargs = {}
        
        # Text-Feld Parameter
        if attribute_type in ["INPUT_FIELD", "TEXT_FIELD"]:
            if placeholder:
                kwargs["placeholder"] = placeholder
            if max_length:
                kwargs["maxLength"] = max_length
            if min_length:
                kwargs["minLength"] = min_length
            if default_value:
                kwargs["default_value"] = default_value
            if mask:
                kwargs["mask"] = mask
            if input_type != "text":
                kwargs["input_type"] = input_type
                
        # Numerische Parameter
        elif attribute_type == "NUMERIC_FIELD":
            if numeric_datatype != "integer":
                kwargs["numeric_datatype"] = numeric_datatype
            if min_numeric is not None:
                kwargs["minNumeric"] = min_numeric
            if max_numeric is not None:
                kwargs["maxNumeric"] = max_numeric
            if default_value:
                kwargs["default_value"] = default_value
            if is_auto_increment:
                kwargs["is_auto_increment"] = is_auto_increment
            if number_representation != "default":
                kwargs["number_representation"] = number_representation
                
        # Boolean Parameter
        elif attribute_type == "BOOLEAN_FIELD":
            if default_checked:
                kwargs["default_checked"] = default_checked
            if true_text != "Ja":
                kwargs["true_text"] = true_text
            if false_text != "Nein":
                kwargs["false_text"] = false_text
                
        # Dropdown Parameter
        elif attribute_type in ["DROPDOWN_FIELD", "DROPDOWN_MULTI_FIELD"]:
            if dropdown_type != "string":
                kwargs["dropdown_type"] = dropdown_type
            if dropdown_options:
                import json
                try:
                    options = json.loads(dropdown_options)
                    if dropdown_type == "string":
                        kwargs["dropdown_options_string"] = options
                    else:
                        kwargs["dropdown_options_number"] = options
                except json.JSONDecodeError:
                    return {
                        "success": False,
                        "error": "Ungültiges JSON-Format für dropdown_options",
                        "message": f"Fehler beim Parsen der Dropdown-Optionen"
                    }
                    
        # Relation Parameter
        elif attribute_type in ["RELATION_FIELD", "RELATION_FIELD_MULTI"]:
            if not linked_resource:
                return {
                    "success": False,
                    "error": "linked_resource ist erforderlich für RELATION_FIELD",
                    "message": f"Verknüpfte Resource muss angegeben werden"
                }
            kwargs["linked_resource"] = linked_resource
            if alt_display_field:
                kwargs["alt_display_field"] = alt_display_field
            if hide_child_resource:
                kwargs["hide_child_resource"] = hide_child_resource
                
        # Timestamp Parameter
        elif attribute_type == "TIMESTAMP_FIELD":
            if date_format != "YYYY-MM-DD":
                kwargs["date_format"] = date_format
            if datetime_input_type != "date":
                kwargs["input_type"] = datetime_input_type
        
        result = await client.create_attribute(
            resource_name=resource_name,
            name=name,
            attribute_type=attribute_type,
            label=label,
            description=description,
            required=required,
            readonly=readonly,
            unique=unique,
            show_in_table=show_in_table,
            enable_sum=enable_sum,
            field_order=field_order,
            form_layout_location=form_layout_location,
            form_layout_col=form_layout_col,
            **kwargs
        )
        
        return {
            "success": True,
            "message": f"Attribut '{name}' für Resource '{resource_name}' erfolgreich erstellt",
            "attribute": {
                "object_id": result.get("object_id"),
                "name": result.get("name"),
                "type": result.get("type"),
                "label": result.get("label"),
                "description": result.get("description"),
                "required": result.get("required"),
                "readonly": result.get("readonly"),
                "unique": result.get("unique"),
                "show_in_table": result.get("show_in_table"),
                "enable_sum": result.get("enable_sum"),
                "field_order": result.get("field_order"),
                "form_layout_location": result.get("form_layout_location"),
                "form_layout_col": result.get("form_layout_col"),
                "resource": result.get("resource", {}),
                "ingest_timestamp": result.get("ingest_timestamp"),
                "update_timestamp": result.get("update_timestamp")
            }
        }
        
    except Exception as e:
        logger.error(f"Fehler beim Erstellen des Attributs: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Erstellen des Attributs '{name}' für Resource '{resource_name}'"
        }

@mcp.tool()
async def update_attribute(
    resource_name: str,
    attribute_id: str,
    name: str = None,
    label: str = None,
    description: str = None,
    required: bool = None,
    readonly: bool = None,
    unique: bool = None,
    show_in_table: bool = None,
    enable_sum: bool = None,
    field_order: int = None,
    form_layout_location: str = None,
    form_layout_col: str = None
) -> Dict[str, Any]:
    """
    Aktualisiert ein bestehendes Attribut.
    
    Args:
        resource_name: Name der Resource
        attribute_id: UUID des zu aktualisierenden Attributs
        name: Neuer technischer Name (optional)
        label: Neuer Anzeigename (optional)
        description: Neue Beschreibung (optional)
        required: Neuer required-Status (optional)
        readonly: Neuer readonly-Status (optional) 
        unique: Neuer unique-Status (optional)
        show_in_table: Neuer show_in_table-Status (optional)
        enable_sum: Neuer enable_sum-Status (optional)
        field_order: Neue Reihenfolge (optional)
        form_layout_location: Neuer Layout-Bereich (optional)
        form_layout_col: Neue Spaltenbreite (optional)
    
    Returns:
        Aktualisiertes Attribut mit Details
    """
    try:
        client = await get_api_client()
        result = await client.update_attribute(
            resource_name=resource_name,
            attribute_id=attribute_id,
            name=name,
            label=label,
            description=description,
            required=required,
            readonly=readonly,
            unique=unique,
            show_in_table=show_in_table,
            enable_sum=enable_sum,
            field_order=field_order,
            form_layout_location=form_layout_location,
            form_layout_col=form_layout_col
        )
        
        return {
            "success": True,
            "message": f"Attribut '{result.get('name')}' erfolgreich aktualisiert",
            "attribute": {
                "object_id": result.get("object_id"),
                "name": result.get("name"),
                "type": result.get("type"),
                "label": result.get("label"),
                "description": result.get("description"),
                "required": result.get("required"),
                "readonly": result.get("readonly"),
                "unique": result.get("unique"),
                "show_in_table": result.get("show_in_table"),
                "enable_sum": result.get("enable_sum"),
                "field_order": result.get("field_order"),
                "form_layout_location": result.get("form_layout_location"),
                "form_layout_col": result.get("form_layout_col"),
                "resource": result.get("resource", {}),
                "ingest_timestamp": result.get("ingest_timestamp"),
                "update_timestamp": result.get("update_timestamp")
            }
        }
        
    except Exception as e:
        logger.error(f"Fehler beim Aktualisieren des Attributs: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Aktualisieren des Attributs ID '{attribute_id}'"
        }

@mcp.tool()
async def delete_attribute(resource_name: str, attribute_id: str) -> Dict[str, Any]:
    """
    Löscht ein Attribut aus einer Resource.
    
    Args:
        resource_name: Name der Resource
        attribute_id: UUID des zu löschenden Attributs
    
    Returns:
        Bestätigung der Löschung
    """
    try:
        client = await get_api_client()
        success = await client.delete_attribute(resource_name, attribute_id)
        
        if success:
            return {
                "success": True,
                "message": f"Attribut ID '{attribute_id}' erfolgreich aus Resource '{resource_name}' gelöscht"
            }
        else:
            return {
                "success": False,
                "message": f"Fehler beim Löschen des Attributs ID '{attribute_id}'"
            }
        
    except Exception as e:
        logger.error(f"Fehler beim Löschen des Attributs: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Löschen des Attributs ID '{attribute_id}' aus Resource '{resource_name}'"
        }

@mcp.tool()
async def create_attributes_bulk(resource_name: str, attributes_json: str) -> Dict[str, Any]:
    """
    Erstellt mehrere Attribute gleichzeitig für eine Resource.
    
    Args:
        resource_name: Name der Resource
        attributes_json: JSON-String mit Liste von Attribut-Definitionen
                        Format: [{"name": "...", "type": "...", "label": "...", ...}, ...]
    
    Returns:
        Liste der erstellten Attribute
    """
    try:
        import json
        
        # JSON parsen
        try:
            attributes = json.loads(attributes_json)
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Ungültiges JSON-Format: {e}",
                "message": "Fehler beim Parsen der Attribut-Definitionen"
            }
        
        if not isinstance(attributes, list):
            return {
                "success": False,
                "error": "Attribute müssen als Liste angegeben werden",
                "message": "Ungültiges Format für Attribut-Definitionen"
            }
        
        client = await get_api_client()
        result = await client.create_attributes_bulk(resource_name, attributes)
        
        return {
            "success": True,
            "message": f"{len(result)} Attribute für Resource '{resource_name}' erfolgreich erstellt",
            "attributes": result
        }
        
    except Exception as e:
        logger.error(f"Fehler beim Bulk-Erstellen der Attribute: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Bulk-Erstellen der Attribute für Resource '{resource_name}'"
        }

# =====================================
# Generics API (Resource Data)
# =====================================

@mcp.tool()
async def list_generic_entries(
    resource_name: str,
    search: str = "",
    page_size: int = 20,
    page: int = 1,
    ordering: str = "",
    filters_json: str = "{}",
    directus_filter_json: str = "",
    aggregate_json: str = ""
) -> Dict[str, Any]:
    """
    Listet Einträge einer Resource auf (echte Daten aus den Tabellen) mit Aggregationen.
    
    Args:
        resource_name: Name der Resource (Tabellenname, z.B. 'lau6_RunEntries')
        search: Suchbegriff für Textfelder (Volltext-Suche in allen Feldern)
        page_size: Anzahl Einträge pro Seite (Standard: 20)
        page: Seitennummer, 1-basiert (Standard: 1)
        ordering: Sortierung (z.B. "name", "-date_created" für absteigende Sortierung)
        filters_json: JSON-String mit einfachen Filtern (Legacy, für Rückwärtskompatibilität)
        directus_filter_json: JSON-String mit Directus-ähnlichen Filtern (empfohlen)
        aggregate_json: JSON-String mit Aggregation-Parametern
    
    Returns:
        Strukturierte Antwort mit count, next, previous, results und aggregations
        Bei Aggregationen: results enthält aggregierte Werte statt Rohdaten
        
    Beispiele für einfache Filter (filters_json):
        '{"training_type": "dauerlauf"}'
        
    Beispiele für Directus-Filter (directus_filter_json):
        '{"state": {"_eq": "ok"}}'                                    # Gleichheit
        '{"amount": {"_gte": 10}}'                                    # Größer gleich
        '{"name": {"_contains": "Canva"}}'                            # Enthält Text
        '{"date_created": {"_between": ["2025-01-01", "2025-12-31"]}}' # Zwischen Daten
        '{"state": {"_in": ["ok", "pending"]}}'                       # In Liste
        '{"_and": [{"state": {"_eq": "ok"}}, {"amount": {"_gte": 10}}]}' # UND-Verknüpfung
        '{"_or": [{"state": {"_eq": "ok"}}, {"state": {"_eq": "pending"}}]}' # ODER-Verknüpfung
        
    Beispiele für Aggregationen (aggregate_json):
        '{"sum": "amount"}'                                           # Summe aller amount-Werte
        '{"count": "amount"}'                                         # Anzahl nicht-null amount-Werte
        '{"avg": "amount"}'                                           # Durchschnitt aller amount-Werte
        '{"min": "amount"}'                                           # Minimum der amount-Werte
        '{"max": "amount"}'                                           # Maximum der amount-Werte
        '{"sum": "distance_km", "count": "name"}'                     # Mehrere Aggregationen gleichzeitig
        
    Beispiele für Search-Parameter:
        search="Marathon"        # Findet alle Einträge, die "Marathon" in beliebigen Textfeldern enthalten
        search="Dauerlauf"       # Findet alle Einträge mit "Dauerlauf" in Namen, Beschreibungen, Notizen
        search="10km"            # Findet alle Einträge, die "10km" enthalten
        
    Verfügbare Directus-Operatoren:
        _eq: Gleichheit, _neq: Ungleichheit, _gt: Größer, _gte: Größer gleich
        _lt: Kleiner, _lte: Kleiner gleich, _in: In Liste, _nin: Nicht in Liste
        _contains: Enthält, _ncontains: Enthält nicht, _starts_with: Beginnt mit
        _nstarts_with: Beginnt nicht mit, _ends_with: Endet mit, _nends_with: Endet nicht mit
        _between: Zwischen, _nbetween: Nicht zwischen, _null: Ist null, _nnull: Ist nicht null
        _empty: Ist leer, _nempty: Ist nicht leer
        
    Logische Operatoren:
        _and: UND-Verknüpfung, _or: ODER-Verknüpfung
        
    Verfügbare Aggregations-Funktionen:
        sum: Summe aller Werte (nur für numerische Felder)
        count: Anzahl nicht-null Werte 
        avg: Durchschnitt aller Werte (nur für numerische Felder)
        min: Minimum der Werte
        max: Maximum der Werte
    """
    try:
        import json
        
        # Filter JSON parsen
        filters = {}
        directus_filter = {}
        aggregate = {}
        
        # Legacy einfache Filter
        if filters_json and filters_json != "{}":
            try:
                filters = json.loads(filters_json)
            except json.JSONDecodeError as e:
                return {
                    "success": False,
                    "error": f"Ungültiges JSON-Format für einfache Filter: {e}",
                    "message": "Fehler beim Parsen der Filter-Parameter"
                }
        
        # Directus-ähnliche Filter (bevorzugt)
        if directus_filter_json:
            try:
                directus_filter = json.loads(directus_filter_json)
            except json.JSONDecodeError as e:
                return {
                    "success": False,
                    "error": f"Ungültiges JSON-Format für Directus-Filter: {e}",
                    "message": "Fehler beim Parsen der Directus-Filter-Parameter"
                }
        
        # Aggregation-Parameter parsen
        if aggregate_json:
            try:
                aggregate = json.loads(aggregate_json)
            except json.JSONDecodeError as e:
                return {
                    "success": False,
                    "error": f"Ungültiges JSON-Format für Aggregations-Parameter: {e}",
                    "message": "Fehler beim Parsen der Aggregations-Parameter"
                }
        
        client = await get_api_client()
        result = await client.list_generic_entries(
            resource_name=resource_name,
            search=search if search else None,
            page_size=page_size if page_size > 0 else None,
            page=page if page > 0 else None,
            ordering=ordering if ordering else None,
            filters=filters if filters else None,
            directus_filter=directus_filter if directus_filter else None,
            aggregate=aggregate if aggregate else None
        )
        
        return {
            "success": True,
            "message": f"Einträge für Resource '{resource_name}' erfolgreich abgerufen",
            "data": {
                "count": result.get("count", 0),
                "total_pages": (result.get("count", 0) + page_size - 1) // page_size if page_size > 0 else 1,
                "current_page": page,
                "page_size": page_size,
                "has_next": result.get("next") is not None,
                "has_previous": result.get("previous") is not None,
                "next_url": result.get("next"),
                "previous_url": result.get("previous"),
                "aggregations": result.get("aggregations", []),
                "results": result.get("results", [])
            },
            "resource_name": resource_name,
            "search_term": search,
            "ordering": ordering,
            "simple_filters": filters,
            "directus_filters": directus_filter,
            "aggregations": aggregate
        }
        
    except Exception as e:
        logger.error(f"Fehler beim Abrufen der Generic Entries für '{resource_name}': {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Abrufen der Einträge für Resource '{resource_name}'"
        }
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Abrufen der Einträge für Resource '{resource_name}'"
        }

@mcp.tool()
async def create_generic_entry(
    resource_name: str,
    entry_data_json: str
) -> Dict[str, Any]:
    """
    Erstellt einen neuen Eintrag in einer Resource (echte Daten in Tabellen).
    
    Args:
        resource_name: Name der Resource (Tabellenname, z.B. 'lau6_RunEntries')
        entry_data_json: JSON-String mit den Daten für den neuen Eintrag
    
    Returns:
        Strukturierte Antwort mit dem erstellten Eintrag
        
    Beispiele für entry_data_json:
        '{"name": "Morgenlauf", "distance_km": 5.2, "training_type": "dauerlauf"}'
        '{"name": "Canva Pro", "amount": 27.50, "state": "ok", "from": "canva.com"}'
        '{"product_name": "Laptop", "is_available": true, "priority": "high"}'
        
    Automatische Felder (werden vom System gesetzt):
        - object_id: Eindeutige UUID für den Eintrag
        - date_created: Zeitstempel der Erstellung
        - date_updated: Zeitstempel der letzten Änderung
        - subscription: Verknüpfung zum Dimetrics-Account
        
    Pflichtfelder (je nach Resource):
        - name: Name/Titel des Eintrags (meist erforderlich)
        - state: Status des Eintrags (falls vorhanden, z.B. "active", "ok", "pending")
    """
    try:
        import json
        
        # Entry-Daten JSON parsen
        try:
            entry_data = json.loads(entry_data_json)
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Ungültiges JSON-Format für Entry-Daten: {e}",
                "message": "Fehler beim Parsen der Entry-Daten-Parameter"
            }
        
        client = await get_api_client()
        result = await client.create_generic_entry(
            resource_name=resource_name,
            data=entry_data
        )
        
        return {
            "success": True,
            "message": f"Eintrag in Resource '{resource_name}' erfolgreich erstellt",
            "entry": result,
            "resource_name": resource_name,
            "created_id": result.get("object_id"),
            "entry_data": entry_data
        }
        
    except Exception as e:
        logger.error(f"Fehler beim Erstellen des Generic Entry für '{resource_name}': {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Erstellen des Eintrags für Resource '{resource_name}'"
        }

@mcp.tool()
async def get_generic_entry(
    resource_name: str,
    entry_id: str
) -> Dict[str, Any]:
    """
    Holt einen spezifischen Eintrag aus einer Resource (echte Daten).
    
    Args:
        resource_name: Name der Resource (Tabellenname, z.B. 'lau6_RunEntries')
        entry_id: object_id des Eintrags (UUID)
    
    Returns:
        Strukturierte Antwort mit den detaillierten Eintragsdaten
        
    Beispiele:
        resource_name="lau6_RunEntries", entry_id="a1b2c3d4-e5f6-7890-abcd-ef1234567890"
        resource_name="n8n_collection", entry_id="c89515a4-13f3-4d7e-b4a5-249b5b4e8368"
        
    Rückgabedaten enthalten:
        - Alle Attribute-Werte des Eintrags
        - Metadaten: object_id, date_created, date_updated, subscription
        - Relation-Fields: Verknüpfte Objekte (vendor, etc.)
    """
    try:
        client = await get_api_client()
        result = await client.get_generic_entry(
            resource_name=resource_name,
            entry_id=entry_id
        )
        
        return {
            "success": True,
            "message": f"Eintrag '{entry_id}' aus Resource '{resource_name}' erfolgreich abgerufen",
            "entry": result,
            "resource_name": resource_name,
            "entry_id": entry_id
        }
        
    except Exception as e:
        logger.error(f"Fehler beim Abrufen des Generic Entry '{entry_id}' für '{resource_name}': {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Abrufen des Eintrags '{entry_id}' für Resource '{resource_name}'"
        }

@mcp.tool()
async def update_generic_entry(
    resource_name: str,
    entry_id: str,
    update_data_json: str
) -> Dict[str, Any]:
    """
    Aktualisiert einen Eintrag in einer Resource (PATCH - nur veränderte Felder).
    
    Args:
        resource_name: Name der Resource (Tabellenname, z.B. 'lau6_RunEntries')
        entry_id: object_id des zu aktualisierenden Eintrags (UUID)
        update_data_json: JSON-String mit den zu ändernden Daten
    
    Returns:
        Strukturierte Antwort mit dem aktualisierten Eintrag
        
    Beispiele für update_data_json:
        '{"distance_km": 6.8, "notes": "Sehr guter Lauf!"}'
        '{"state": "completed", "amount": 29.99}'
        '{"priority": "urgent", "is_available": false}'
        
    PATCH-Verhalten:
        - Nur angegebene Felder werden geändert
        - Andere Felder bleiben unverändert
        - date_updated wird automatisch aktualisiert
        - object_id und date_created bleiben unverändert
        
    Häufige Update-Szenarien:
        - Status ändern: '{"state": "completed"}'
        - Werte korrigieren: '{"distance_km": 5.5, "pace_min_per_km": 5.2}'
        - Notizen hinzufügen: '{"notes": "Toller Lauf bei perfektem Wetter"}'
        - Verfügbarkeit ändern: '{"is_available": true}'
    """
    try:
        import json
        
        # Update-Daten JSON parsen
        try:
            update_data = json.loads(update_data_json)
        except json.JSONDecodeError as e:
            return {
                "success": False,
                "error": f"Ungültiges JSON-Format für Update-Daten: {e}",
                "message": "Fehler beim Parsen der Update-Daten-Parameter"
            }
        
        client = await get_api_client()
        result = await client.update_generic_entry(
            resource_name=resource_name,
            entry_id=entry_id,
            data=update_data
        )
        
        return {
            "success": True,
            "message": f"Eintrag '{entry_id}' in Resource '{resource_name}' erfolgreich aktualisiert",
            "entry": result,
            "resource_name": resource_name,
            "entry_id": entry_id,
            "updated_fields": list(update_data.keys()),
            "update_data": update_data
        }
        
    except Exception as e:
        logger.error(f"Fehler beim Aktualisieren des Generic Entry '{entry_id}' für '{resource_name}': {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Aktualisieren des Eintrags '{entry_id}' für Resource '{resource_name}'"
        }

@mcp.tool()
async def delete_generic_entry(
    resource_name: str,
    entry_id: str,
    confirm_deletion: bool = False
) -> Dict[str, Any]:
    """
    Löscht einen Eintrag aus einer Resource (VORSICHT: Unwiderruflich!).
    
    Args:
        resource_name: Name der Resource (Tabellenname, z.B. 'lau6_RunEntries')
        entry_id: object_id des zu löschenden Eintrags (UUID)
        confirm_deletion: Bestätigung für die Löschung (MUSS True sein)
    
    Returns:
        Strukturierte Antwort mit Lösch-Bestätigung
        
    ⚠️  WARNUNG: Diese Aktion ist UNWIDERRUFLICH!
        - Der Eintrag wird permanent aus der Datenbank entfernt
        - Alle Daten des Eintrags gehen verloren
        - Verknüpfungen zu anderen Objekten werden gelöscht
        
    Sicherheits-Check:
        - confirm_deletion MUSS auf True gesetzt werden
        - Ohne Bestätigung wird die Löschung abgebrochen
        
    Beispiele:
        resource_name="lau6_RunEntries", entry_id="...", confirm_deletion=True
        resource_name="n8n_collection", entry_id="...", confirm_deletion=True
        
    Empfehlung:
        - Vorher mit get_generic_entry() die Daten überprüfen
        - Bei wichtigen Daten: Backup/Export vor Löschung
        - Für Tests: Nur Test-Einträge löschen, niemals produktive Daten
    """
    try:
        # Sicherheits-Check
        if not confirm_deletion:
            return {
                "success": False,
                "error": "Löschung nicht bestätigt",
                "message": "Setzen Sie confirm_deletion=True zur Bestätigung der Löschung",
                "warning": "Diese Aktion ist unwiderruflich! Überprüfen Sie die Daten vorher."
            }
        
        client = await get_api_client()
        result = await client.delete_generic_entry(
            resource_name=resource_name,
            entry_id=entry_id
        )
        
        return {
            "success": True,
            "message": f"Eintrag '{entry_id}' aus Resource '{resource_name}' erfolgreich gelöscht",
            "deletion_result": result,
            "resource_name": resource_name,
            "deleted_entry_id": entry_id,
            "warning": "Löschung war erfolgreich und unwiderruflich."
        }
        
    except Exception as e:
        logger.error(f"Fehler beim Löschen des Generic Entry '{entry_id}' für '{resource_name}': {e}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Fehler beim Löschen des Eintrags '{entry_id}' für Resource '{resource_name}'"
        }

if __name__ == "__main__":
    import sys
    
    def main():
        """Hauptfunktion zum Starten des MCP Servers."""
        # Überprüfe, ob HTTP-Transport gewünscht ist (für Container)
        if os.getenv("MCP_TRANSPORT") == "http" or os.getenv("PORT"):
            # SSE-Transport für Container (nicht Streamable HTTP)
            logger.info(f"Starte MCP Server im SSE-Modus für Container")
            # Konfiguriere Host für Container-Nutzung
            if hasattr(mcp, 'settings'):
                mcp.settings.host = "0.0.0.0"
                mcp.settings.port = int(os.getenv("PORT", 8000))
            mcp.run(transport="sse")
        else:
            # Standard stdio-Transport für lokale Entwicklung
            logger.info("Starte MCP Server im stdio-Modus")
            mcp.run()
    
    main()
