"""
MCP Tools für die Dimetrics API Integration.
"""

import json
import logging
from typing import Any, Dict, List, Optional

import mcp.types as types
from mcp.server import Server

from .api_client import DimetricsAPIClient

logger = logging.getLogger(__name__)

def register_tools(server: Server, api_client: DimetricsAPIClient):
    """Registriert alle MCP Tools für den Dimetrics API Client."""
    
    # Service (App) Management Tools
    @server.call_tool()
    async def create_app(arguments: dict) -> list[types.TextContent]:
        """
        Erstellt eine neue App (Service) in der Dimetrics Plattform.
        
        Args:
            name (str): Name der App
            description (str, optional): Beschreibung der App
        """
        try:
            name = arguments.get("name")
            description = arguments.get("description", "")
            
            if not name:
                return [types.TextContent(
                    type="text",
                    text="Fehler: App-Name ist erforderlich."
                )]
            
            result = await api_client.create_service(name, description)
            
            return [types.TextContent(
                type="text",
                text=f"App '{name}' erfolgreich erstellt. ID: {result.get('id', 'N/A')}"
            )]
            
        except Exception as e:
            logger.error(f"Fehler beim Erstellen der App: {e}")
            return [types.TextContent(
                type="text",
                text=f"Fehler beim Erstellen der App: {str(e)}"
            )]
    
    @server.call_tool()
    async def list_apps(arguments: dict) -> list[types.TextContent]:
        """
        Listet alle verfügbaren Apps (Services) auf.
        """
        try:
            services = await api_client.list_services()
            
            if not services:
                return [types.TextContent(
                    type="text",
                    text="Keine Apps gefunden."
                )]
            
            app_list = "\n".join([
                f"- {service.get('name', 'Unbekannt')} (ID: {service.get('id', 'N/A')}): {service.get('description', 'Keine Beschreibung')}"
                for service in services
            ])
            
            return [types.TextContent(
                type="text",
                text=f"Verfügbare Apps:\n{app_list}"
            )]
            
        except Exception as e:
            logger.error(f"Fehler beim Auflisten der Apps: {e}")
            return [types.TextContent(
                type="text",
                text=f"Fehler beim Auflisten der Apps: {str(e)}"
            )]
    
    @server.call_tool()
    async def delete_app(arguments: dict) -> list[types.TextContent]:
        """
        Löscht eine App (Service).
        
        Args:
            app_id (str): ID der zu löschenden App
        """
        try:
            app_id = arguments.get("app_id")
            
            if not app_id:
                return [types.TextContent(
                    type="text",
                    text="Fehler: App-ID ist erforderlich."
                )]
            
            await api_client.delete_service(app_id)
            
            return [types.TextContent(
                type="text",
                text=f"App mit ID '{app_id}' erfolgreich gelöscht."
            )]
            
        except Exception as e:
            logger.error(f"Fehler beim Löschen der App: {e}")
            return [types.TextContent(
                type="text",
                text=f"Fehler beim Löschen der App: {str(e)}"
            )]
    
    # Table Management Tools
    @server.call_tool()
    async def create_table(arguments: dict) -> list[types.TextContent]:
        """
        Erstellt eine neue Tabelle in einer App.
        
        Args:
            app_id (str): ID der App
            name (str): Name der Tabelle
            description (str, optional): Beschreibung der Tabelle
        """
        try:
            app_id = arguments.get("app_id")
            name = arguments.get("name")
            description = arguments.get("description", "")
            
            if not app_id or not name:
                return [types.TextContent(
                    type="text",
                    text="Fehler: App-ID und Tabellenname sind erforderlich."
                )]
            
            result = await api_client.create_table(app_id, name, description)
            
            return [types.TextContent(
                type="text",
                text=f"Tabelle '{name}' erfolgreich in App '{app_id}' erstellt. Tabellen-ID: {result.get('id', 'N/A')}"
            )]
            
        except Exception as e:
            logger.error(f"Fehler beim Erstellen der Tabelle: {e}")
            return [types.TextContent(
                type="text",
                text=f"Fehler beim Erstellen der Tabelle: {str(e)}"
            )]
    
    @server.call_tool()
    async def list_tables(arguments: dict) -> list[types.TextContent]:
        """
        Listet alle Tabellen auf (optional für eine bestimmte App).
        
        Args:
            app_id (str, optional): ID der App (wenn nicht angegeben, werden alle Tabellen aufgelistet)
        """
        try:
            app_id = arguments.get("app_id")
            tables = await api_client.list_tables(app_id)
            
            if not tables:
                return [types.TextContent(
                    type="text",
                    text="Keine Tabellen gefunden."
                )]
            
            table_list = "\n".join([
                f"- {table.get('name', 'Unbekannt')} (ID: {table.get('id', 'N/A')}): {table.get('description', 'Keine Beschreibung')}"
                for table in tables
            ])
            
            return [types.TextContent(
                type="text",
                text=f"Verfügbare Tabellen:\n{table_list}"
            )]
            
        except Exception as e:
            logger.error(f"Fehler beim Auflisten der Tabellen: {e}")
            return [types.TextContent(
                type="text",
                text=f"Fehler beim Auflisten der Tabellen: {str(e)}"
            )]
    
    # Attribute Management Tools
    @server.call_tool()
    async def create_attribute(arguments: dict) -> list[types.TextContent]:
        """
        Erstellt ein neues Attribut für eine Tabelle.
        
        Args:
            table_id (str): ID der Tabelle
            name (str): Name des Attributs
            type (str): Typ des Attributs (input, dropdown, relation, boolean, number, date, etc.)
            required (bool, optional): Ob das Attribut erforderlich ist (Standard: false)
            options (dict, optional): Zusätzliche Optionen für das Attribut
        """
        try:
            table_id = arguments.get("table_id")
            name = arguments.get("name")
            attr_type = arguments.get("type")
            required = arguments.get("required", False)
            options = arguments.get("options", {})
            
            if not table_id or not name or not attr_type:
                return [types.TextContent(
                    type="text",
                    text="Fehler: Tabellen-ID, Attributname und Typ sind erforderlich."
                )]
            
            result = await api_client.create_attribute(
                table_id, name, attr_type, required, options
            )
            
            return [types.TextContent(
                type="text",
                text=f"Attribut '{name}' ({attr_type}) erfolgreich in Tabelle '{table_id}' erstellt. Attribut-ID: {result.get('id', 'N/A')}"
            )]
            
        except Exception as e:
            logger.error(f"Fehler beim Erstellen des Attributs: {e}")
            return [types.TextContent(
                type="text",
                text=f"Fehler beim Erstellen des Attributs: {str(e)}"
            )]
    
    @server.call_tool()
    async def list_attributes(arguments: dict) -> list[types.TextContent]:
        """
        Listet alle Attribute einer Tabelle auf.
        
        Args:
            table_id (str): ID der Tabelle
        """
        try:
            table_id = arguments.get("table_id")
            
            if not table_id:
                return [types.TextContent(
                    type="text",
                    text="Fehler: Tabellen-ID ist erforderlich."
                )]
            
            attributes = await api_client.list_attributes(table_id)
            
            if not attributes:
                return [types.TextContent(
                    type="text",
                    text=f"Keine Attribute in Tabelle '{table_id}' gefunden."
                )]
            
            attr_list = "\n".join([
                f"- {attr.get('name', 'Unbekannt')} ({attr.get('type', 'Unbekannt')}) "
                f"{'[Erforderlich]' if attr.get('required') else '[Optional]'} "
                f"(ID: {attr.get('id', 'N/A')})"
                for attr in attributes
            ])
            
            return [types.TextContent(
                type="text",
                text=f"Attribute in Tabelle '{table_id}':\n{attr_list}"
            )]
            
        except Exception as e:
            logger.error(f"Fehler beim Auflisten der Attribute: {e}")
            return [types.TextContent(
                type="text",
                text=f"Fehler beim Auflisten der Attribute: {str(e)}"
            )]
    
    # Data Management (CRUD) Tools
    @server.call_tool()
    async def create_record(arguments: dict) -> list[types.TextContent]:
        """
        Erstellt einen neuen Datensatz in einer Tabelle.
        
        Args:
            table_id (str): ID der Tabelle
            data (dict): Daten für den neuen Datensatz
        """
        try:
            table_id = arguments.get("table_id")
            data = arguments.get("data")
            
            if not table_id or not data:
                return [types.TextContent(
                    type="text",
                    text="Fehler: Tabellen-ID und Daten sind erforderlich."
                )]
            
            result = await api_client.create_record(table_id, data)
            
            return [types.TextContent(
                type="text",
                text=f"Datensatz erfolgreich in Tabelle '{table_id}' erstellt. Datensatz-ID: {result.get('id', 'N/A')}"
            )]
            
        except Exception as e:
            logger.error(f"Fehler beim Erstellen des Datensatzes: {e}")
            return [types.TextContent(
                type="text",
                text=f"Fehler beim Erstellen des Datensatzes: {str(e)}"
            )]
    
    @server.call_tool()
    async def list_records(arguments: dict) -> list[types.TextContent]:
        """
        Listet Datensätze einer Tabelle auf.
        
        Args:
            table_id (str): ID der Tabelle
            limit (int, optional): Maximale Anzahl der Datensätze
            offset (int, optional): Anzahl der zu überspringenden Datensätze
        """
        try:
            table_id = arguments.get("table_id")
            limit = arguments.get("limit")
            offset = arguments.get("offset")
            
            if not table_id:
                return [types.TextContent(
                    type="text",
                    text="Fehler: Tabellen-ID ist erforderlich."
                )]
            
            records = await api_client.list_records(table_id, limit, offset)
            
            if not records:
                return [types.TextContent(
                    type="text",
                    text=f"Keine Datensätze in Tabelle '{table_id}' gefunden."
                )]
            
            # Formatierte Ausgabe der ersten paar Datensätze
            formatted_records = []
            for i, record in enumerate(records[:5]):  # Nur die ersten 5 anzeigen
                record_info = f"Datensatz {i+1} (ID: {record.get('id', 'N/A')}):"
                for key, value in record.items():
                    if key != 'id':
                        record_info += f"\n  - {key}: {value}"
                formatted_records.append(record_info)
            
            result_text = f"Datensätze in Tabelle '{table_id}' (Anzahl: {len(records)}):\n\n"
            result_text += "\n\n".join(formatted_records)
            
            if len(records) > 5:
                result_text += f"\n\n... und {len(records) - 5} weitere Datensätze."
            
            return [types.TextContent(
                type="text",
                text=result_text
            )]
            
        except Exception as e:
            logger.error(f"Fehler beim Auflisten der Datensätze: {e}")
            return [types.TextContent(
                type="text",
                text=f"Fehler beim Auflisten der Datensätze: {str(e)}"
            )]
    
    @server.call_tool()
    async def update_record(arguments: dict) -> list[types.TextContent]:
        """
        Aktualisiert einen Datensatz.
        
        Args:
            table_id (str): ID der Tabelle
            record_id (str): ID des Datensatzes
            data (dict): Neue Daten für den Datensatz
        """
        try:
            table_id = arguments.get("table_id")
            record_id = arguments.get("record_id")
            data = arguments.get("data")
            
            if not table_id or not record_id or not data:
                return [types.TextContent(
                    type="text",
                    text="Fehler: Tabellen-ID, Datensatz-ID und Daten sind erforderlich."
                )]
            
            result = await api_client.update_record(table_id, record_id, data)
            
            return [types.TextContent(
                type="text",
                text=f"Datensatz '{record_id}' in Tabelle '{table_id}' erfolgreich aktualisiert."
            )]
            
        except Exception as e:
            logger.error(f"Fehler beim Aktualisieren des Datensatzes: {e}")
            return [types.TextContent(
                type="text",
                text=f"Fehler beim Aktualisieren des Datensatzes: {str(e)}"
            )]
    
    @server.call_tool()
    async def delete_record(arguments: dict) -> list[types.TextContent]:
        """
        Löscht einen Datensatz.
        
        Args:
            table_id (str): ID der Tabelle
            record_id (str): ID des Datensatzes
        """
        try:
            table_id = arguments.get("table_id")
            record_id = arguments.get("record_id")
            
            if not table_id or not record_id:
                return [types.TextContent(
                    type="text",
                    text="Fehler: Tabellen-ID und Datensatz-ID sind erforderlich."
                )]
            
            await api_client.delete_record(table_id, record_id)
            
            return [types.TextContent(
                type="text",
                text=f"Datensatz '{record_id}' aus Tabelle '{table_id}' erfolgreich gelöscht."
            )]
            
        except Exception as e:
            logger.error(f"Fehler beim Löschen des Datensatzes: {e}")
            return [types.TextContent(
                type="text",
                text=f"Fehler beim Löschen des Datensatzes: {str(e)}"
            )]
    
    # Utility Tools
    @server.call_tool()
    async def create_complete_app(arguments: dict) -> list[types.TextContent]:
        """
        Erstellt eine komplette App mit Tabellen und Attributen basierend auf einer Beschreibung.
        Dies ist ein High-Level Tool für komplexe App-Erstellung.
        
        Args:
            app_name (str): Name der App
            app_description (str): Beschreibung der App
            tables (list): Liste von Tabellen-Definitionen mit Attributen
                Format: [{"name": "table_name", "description": "...", "attributes": [{"name": "attr_name", "type": "attr_type", "required": bool, "options": {}}]}]
        """
        try:
            app_name = arguments.get("app_name")
            app_description = arguments.get("app_description", "")
            tables_def = arguments.get("tables", [])
            
            if not app_name:
                return [types.TextContent(
                    type="text",
                    text="Fehler: App-Name ist erforderlich."
                )]
            
            # App erstellen
            app_result = await api_client.create_service(app_name, app_description)
            app_id = app_result.get("id")
            
            if not app_id:
                return [types.TextContent(
                    type="text",
                    text="Fehler: App konnte nicht erstellt werden."
                )]
            
            result_messages = [f"App '{app_name}' erfolgreich erstellt (ID: {app_id})"]
            
            # Tabellen und Attribute erstellen
            for table_def in tables_def:
                table_name = table_def.get("name")
                table_desc = table_def.get("description", "")
                attributes = table_def.get("attributes", [])
                
                if not table_name:
                    continue
                
                # Tabelle erstellen
                table_result = await api_client.create_table(app_id, table_name, table_desc)
                table_id = table_result.get("id")
                
                if table_id:
                    result_messages.append(f"  Tabelle '{table_name}' erstellt (ID: {table_id})")
                    
                    # Attribute erstellen
                    for attr in attributes:
                        attr_name = attr.get("name")
                        attr_type = attr.get("type")
                        attr_required = attr.get("required", False)
                        attr_options = attr.get("options", {})
                        
                        if attr_name and attr_type:
                            try:
                                attr_result = await api_client.create_attribute(
                                    table_id, attr_name, attr_type, attr_required, attr_options
                                )
                                result_messages.append(f"    Attribut '{attr_name}' ({attr_type}) erstellt")
                            except Exception as e:
                                result_messages.append(f"    Fehler beim Erstellen von Attribut '{attr_name}': {str(e)}")
                else:
                    result_messages.append(f"  Fehler beim Erstellen der Tabelle '{table_name}'")
            
            return [types.TextContent(
                type="text",
                text="\n".join(result_messages)
            )]
            
        except Exception as e:
            logger.error(f"Fehler beim Erstellen der kompletten App: {e}")
            return [types.TextContent(
                type="text",
                text=f"Fehler beim Erstellen der kompletten App: {str(e)}"
            )]

    # Resource Permission Group Tools
    @server.call_tool()
    async def list_resource_permission_groups(arguments: dict) -> list[types.TextContent]:
        """Listet Resource-Permission-Gruppen mit Pagination."""
        try:
            page = arguments.get("page", 1)
            page_size = arguments.get("page_size", 50)
            filters = arguments.get("filters")

            result = await api_client.list_resource_permission_groups(
                page_size=page_size,
                page=page,
                extra_params=filters or None,
            )

            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        except Exception as exc:
            logger.error("Fehler beim Auflisten der Permission-Gruppen: %s", exc)
            return [types.TextContent(type="text", text=f"Fehler: {exc}")]

    @server.call_tool()
    async def get_resource_permission_group(arguments: dict) -> list[types.TextContent]:
        """Liest Details einer einzelnen Resource-Permission-Gruppe."""
        try:
            group_id = arguments.get("group_id")
            if not group_id:
                return [types.TextContent(type="text", text="Fehler: group_id ist erforderlich.")]

            result = await api_client.get_resource_permission_group(group_id)
            return [types.TextContent(
                type="text",
                text=json.dumps(result, indent=2, ensure_ascii=False)
            )]
        except Exception as exc:
            logger.error("Fehler beim Lesen der Permission-Gruppe: %s", exc)
            return [types.TextContent(type="text", text=f"Fehler: {exc}")]

    @server.call_tool()
    async def create_resource_permission_group(arguments: dict) -> list[types.TextContent]:
        """Erstellt eine neue Resource-Permission-Gruppe."""
        try:
            name = arguments.get("name")
            resource = arguments.get("resource")
            subscription = arguments.get("subscription")

            if not all([name, resource, subscription]):
                return [types.TextContent(
                    type="text",
                    text="Fehler: name, resource und subscription sind erforderlich."
                )]

            permission_flags = {
                "show_resource": arguments.get("show_resource", True),
                "can_create_document": arguments.get("can_create_document", False),
                "can_edit_document": arguments.get("can_edit_document", False),
                "can_delete_document": arguments.get("can_delete_document", False),
                "can_view_all_documents": arguments.get("can_view_all_documents", False),
                "can_edit_resource": arguments.get("can_edit_resource", False),
                "can_delete_resource": arguments.get("can_delete_resource", False),
            }

            payload = await api_client.create_resource_permission_group(
                name=name,
                resource=resource,
                subscription=subscription,
                hidden_attributes=arguments.get("hidden_attributes"),
                custom_filter=arguments.get("custom_filter"),
                extra_fields=arguments.get("extra_fields"),
                **permission_flags,
            )

            return [types.TextContent(
                type="text",
                text=f"Permission-Gruppe '{name}' erstellt:\n" + json.dumps(payload, indent=2, ensure_ascii=False)
            )]
        except Exception as exc:
            logger.error("Fehler beim Erstellen der Permission-Gruppe: %s", exc)
            return [types.TextContent(type="text", text=f"Fehler: {exc}")]

    @server.call_tool()
    async def update_resource_permission_group(arguments: dict) -> list[types.TextContent]:
        """Aktualisiert Felder einer Resource-Permission-Gruppe."""
        try:
            group_id = arguments.get("group_id")
            if not group_id:
                return [types.TextContent(type="text", text="Fehler: group_id ist erforderlich.")]

            update_fields = arguments.get("fields", {})
            if not isinstance(update_fields, dict) or not update_fields:
                return [types.TextContent(type="text", text="Fehler: fields (dict) ist erforderlich.")]

            result = await api_client.update_resource_permission_group(group_id, **update_fields)
            return [types.TextContent(
                type="text",
                text="Permission-Gruppe aktualisiert:\n" + json.dumps(result, indent=2, ensure_ascii=False)
            )]
        except Exception as exc:
            logger.error("Fehler beim Aktualisieren der Permission-Gruppe: %s", exc)
            return [types.TextContent(type="text", text=f"Fehler: {exc}")]
