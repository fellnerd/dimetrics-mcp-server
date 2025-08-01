"""
API Client für die Dimetrics Web-API.
"""

import httpx
import json
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class DimetricsAPIClient:
    """Client für die Dimetrics REST API."""
    
    def __init__(
        self,
        base_url: str,
        api_key: Optional[str] = None,
        session_cookie: Optional[str] = None,
        timeout: int = 30,
        debug: bool = False
    ):
        """
        Initialisiert den API Client.
        
        Args:
            base_url: Basis-URL der API
            api_key: API Key für Authentifizierung
            session_cookie: Session Cookie für Authentifizierung
            timeout: Timeout für HTTP-Requests
            debug: Debug-Modus aktivieren
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.debug = debug
        
        # HTTP Client konfigurieren
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        # Authentifizierung - Dimetrics verwendet "Token" statt "Bearer"
        if api_key:
            headers["Authorization"] = f"Token {api_key}"
        elif session_cookie:
            headers["Cookie"] = session_cookie
        
        self.client = httpx.AsyncClient(
            headers=headers,
            timeout=timeout,
            base_url=self.base_url
        )
    
    # Apps API Methods
    async def create_app(self, name: str, description: str = "", prefix: str = "") -> Dict[str, Any]:
        """
        Erstellt eine neue App in Dimetrics.
        
        Args:
            name: Name der App
            description: Beschreibung der App
            prefix: Prefix für die App (optional, wird automatisch generiert wenn leer)
        
        Returns:
            Erstellte App-Daten
        """
        # Automatische Prefix-Generierung falls leer
        if not prefix:
            import time
            # Dimetrics erlaubt max. 5 Zeichen für Prefix
            # Nehme max. 3 Zeichen vom Namen, 1 Zeichen von der Zeit, 1 Underscore = 5 total
            clean_name = name.lower().replace(" ", "").replace("-", "")
            prefix = clean_name[:3] + str(int(time.time()))[-1] + "_"
            # Sicherheitscheck: Kürze auf max. 5 Zeichen
            if len(prefix) > 5:
                prefix = prefix[:5]
        
        data = {
            "name": name,
            "title": name,  # Dimetrics erwartet sowohl name als auch title
            "prefix": prefix
        }
        
        if description:
            data["description"] = description
        
        if self.debug:
            logger.info(f"Sending data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        response = await self.client.post("/apps/", json=data)
        
        if self.debug:
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")
        
        response.raise_for_status()
        return response.json()
    
    async def create_service_deprecated(self, name: str, description: str = "", prefix: str = "") -> Dict[str, Any]:
        """
        DEPRECATED: Diese Methode war fälschlicherweise für App-Erstellung implementiert.
        Verwende stattdessen create_service_endpoint() für Services oder create_app() für Apps.
        
        Args:
            name: Name der App
            description: Beschreibung der App
            prefix: Prefix für die App (optional, wird automatisch generiert wenn leer)
        
        Returns:
            Erstellte App-Daten
        """
        # Automatische Prefix-Generierung falls leer
        if not prefix:
            import time
            # Dimetrics erlaubt max. 5 Zeichen für Prefix
            # Nehme max. 3 Zeichen vom Namen, 1 Zeichen von der Zeit, 1 Underscore = 5 total
            clean_name = name.lower().replace(" ", "").replace("-", "")
            prefix = clean_name[:3] + str(int(time.time()))[-1] + "_"
            # Sicherheitscheck: Kürze auf max. 5 Zeichen
            if len(prefix) > 5:
                prefix = prefix[:5]
        
        data = {
            "name": name,
            "title": name,  # Dimetrics erwartet sowohl name als auch title
            "prefix": prefix
        }
        
        if description:
            data["description"] = description
        
        if self.debug:
            logger.info(f"Sending data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        response = await self.client.post("/apps/", json=data)
        
        if self.debug:
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")
        
        response.raise_for_status()
        return response.json()
    
    async def list_services(self, search: str = None, page_size: int = None, page: int = None, limit: int = None) -> Dict[str, Any]:
        """
        Listet alle verfügbaren Apps auf.
        
        Args:
            search: Optionaler Suchbegriff
            page_size: Anzahl der Ergebnisse pro Seite
            page: Seitennummer für Pagination
            limit: Maximale Anzahl der Ergebnisse
        
        Returns:
            Apps-Liste mit Pagination-Informationen
        """
        params = {}
        
        if search:
            params["search"] = search
        if page_size:
            params["page_size"] = page_size
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit
        
        response = await self.client.get("/apps/", params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_service(self, app_id: str) -> Dict[str, Any]:
        """
        Holt Details einer spezifischen App.
        
        Args:
            app_id: object_id der App
        
        Returns:
            App-Details
        """
        # Dimetrics erwartet trailing slash für GET detail
        response = await self.client.get(f"/apps/{app_id}/")
        response.raise_for_status()
        return response.json()
    
    async def delete_service(self, app_id: str) -> bool:
        """
        Löscht eine App.
        
        Args:
            app_id: object_id der App
        
        Returns:
            True wenn erfolgreich gelöscht
        """
        # Dimetrics erwartet trailing slash für DELETE
        response = await self.client.delete(f"/apps/{app_id}/")
        response.raise_for_status()
        return True
    
    async def update_app_deprecated(self, app_id: str, name: str = None, description: str = None, prefix: str = None) -> Dict[str, Any]:
        """
        DEPRECATED: Diese Methode war fälschlicherweise als update_service benannt.
        Verwende stattdessen update_app() für Apps oder update_service_endpoint() für Services.
        
        Args:
            app_id: object_id der App
            name: Neuer Name (optional)
            description: Neue Beschreibung (optional)
            prefix: Neuer Prefix (optional)
        
        Returns:
            Aktualisierte App-Daten
        """
        data = {}
        
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if prefix is not None:
            data["prefix"] = prefix
        
        if not data:
            raise ValueError("Mindestens ein Parameter muss angegeben werden")
        
        # Dimetrics erwartet trailing slash für PATCH
        response = await self.client.patch(f"/apps/{app_id}/", json=data)
        response.raise_for_status()
        
        return response.json()
    
    # Categories API Methods
    async def list_categories(self, search: str = None, page_size: int = None, page: int = None, limit: int = None) -> Dict[str, Any]:
        """
        Listet alle verfügbaren Categories auf.
        
        Args:
            search: Optionaler Suchbegriff
            page_size: Anzahl der Ergebnisse pro Seite
            page: Seitennummer für Pagination
            limit: Maximale Anzahl der Ergebnisse
        
        Returns:
            Categories-Liste mit Pagination-Informationen
        """
        params = {}
        
        if search:
            params["search"] = search
        if page_size:
            params["page_size"] = page_size
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit
        
        response = await self.client.get("/categories/", params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_category(self, category_id: str) -> Dict[str, Any]:
        """
        Holt Details einer spezifischen Category.
        
        Args:
            category_id: object_id der Category
        
        Returns:
            Category-Details
        """
        # Dimetrics erwartet trailing slash für GET detail
        response = await self.client.get(f"/categories/{category_id}/")
        response.raise_for_status()
        return response.json()
    
    async def create_category(self, name: str, description: str = "", prefix: str = "") -> Dict[str, Any]:
        """
        Erstellt eine neue Category.
        
        Args:
            name: Name der Category
            description: Beschreibung der Category
            prefix: Prefix für die Category (optional, wird automatisch generiert wenn leer)
        
        Returns:
            Erstellte Category-Daten
        """
        # Automatische Prefix-Generierung falls leer
        if not prefix:
            import time
            # Dimetrics erlaubt max. 5 Zeichen für Prefix
            # Nehme max. 3 Zeichen vom Namen, 1 Zeichen von der Zeit, 1 Underscore = 5 total
            clean_name = name.lower().replace(" ", "").replace("-", "")
            prefix = clean_name[:3] + str(int(time.time()))[-1] + "_"
            # Sicherheitscheck: Kürze auf max. 5 Zeichen
            if len(prefix) > 5:
                prefix = prefix[:5]
        
        data = {
            "name": name,
            "title": name,  # Dimetrics erwartet sowohl name als auch title
            "prefix": prefix
        }
        
        if description:
            data["description"] = description
        
        if self.debug:
            logger.info(f"Sending data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        response = await self.client.post("/categories/", json=data)
        
        if self.debug:
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")
        
        response.raise_for_status()
        return response.json()
    
    async def update_category(self, category_id: str, name: str = None, description: str = None, prefix: str = None) -> Dict[str, Any]:
        """
        Aktualisiert eine Category.
        
        Args:
            category_id: object_id der Category
            name: Neuer Name (optional)
            description: Neue Beschreibung (optional)
            prefix: Neuer Prefix (optional)
        
        Returns:
            Aktualisierte Category-Daten
        """
        data = {}
        
        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if prefix is not None:
            data["prefix"] = prefix
        
        if not data:
            raise ValueError("Mindestens ein Parameter muss angegeben werden")
        
        # Dimetrics erwartet trailing slash für PATCH
        response = await self.client.patch(f"/categories/{category_id}/", json=data)
        response.raise_for_status()
        
        return response.json()
    
    async def delete_category(self, category_id: str) -> bool:
        """
        Löscht eine Category.
        
        Args:
            category_id: object_id der Category
        
        Returns:
            True wenn erfolgreich gelöscht
        """
        # Dimetrics erwartet trailing slash für DELETE
        response = await self.client.delete(f"/categories/{category_id}/")
        response.raise_for_status()
        return True
    
    # Services API Methods
    async def list_services_endpoint(self, search: str = None, page_size: int = None, page: int = None, limit: int = None) -> Dict[str, Any]:
        """
        Listet alle verfügbaren Services auf.
        
        Args:
            search: Optionaler Suchbegriff
            page_size: Anzahl der Ergebnisse pro Seite
            page: Seitennummer für Pagination
            limit: Maximale Anzahl der Ergebnisse
        
        Returns:
            Services-Liste mit Pagination-Informationen
        """
        params = {}
        
        if search:
            params["search"] = search
        if page_size:
            params["page_size"] = page_size
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit
        
        response = await self.client.get("/services/", params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_service_endpoint(self, service_id: str) -> Dict[str, Any]:
        """
        Holt Details eines spezifischen Services.
        
        Args:
            service_id: object_id des Services
        
        Returns:
            Service-Details
        """
        # Dimetrics erwartet trailing slash für GET detail
        response = await self.client.get(f"/services/{service_id}/")
        response.raise_for_status()
        return response.json()
    
    async def create_service_endpoint(
        self, 
        name: str, 
        app_space: str, 
        title: str = None,
        description: str = "", 
        category: str = None,
        icon: str = "DataBarHorizontal24Regular",
        order: int = 0,
        hidden: bool = False,
        isFavorite: bool = False
    ) -> Dict[str, Any]:
        """
        Erstellt einen neuen Service.
        
        Args:
            name: Name des Services (unique identifier)
            app_space: object_id der App zu der der Service gehört (Pflichtfeld)
            title: Anzeigename des Services (optional, default = name)
            description: Beschreibung des Services
            category: object_id der Category (optional)
            icon: Icon für den Service
            order: Reihenfolge/Sortierung
            hidden: Ob der Service versteckt ist
            isFavorite: Ob der Service als Favorit markiert ist
        
        Returns:
            Erstellte Service-Daten
        """
        data = {
            "name": name,
            "title": title or name,
            "app_space": app_space,  # Pflichtfeld
            "icon": icon,
            "order": order,
            "hidden": hidden,
            "isFavorite": isFavorite
        }
        
        if description:
            data["description"] = description
        if category:
            data["category"] = category
        
        if self.debug:
            logger.info(f"Sending data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        response = await self.client.post("/services/", json=data)
        
        if self.debug:
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")
        
        response.raise_for_status()
        return response.json()
    
    async def update_service_endpoint(
        self, 
        service_id: str, 
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
        Aktualisiert einen Service.
        
        Args:
            service_id: object_id des Services
            name: Neuer Name (optional)
            title: Neuer Titel (optional)
            description: Neue Beschreibung (optional)
            category: Neue Category ID (optional)
            app_space: Neue App Space ID (optional)
            icon: Neues Icon (optional)
            order: Neue Reihenfolge (optional)
            hidden: Neuer Hidden Status (optional)
            isFavorite: Neuer Favorite Status (optional)
        
        Returns:
            Aktualisierte Service-Daten
        """
        data = {}
        
        if name is not None:
            data["name"] = name
        if title is not None:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if category is not None:
            data["category"] = category
        if app_space is not None:
            data["app_space"] = app_space
        if icon is not None:
            data["icon"] = icon
        if order is not None:
            data["order"] = order
        if hidden is not None:
            data["hidden"] = hidden
        if isFavorite is not None:
            data["isFavorite"] = isFavorite
        
        if not data:
            raise ValueError("Mindestens ein Parameter muss angegeben werden")
        
        # Dimetrics erwartet trailing slash für PATCH
        response = await self.client.patch(f"/services/{service_id}/", json=data)
        response.raise_for_status()
        
        return response.json()
    
    async def delete_service_endpoint(self, service_id: str) -> bool:
        """
        Löscht einen Service.
        
        Args:
            service_id: object_id des Services
        
        Returns:
            True wenn erfolgreich gelöscht
        """
        # Dimetrics erwartet trailing slash für DELETE
        response = await self.client.delete(f"/services/{service_id}/")
        response.raise_for_status()
        return True

    # Resources Endpoints
    async def list_resources_endpoint(self, search: str = None, page_size: int = None, page: int = None, limit: int = None) -> Dict[str, Any]:
        """Listet alle Resources auf."""
        params = {}
        if search:
            params["search"] = search
        if page_size:
            params["page_size"] = page_size
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit
        
        response = await self.client.get("/resources/", params=params)
        response.raise_for_status()
        return response.json()

    async def get_resource_endpoint(self, resource_id: str) -> Dict[str, Any]:
        """Holt Details eines spezifischen Resources."""
        response = await self.client.get(f"/resources/{resource_id}/")
        response.raise_for_status()
        return response.json()

    async def create_resource_endpoint(
        self,
        name: str,
        service: str,
        title: str = "",
        title_plural: str = "",
        description: str = "",
       
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
    
    ) -> Dict[str, Any]:
        """Erstellt eine neue Resource mit JSON-Data."""
        data = {
            "service": service,
            "name": name,
            "title": title or name,
            "title_plural": title_plural or title or name,
            "description": description,
           
            "form_layout_type": form_layout_type,
            "meta_attributes_enabled": meta_attributes_enabled,
            "database_connection": database_connection,
            "primary_key_name": primary_key_name,
            "primary_key_type": primary_key_type,
            "table_type": table_type,
            "table_column_width": table_column_width,
            "default_page_size": default_page_size,
            "is_table_pagination": is_table_pagination,
            "is_table_flex": is_table_flex,
            "allow_table_inline_edit": allow_table_inline_edit,
            "table_sort_default_column_name": table_sort_default_column_name,
        
        }
        
        if self.debug:
            logger.info(f"Sending data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        response = await self.client.post("/resources/", json=data)
        
        if self.debug:
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")
            
        response.raise_for_status()
        return response.json()

    async def update_resource_endpoint(
        self,
        resource_id: str,
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
     
    ) -> Dict[str, Any]:
        """Aktualisiert eine Resource mit JSON-Data."""
        data = {}
        
        if name is not None:
            data["name"] = name
        if title is not None:
            data["title"] = title
        if title_plural is not None:
            data["title_plural"] = title_plural
        if description is not None:
            data["description"] = description
        if icon is not None:
            data["icon"] = icon
        if form_layout_type is not None:
            data["form_layout_type"] = form_layout_type
        if meta_attributes_enabled is not None:
            data["meta_attributes_enabled"] = meta_attributes_enabled
        if database_connection is not None:
            data["database_connection"] = database_connection
        if primary_key_name is not None:
            data["primary_key_name"] = primary_key_name
        if primary_key_type is not None:
            data["primary_key_type"] = primary_key_type
        if table_type is not None:
            data["table_type"] = table_type
        if table_column_width is not None:
            data["table_column_width"] = table_column_width
        if default_page_size is not None:
            data["default_page_size"] = default_page_size
        if is_table_pagination is not None:
            data["is_table_pagination"] = is_table_pagination
        if is_table_flex is not None:
            data["is_table_flex"] = is_table_flex
        if allow_table_inline_edit is not None:
            data["allow_table_inline_edit"] = allow_table_inline_edit
        if table_sort_default_column_name is not None:
            data["table_sort_default_column_name"] = table_sort_default_column_name
        if table_sort_default_direction is not None:
            data["table_sort_default_direction"] = table_sort_default_direction
       
        
        if not data:
            raise ValueError("Mindestens ein Parameter muss angegeben werden")
        
        response = await self.client.patch(f"/resources/{resource_id}/", json=data)
        response.raise_for_status()
        return response.json()

    async def delete_resource_endpoint(self, resource_id: str) -> bool:
        """Löscht eine Resource."""
        # Dimetrics erwartet trailing slash für DELETE
        response = await self.client.delete(f"/resources/{resource_id}/")
        response.raise_for_status()
        return True

    # ===== ATTRIBUTE ENDPOINTS =====
    
    async def list_attributes(self, resource_name: str, search: str = None, page_size: int = None, page: int = None, limit: int = None) -> Dict[str, Any]:
        """
        Listet alle Attribute für eine Resource auf.
        
        Args:
            resource_name: Name der Resource
            search: Optionaler Suchbegriff
            page_size: Anzahl der Ergebnisse pro Seite
            page: Seitennummer für Pagination
            limit: Maximale Anzahl der Ergebnisse
        
        Returns:
            Liste der Attribute
        """
        params = {}
        if search:
            params["search"] = search
        if page_size:
            params["page_size"] = page_size
        if page:
            params["page"] = page
        if limit:
            params["limit"] = limit
        
        response = await self.client.get(f"/attributes/{resource_name}/", params=params)
        response.raise_for_status()
        return response.json()

    async def get_attribute_details(self, resource_name: str, attribute_id: str) -> Dict[str, Any]:
        """
        Holt detaillierte Informationen zu einem Attribut.
        
        Args:
            resource_name: Name der Resource
            attribute_id: ID des Attributs
        
        Returns:
            Attribut-Details
        """
        response = await self.client.get(f"/attributes/{resource_name}/{attribute_id}/")
        response.raise_for_status()
        return response.json()

    async def create_attribute(
        self,
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
        **kwargs
    ) -> Dict[str, Any]:
        """
        Erstellt ein neues Attribut für eine Resource.
        
        Args:
            resource_name: Name der Resource
            name: Technischer Name des Attributs (nur Buchstaben, Zahlen, Unterstriche)
            attribute_type: Typ des Attributs (INPUT_FIELD, NUMERIC_FIELD, etc.)
            label: Anzeigename des Attributs
            description: Beschreibung des Attributs
            required: Ob das Feld erforderlich ist
            readonly: Ob das Feld nur lesbar ist
            unique: Ob der Wert eindeutig sein muss
            show_in_table: Ob das Feld in Tabellen angezeigt wird
            enable_sum: Ob Summen-Aggregation aktiviert ist (nur für numerische Felder)
            field_order: Reihenfolge der Felder
            form_layout_location: Layout-Bereich im Formular (Main, Meta, Advanced)
            form_layout_col: Spaltenbreite im Formular (1-12)
            **kwargs: Zusätzliche typ-spezifische Parameter
        
        Returns:
            Erstellte Attribut-Daten
        """
        data = {
            "name": name,
            "type": attribute_type,
            "label": label,
            "required": required,
            "readonly": readonly,
            "unique": unique,
            "show_in_table": show_in_table,
            "enable_sum": enable_sum,
            "form_layout_location": form_layout_location,
            "form_layout_col": form_layout_col
        }
        
        if description:
            data["description"] = description
        if field_order is not None:
            data["field_order"] = field_order
            
        # Typ-spezifische Parameter hinzufügen
        data.update(kwargs)
        
        if self.debug:
            logger.info(f"Creating attribute with data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        response = await self.client.post(f"/attributes/{resource_name}/", json=data)
        
        if self.debug:
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")
        
        response.raise_for_status()
        return response.json()

    async def update_attribute(
        self,
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
        form_layout_col: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Aktualisiert ein Attribut.
        
        Args:
            resource_name: Name der Resource
            attribute_id: ID des Attributs
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
            **kwargs: Zusätzliche typ-spezifische Parameter
        
        Returns:
            Aktualisierte Attribut-Daten
        """
        data = {}
        
        if name is not None:
            data["name"] = name
        if label is not None:
            data["label"] = label
        if description is not None:
            data["description"] = description
        if required is not None:
            data["required"] = required
        if readonly is not None:
            data["readonly"] = readonly
        if unique is not None:
            data["unique"] = unique
        if show_in_table is not None:
            data["show_in_table"] = show_in_table
        if enable_sum is not None:
            data["enable_sum"] = enable_sum
        if field_order is not None:
            data["field_order"] = field_order
        if form_layout_location is not None:
            data["form_layout_location"] = form_layout_location
        if form_layout_col is not None:
            data["form_layout_col"] = form_layout_col
            
        # Typ-spezifische Parameter hinzufügen
        data.update(kwargs)
        
        if self.debug:
            logger.info(f"Updating attribute with data: {json.dumps(data, indent=2, ensure_ascii=False)}")
        
        # Dimetrics erwartet PATCH für Attribut-Updates mit trailing slash
        response = await self.client.patch(f"/attributes/{resource_name}/{attribute_id}/", json=data)
        
        if self.debug:
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")
        
        response.raise_for_status()
        return response.json()

    async def delete_attribute(self, resource_name: str, attribute_id: str) -> bool:
        """
        Löscht ein Attribut.
        
        Args:
            resource_name: Name der Resource
            attribute_id: ID des Attributs
        
        Returns:
            True bei erfolgreichem Löschen
        """
        # Dimetrics erwartet trailing slash für DELETE
        response = await self.client.delete(f"/attributes/{resource_name}/{attribute_id}/")
        response.raise_for_status()
        return True

    async def create_attributes_bulk(self, resource_name: str, attributes: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Erstellt mehrere Attribute gleichzeitig.
        
        Args:
            resource_name: Name der Resource
            attributes: Liste von Attribut-Definitionen
        
        Returns:
            Liste der erstellten Attribute
        """
        if self.debug:
            logger.info(f"Creating bulk attributes: {json.dumps(attributes, indent=2, ensure_ascii=False)}")
        
        response = await self.client.post(f"/attributes/{resource_name}/bulk/", json=attributes)
        
        if self.debug:
            logger.info(f"Response status: {response.status_code}")
            logger.info(f"Response body: {response.text}")
        
        response.raise_for_status()
        return response.json()
    
    async def close(self):
        """Schließt den HTTP Client."""
        await self.client.aclose()
