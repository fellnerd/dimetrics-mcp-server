## AttributeDefinition API Documentation

### Übersicht

Das AttributeDefinition System ermöglicht die dynamische Definition von Feldern für Resources. Jedes Attribut definiert ein Datenfeld mit spezifischen Eigenschaften, Validierungsregeln und UI-Verhalten.

### Basis-Schema

```json
{
  "type": "object",
  "properties": {
    "object_id": {
      "type": "string",
      "format": "uuid",
      "description": "Eindeutige ID des Attributs"
    },
    "name": {
      "type": "string",
      "pattern": "^[A-Za-z0-9_]+$",
      "description": "Technischer Name des Attributs (nur Buchstaben, Zahlen, Unterstriche)"
    },
    "resource": {
      "type": "string",
      "format": "uuid",
      "description": "Resource-ID zu der das Attribut gehört"
    },
    "type": {
      "type": "string",
      "enum": [
        "INPUT_FIELD", "TEXT_FIELD", "NUMERIC_FIELD", "BOOLEAN_FIELD",
        "SLIDER_FIELD", "DROPDOWN_FIELD", "DROPDOWN_MULTI_FIELD",
        "RELATION_FIELD", "RELATION_FIELD_MULTI", "TIMESTAMP_FIELD",
        "STATE_FIELD", "ICON_SELECT", "ACTION", "FILE", "FILES",
        "IMAGE", "INFO", "LINK", "MEMBER", "MEMBER_MULTI",
        "LIST_FIELD", "IFRAME", "TIMELINE", "RTE", "JSON"
      ],
      "description": "Typ des Attributs"
    },
    "label": {
      "type": "string",
      "description": "Anzeigename des Attributs"
    },
    "description": {
      "type": "string",
      "description": "Beschreibung des Attributs"
    },
    "required": {
      "type": "boolean",
      "default": false,
      "description": "Ob das Feld erforderlich ist"
    },
    "readonly": {
      "type": "boolean",
      "default": false,
      "description": "Ob das Feld nur lesbar ist"
    },
    "unique": {
      "type": "boolean",
      "default": false,
      "description": "Ob der Wert eindeutig sein muss"
    },
    "show_in_table": {
      "type": "boolean",
      "default": true,
      "description": "Ob das Feld in Tabellen angezeigt wird"
    },
    "enable_sum": {
      "type": "boolean",
      "default": false,
      "description": "Ob Summen-Aggregation für numerische Felder aktiviert ist"
    },
    "field_order": {
      "type": "integer",
      "description": "Reihenfolge der Felder"
    },
    "form_layout_location": {
      "type": "string",
      "enum": ["Main", "Meta", "Advanced"],
      "default": "Main",
      "description": "Layout-Bereich im Formular"
    },
    "form_layout_col": {
      "type": "string",
      "pattern": "^(1|2|3|4|6|12)$",
      "default": "12",
      "description": "Spaltenbreite im Formular (1-12)"
    }
  },
  "required": ["name", "type", "label"]
}
```

### Feld-Typen und spezifische Eigenschaften

#### INPUT_FIELD / TEXT_FIELD
Einfache Text-Eingabefelder

```json
{
  "allOf": [{"$ref": "#/definitions/BaseAttribute"}],
  "properties": {
    "type": {"enum": ["INPUT_FIELD", "TEXT_FIELD"]},
    "placeholder": {"type": "string"},
    "maxLength": {"type": "integer", "minimum": 1},
    "minLength": {"type": "integer", "minimum": 0},
    "default_value": {"type": "string"},
    "mask": {"type": "string", "description": "Input-Maske"},
    "input_type": {
      "type": "string",
      "enum": ["text", "email", "password", "tel", "url", "search"],
      "default": "text"
    }
  }
}
```

#### NUMERIC_FIELD
Numerische Felder

```json
{
  "allOf": [{"$ref": "#/definitions/BaseAttribute"}],
  "properties": {
    "type": {"enum": ["NUMERIC_FIELD"]},
    "numeric_datatype": {
      "type": "string",
      "enum": ["integer", "bigint", "decimal", "real"],
      "default": "integer"
    },
    "minNumeric": {"type": "number"},
    "maxNumeric": {"type": "number"},
    "default_value": {"type": "string", "pattern": "^-?\\d+(\\.\\d+)?$"},
    "is_auto_increment": {"type": "boolean", "default": false},
    "enable_sum": {"type": "boolean", "default": false},
    "number_representation": {
      "type": "string",
      "enum": ["default", "currency", "percentage"],
      "default": "default"
    }
  }
}
```

#### BOOLEAN_FIELD
Boolean-Felder

```json
{
  "allOf": [{"$ref": "#/definitions/BaseAttribute"}],
  "properties": {
    "type": {"enum": ["BOOLEAN_FIELD"]},
    "default_checked": {"type": "boolean", "default": false},
    "true_text": {"type": "string", "default": "Ja"},
    "false_text": {"type": "string", "default": "Nein"}
  }
}
```

#### DROPDOWN_FIELD / DROPDOWN_MULTI_FIELD
Dropdown-Auswahlfelder

```json
{
  "allOf": [{"$ref": "#/definitions/BaseAttribute"}],
  "properties": {
    "type": {"enum": ["DROPDOWN_FIELD", "DROPDOWN_MULTI_FIELD"]},
    "dropdown_options_string": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "text": {"type": "string"},
          "value": {"type": "string"}
        },
        "required": ["text", "value"]
      }
    },
    "dropdown_options_number": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "text": {"type": "string"},
          "value": {"type": "number"}
        },
        "required": ["text", "value"]
      }
    },
    "dropdown_type": {
      "type": "string",
      "enum": ["string", "number"],
      "default": "string"
    }
  }
}
```

