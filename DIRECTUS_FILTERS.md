# 🎯 Directus-Filter für Dimetrics MCP Server

## ✅ Implementierungsstatus

Die Directus-ähnlichen Filter wurden erfolgreich implementiert und getestet! Das System unterstützt jetzt die gleiche mächtige Filter-Syntax wie Directus CMS.

## 🚀 Neue Features

### API Client (`list_generic_entries`)
- ✅ **Directus-Filter Parameter**: Neuer `directus_filter` Parameter
- ✅ **URL-Encoding**: Automatische JSON-zu-URL-Konvertierung
- ✅ **Backward Compatibility**: Legacy `filters` Parameter weiterhin unterstützt
- ✅ **Debug Logging**: Detaillierte Filter-Logs für Entwicklung

### MCP Tool (`list_generic_entries`)
- ✅ **Neuer Parameter**: `directus_filter_json` für Directus-ähnliche Filter
- ✅ **Legacy Support**: `filters_json` für einfache Filter (Rückwärtskompatibilität)
- ✅ **Umfassende Dokumentation**: Alle Operatoren und Beispiele in der Tool-Beschreibung
- ✅ **Error Handling**: Separate JSON-Validierung für beide Filter-Typen

## 📊 Unterstützte Directus-Operatoren

### Vergleichsoperatoren
| Operator | Beschreibung | Beispiel |
|----------|--------------|----------|
| `_eq` | Gleichheit | `{"state": {"_eq": "ok"}}` |
| `_neq` | Ungleichheit | `{"state": {"_neq": "pending"}}` |
| `_gt` | Größer | `{"amount": {"_gt": 10}}` |
| `_gte` | Größer oder gleich | `{"amount": {"_gte": 10}}` |
| `_lt` | Kleiner | `{"amount": {"_lt": 100}}` |
| `_lte` | Kleiner oder gleich | `{"amount": {"_lte": 100}}` |

### Mengen-Operatoren
| Operator | Beschreibung | Beispiel |
|----------|--------------|----------|
| `_in` | In Liste | `{"state": {"_in": ["ok", "pending"]}}` |
| `_nin` | Nicht in Liste | `{"state": {"_nin": ["error", "failed"]}}` |

### Text-Operatoren
| Operator | Beschreibung | Beispiel |
|----------|--------------|----------|
| `_contains` | Enthält | `{"name": {"_contains": "Canva"}}` |
| `_ncontains` | Enthält nicht | `{"name": {"_ncontains": "test"}}` |
| `_starts_with` | Beginnt mit | `{"name": {"_starts_with": "WG:"}}` |
| `_nstarts_with` | Beginnt nicht mit | `{"name": {"_nstarts_with": "RE:"}}` |
| `_ends_with` | Endet mit | `{"name": {"_ends_with": "Rechnung"}}` |
| `_nends_with` | Endet nicht mit | `{"name": {"_nends_with": "Draft"}}` |

### Spezial-Operatoren
| Operator | Beschreibung | Beispiel |
|----------|--------------|----------|
| `_between` | Zwischen Werten | `{"date_created": {"_between": ["2025-01-01", "2025-12-31"]}}` |
| `_nbetween` | Nicht zwischen | `{"amount": {"_nbetween": [0, 10]}}` |
| `_null` | Ist null | `{"description": {"_null": true}}` |
| `_nnull` | Ist nicht null | `{"description": {"_nnull": true}}` |
| `_empty` | Ist leer | `{"notes": {"_empty": true}}` |
| `_nempty` | Ist nicht leer | `{"notes": {"_nempty": true}}` |

### Logische Operatoren
| Operator | Beschreibung | Beispiel |
|----------|--------------|----------|
| `_and` | UND-Verknüpfung | `{"_and": [{"state": {"_eq": "ok"}}, {"amount": {"_gte": 10}}]}` |
| `_or` | ODER-Verknüpfung | `{"_or": [{"state": {"_eq": "ok"}}, {"state": {"_eq": "pending"}}]}` |

## 🛠️ Anwendungsbeispiele

### 1. Einfache Filter
```bash
# Nur aktive Einträge
@dimetrics list_generic_entries resource_name="lau6_RunEntries" directus_filter_json='{"state": {"_eq": "active"}}'

# Läufe über 5km
@dimetrics list_generic_entries resource_name="lau6_RunEntries" directus_filter_json='{"distance_km": {"_gte": 5}}'

# Trainingsart ist Dauerlauf
@dimetrics list_generic_entries resource_name="lau6_RunEntries" directus_filter_json='{"training_type": {"_eq": "dauerlauf"}}'
```