#### RELATION_FIELD / RELATION_FIELD_MULTI
Beziehungsfelder zu anderen Resources

```json
{
  "allOf": [{"$ref": "#/definitions/BaseAttribute"}],
  "properties": {
    "type": {"enum": ["RELATION_FIELD", "RELATION_FIELD_MULTI"]},
    "linked_resource": {
      "type": "string",
      "format": "uuid",
      "description": "ID der verknüpften Resource"
    },
    "alt_display_field": {
      "type": "string",
      "description": "Alternatives Anzeigefeld"
    },
    "hide_child_resource": {"type": "boolean", "default": false}
  },
  "required": ["linked_resource"]
}
```

#### TIMESTAMP_FIELD
Datum/Zeit-Felder

```json
{
  "allOf": [{"$ref": "#/definitions/BaseAttribute"}],
  "properties": {
    "type": {"enum": ["TIMESTAMP_FIELD"]},
    "date_format": {
      "type": "string",
      "enum": ["YYYY-MM-DD", "DD.MM.YYYY", "MM/DD/YYYY", "ISO"],
      "default": "YYYY-MM-DD"
    },
    "input_type": {
      "type": "string",
      "enum": ["date", "datetime-local", "time"],
      "default": "date"
    }
  }
}
```

#### FILE / FILES / IMAGE
Datei-Upload-Felder

```json
{
  "allOf": [{"$ref": "#/definitions/BaseAttribute"}],
  "properties": {
    "type": {"enum": ["FILE", "FILES", "IMAGE"]},
    "is_image_file": {"type": "boolean", "default": false},
    "file_show_image": {
      "type": "string",
      "enum": ["rounded", "circular"],
      "description": "Bild-Darstellungstyp"
    },
    "use_file_disc_name": {"type": "boolean", "default": false}
  }
}
```

### API Endpoints

#### GET /api/attributes/{resource_name}/
Liste aller Attribute einer Resource

**Response:**
```json
[
  {
    "object_id": "uuid",
    "name": "field_name",
    "type": "INPUT_FIELD",
    "label": "Feldname",
    "resource": {"name": "resource_name", "object_id": "uuid"},
    "show_in_table": true,
    "required": false,
    "field_order": 1
  }
]
```

#### POST /api/attributes/{resource_name}/
Neues Attribut erstellen

**Request Body:**
```json
{
  "name": "new_field",
  "type": "INPUT_FIELD",
  "label": "Neues Feld",
  "required": true,
  "maxLength": 255,
  "placeholder": "Bitte eingeben..."
}
```

#### PUT /api/attributes/{resource_name}/{object_id}/
Attribut aktualisieren

**Request Body:**
```json
{
  "label": "Aktualisierter Feldname",
  "required": false,
  "show_in_table": false
}
```

#### POST /api/attributes/{resource_name}/bulk/
Mehrere Attribute gleichzeitig erstellen/aktualisieren

**Request Body:**
```json
[
  {
    "name": "field1",
    "type": "INPUT_FIELD",
    "label": "Feld 1"
  },
  {
    "name": "field2",
    "type": "NUMERIC_FIELD",
    "label": "Feld 2",
    "enable_sum": true
  }
]
```

### Tabellen-spezifische Eigenschaften

```json
{
  "grid_width": {"type": "integer", "description": "Spaltenbreite in AG-Grid"},
  "table_default_column_width": {"type": "integer", "default": 150},
  "display_in_table_as": {
    "type": "string",
    "enum": ["text", "tag", "link", "badge", "avatar"],
    "default": "text"
  },
  "member_table_display": {
    "type": "string",
    "enum": ["AVATAR", "TAG_COLOR", "TAG"],
    "description": "Darstellung für MEMBER-Felder"
  }
}
```

### Validierungsregeln

1. **Name**: Nur alphanumerische Zeichen und Unterstriche
2. **Typ**: Muss einem der definierten Typen entsprechen
3. **Verknüpfte Resource**: Bei RELATION_FIELD muss linked_resource gesetzt sein
4. **Numerische Felder**: minNumeric ≤ maxNumeric
5. **Text-Felder**: minLength ≤ maxLength
6. **Dropdown-Optionen**: Mindestens eine Option bei DROPDOWN_FIELD

### Besondere Verhaltensweisen

1. **enable_sum**: Nur für NUMERIC_FIELD relevant, aktiviert Summen-Aggregation in Tabellen
2. **is_name**: Kennzeichnet das primäre Namensfeld der Resource
3. **show_as_info**: Zeigt Feld als Info-Icon anstatt vollständiger Spalte
4. **filterable**: Bestimmt ob Feld in Filtern verfügbar ist
5. **current_user**: Bei RELATION_FIELD automatisch aktueller User als Default

### Directus-Integration

Beim Erstellen/Aktualisieren von Attributen werden automatisch entsprechende Directus-Felder erstellt:
- Schema-Definition (Typ, Constraints, Default-Werte)
- Meta-Informationen (Interface, Optionen, Beschreibung)
- Relationen (bei RELATION_FIELD Typen)

### Best Practices

1. Verwende aussagekräftige `name` und `label` Werte
2. Setze `enable_sum: true` nur bei numerischen Feldern wo Summen sinnvoll sind
3. Nutze `field_order` für konsistente Formular-Layouts
4. Gruppiere verwandte Felder in `form_layout_location`
5. Verwende `readonly: true` für berechnete oder System-Felder