### 2. Text-Suche
```bash
# Namen enthalten "Marathon"
@dimetrics list_generic_entries resource_name="lau6_RunEntries" directus_filter_json='{"notes": {"_contains": "Marathon"}}'

# Notizen beginnen mit "Tolles"
@dimetrics list_generic_entries resource_name="lau6_RunEntries" directus_filter_json='{"notes": {"_starts_with": "Tolles"}}'
```

### 3. Datum- und Zeit-Filter
```bash
# Läufe aus 2025
@dimetrics list_generic_entries resource_name="lau6_RunEntries" directus_filter_json='{"run_date": {"_between": ["2025-01-01", "2025-12-31"]}}'

# Läufe der letzten Woche
@dimetrics list_generic_entries resource_name="lau6_RunEntries" directus_filter_json='{"run_date": {"_gte": "2025-09-01"}}'
```

### 4. Komplexe Kombinationen
```bash
# Dauerlauf ODER Longrun, über 10km
@dimetrics list_generic_entries resource_name="lau6_RunEntries" directus_filter_json='{"_and": [{"_or": [{"training_type": {"_eq": "dauerlauf"}}, {"training_type": {"_eq": "longrun"}}]}, {"distance_km": {"_gte": 10}}]}'

# Aktive Läufe mit Notizen
@dimetrics list_generic_entries resource_name="lau6_RunEntries" directus_filter_json='{"_and": [{"state": {"_eq": "active"}}, {"notes": {"_nempty": true}}]}'
```

### 5. Listen-Filter
```bash
# Bestimmte Trainingsarten
@dimetrics list_generic_entries resource_name="lau6_RunEntries" directus_filter_json='{"training_type": {"_in": ["dauerlauf", "longrun", "tempo"]}}'

# Ausschluss bestimmter Zustände
@dimetrics list_generic_entries resource_name="lau6_RunEntries" directus_filter_json='{"state": {"_nin": ["deleted", "draft"]}}'
```

## 🔄 Kombination mit anderen Parametern

```bash
# Filter + Sortierung + Pagination
@dimetrics list_generic_entries \
  resource_name="lau6_RunEntries" \
  directus_filter_json='{"distance_km": {"_gte": 10}}' \
  ordering="-run_date" \
  page_size=5 \
  page=1

# Filter + Textsuche
@dimetrics list_generic_entries \
  resource_name="lau6_RunEntries" \
  search="Marathon" \
  directus_filter_json='{"training_type": {"_eq": "longrun"}}'
```

## 🔧 Technische Details

### URL-Encoding
Die Filter werden automatisch als JSON-String URL-encoded übertragen:
```
/api/generics/n8n_collection/?filter=%7B%22state%22%3A%7B%22_eq%22%3A%22ok%22%7D%7D
```

### Parameter-Priorität
1. **Directus-Filter** (bevorzugt): `directus_filter_json`
2. **Legacy-Filter** (Fallback): `filters_json`

### Rückwärtskompatibilität
Bestehende einfache Filter funktionieren weiterhin:
```bash
# Legacy (funktioniert weiterhin)
@dimetrics list_generic_entries resource_name="lau6_RunEntries" filters_json='{"state": "active"}'

# Neu (empfohlen)
@dimetrics list_generic_entries resource_name="lau6_RunEntries" directus_filter_json='{"state": {"_eq": "active"}}'
```

## ✅ Getestete Funktionen

- ✅ **Alle Operatoren**: `_eq`, `_gte`, `_contains`, `_in`, etc.
- ✅ **Logische Verknüpfungen**: `_and`, `_or`
- ✅ **Kombinationen**: Filter + Sortierung + Pagination + Suche
- ✅ **JSON-Validierung**: Fehlerbehandlung für ungültiges JSON
- ✅ **URL-Encoding**: Korrekte Übertragung komplexer Filter
- ✅ **Rückwärtskompatibilität**: Legacy-Filter funktionieren weiterhin

## 🎯 Nächste Schritte

Die Directus-Filter-Implementierung ist vollständig und produktionsreif! Sie können jetzt:

1. **Komplexe Abfragen** für Ihre Lauftagebuch-Daten erstellen
2. **Relation-Fields** mit Filtern kombinieren (vendor.name, etc.)
3. **Analytische Abfragen** mit Aggregationen durchführen
4. **Performance-optimierte** Abfragen mit gezielten Filtern erstellen

Die Implementierung folgt exakt der Directus-Spezifikation und bietet die gleiche Mächtigkeit und Flexibilität! 🚀
