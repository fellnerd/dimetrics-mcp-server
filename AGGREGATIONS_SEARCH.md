# 📊 Dimetrics Aggregations & Search Features

## ✅ Implementierungsstatus (100% Funktional)

Die Aggregations- und Search-Features wurden erfolgreich implementiert und getestet! Das System unterstützt jetzt:

- ✅ **Aggregations-API**: sum, count, avg, min, max
- ✅ **Search-Parameter**: Volltext-Suche in allen Feldern
- ✅ **Kombinierte Queries**: Filter + Aggregation + Search + Sortierung
- ✅ **MCP Integration**: Vollständige Tool-Integration für GitHub Copilot
- ✅ **Multiple Aggregationen**: Mehrere Aggregationen gleichzeitig

## 🚀 Neue API-Features

### API Client (`list_generic_entries`)
- ✅ **Search Parameter**: Volltext-Suche mit `search` Parameter
- ✅ **Aggregation Parameter**: `aggregate` Dict mit Aggregations-Funktionen
- ✅ **Kombinierte Queries**: Alle Parameter können gleichzeitig verwendet werden
- ✅ **URL-Encoding**: Automatische Parameter-Kodierung für komplexe Queries

### MCP Tool (`list_generic_entries`)
- ✅ **Search Parameter**: `search` für Volltext-Suche
- ✅ **Aggregation Parameter**: `aggregate_json` für JSON-Aggregationen
- ✅ **Erweiterte Dokumentation**: Alle Features und Beispiele in der Tool-Beschreibung
- ✅ **Structured Output**: Klare Trennung von Daten und Aggregations-Ergebnissen

## 📊 Unterstützte Aggregations-Funktionen

### Numerische Aggregationen
| Funktion | Beschreibung | Beispiel | Resultat |
|----------|--------------|----------|----------|
| `sum` | Summe aller Werte | `{"sum": "amount"}` | `{"sum": {"amount": "54.00"}}` |
| `avg` | Durchschnitt aller Werte | `{"avg": "amount"}` | `{"avg": {"amount": "18.0000000000000000"}}` |
| `min` | Minimum der Werte | `{"min": "amount"}` | `{"min": {"amount": "0.00"}}` |
| `max` | Maximum der Werte | `{"max": "amount"}` | `{"max": {"amount": "27.00"}}` |

### Allgemeine Aggregationen
| Funktion | Beschreibung | Beispiel | Resultat |
|----------|--------------|----------|----------|
| `count` | Anzahl nicht-null Werte | `{"count": "amount"}` | `{"count": {"amount": "3"}}` |

### Multiple Aggregationen
```json
{
  "sum": "amount",
  "count": "name", 
  "avg": "amount"
}
```

**Resultat:**
```json
{
  "count": {"name": "3"},
  "sum": {"amount": "54.00"},
  "avg": {"amount": "18.0000000000000000"},
  "object_id": null
}
```

## 🔍 Search-Funktionalität

### Volltext-Suche
Der `search` Parameter durchsucht **alle Textfelder** der Resource:

```bash
# Suche nach "Test" in allen Feldern
search="Test"

# Findet Übereinstimmungen in: name, description, notes, from, etc.
```

**Beispiel-Ergebnis:**
```json
{
  "count": 1,
  "results": [
    {
      "name": "Test",
      "amount": 0.0,
      "state": "error",
      "from": "",
      "object_id": "c89515a4-13f3-4d7e-b4a5-249b5b4e8368"
    }
  ]
}
```

## 🛠️ Anwendungsbeispiele

### 1. Einfache Aggregationen
```bash
# Summe aller Beträge
@dimetrics list_generic_entries resource_name="n8n_collection" aggregate_json='{"sum": "amount"}'

# Anzahl aller Einträge
@dimetrics list_generic_entries resource_name="n8n_collection" aggregate_json='{"count": "name"}'

# Durchschnittlicher Betrag
@dimetrics list_generic_entries resource_name="n8n_collection" aggregate_json='{"avg": "amount"}'
```

### 2. Multiple Aggregationen
```bash
# Mehrere Aggregationen gleichzeitig
@dimetrics list_generic_entries \
  resource_name="n8n_collection" \
  aggregate_json='{"sum": "amount", "count": "name", "avg": "amount", "min": "amount", "max": "amount"}'
```

### 3. Search-Queries
```bash
# Volltext-Suche
@dimetrics list_generic_entries resource_name="n8n_collection" search="Test"

# Search + Filter kombiniert
@dimetrics list_generic_entries \
  resource_name="n8n_collection" \
  search="Test" \
  directus_filter_json='{"state": {"_neq": "deleted"}}'
```

### 4. Aggregation + Filter
```bash
# Summe nur für Einträge mit state="ok"
@dimetrics list_generic_entries \
  resource_name="n8n_collection" \
  directus_filter_json='{"state": {"_eq": "ok"}}' \
  aggregate_json='{"sum": "amount", "count": "amount"}'
```

### 5. Komplexe Kombinationen
```bash
# Vollständige analytische Query
@dimetrics list_generic_entries \
  resource_name="n8n_collection" \
  search="Test" \
  directus_filter_json='{"amount": {"_gte": 10}}' \
  aggregate_json='{"sum": "amount", "avg": "amount", "count": "amount"}' \
  ordering="-amount" \
  page_size=10
```

## 📈 Für Lauftagebuch-Daten

### Trainings-Analysen
```bash
# Gesamte Laufdistanz
@dimetrics list_generic_entries \
  resource_name="lau6_RunEntries" \
  aggregate_json='{"sum": "distance_km"}'

# Durchschnittliche Pace
@dimetrics list_generic_entries \
  resource_name="lau6_RunEntries" \
  aggregate_json='{"avg": "pace_min_per_km"}'

# Anzahl Läufe pro Trainingsart
@dimetrics list_generic_entries \
  resource_name="lau6_RunEntries" \
  directus_filter_json='{"training_type": {"_eq": "dauerlauf"}}' \
  aggregate_json='{"count": "name"}'
```

### Zeitraum-Analysen
```bash
# Läufe aus 2025 mit Gesamtdistanz
@dimetrics list_generic_entries \
  resource_name="lau6_RunEntries" \
  directus_filter_json='{"run_date": {"_between": ["2025-01-01", "2025-12-31"]}}' \
  aggregate_json='{"sum": "distance_km", "count": "name", "avg": "distance_km"}'

# Beste und schlechteste Pace
@dimetrics list_generic_entries \
  resource_name="lau6_RunEntries" \
  aggregate_json='{"min": "pace_min_per_km", "max": "pace_min_per_km"}'
```

### Such-Queries für Laufdaten
```bash
# Suche nach Marathon-Läufen
@dimetrics list_generic_entries \
  resource_name="lau6_RunEntries" \
  search="Marathon"

# Langläufe über 15km
@dimetrics list_generic_entries \
  resource_name="lau6_RunEntries" \
  directus_filter_json='{"_and": [{"training_type": {"_eq": "longrun"}}, {"distance_km": {"_gte": 15}}]}' \
  aggregate_json='{"count": "name", "avg": "distance_km", "max": "distance_km"}'
```

## 🔧 Technische Details

### API-Parameter-Mapping
```python
# Aggregation wird zu URL-Parametern:
aggregate={"sum": "amount", "count": "name"}
# → ?aggregate[sum]=amount&aggregate[count]=name

# Search wird direkt übergeben:
search="Test"
# → ?search=Test
```

### Response-Format bei Aggregationen
```json
{
  "count": 3,          // Anzahl gefundener Einträge (vor Aggregation)
  "next": null,
  "previous": null,
  "aggregations": [],  // Leer (historisch)
  "results": [         // Aggregations-Ergebnisse statt Rohdaten
    {
      "sum": {"amount": "54.00"},
      "count": {"name": "3"},
      "avg": {"amount": "18.0000000000000000"},
      "object_id": null  // Immer null bei Aggregationen
    }
  ]
}
```

### Parameter-Prioritäten
1. **Aggregation**: Wenn gesetzt, werden aggregierte Werte statt Rohdaten zurückgegeben
2. **Search**: Wird vor Filtern angewendet
3. **Directus-Filter**: Werden auf Such-Ergebnisse angewendet
4. **Sortierung**: Bei Aggregationen meist nicht relevant

## ✅ Getestete Funktionen

### Direkte API-Tests (test_aggregations.py)
- ✅ **Sum Aggregation**: `{"sum": {"amount": "54.00"}}`
- ✅ **Count Aggregation**: `{"count": {"amount": "3"}}`
- ✅ **Average Aggregation**: `{"avg": {"amount": "18.0000000000000000"}}`
- ✅ **Min/Max Aggregations**: `{"min": {"amount": "0.00"}, "max": {"amount": "27.00"}}`
- ✅ **Multiple Aggregations**: Gleichzeitige sum, count, avg
- ✅ **Aggregation + Filter**: Filter reduziert Datenbasis für Aggregation
- ✅ **Search Parameter**: Volltext-Suche findet "Test"-Eintrag
- ✅ **Search + Filter**: Kombinierte Such- und Filter-Queries

### MCP-Tool-Tests (test_mcp_aggregations.py)
- ✅ **Alle Aggregations-Typen**: Vollständig über MCP-Tools verfügbar
- ✅ **JSON-Parameter-Parsing**: Korrekte Konvertierung von JSON-Strings
- ✅ **Structured Output**: Klare Trennung von Metadaten und Ergebnissen
- ✅ **Kombinierte Queries**: Search + Filter + Aggregation + Sortierung
- ✅ **Error Handling**: Ungültiges JSON wird korrekt abgefangen

## 🎯 Performance-Vorteile

### Netzwerk-Optimierung
- **Aggregationen**: Server-seitige Berechnung → weniger Datenübertragung
- **Search**: Database-optimierte Volltext-Suche → schneller als Client-Filterung
- **Kombinierte Queries**: Ein Request statt mehrere → reduzierte Latenz

### Analytische Möglichkeiten
- **Real-time Analytics**: Sofortige Berechnung von KPIs
- **Flexible Dashboards**: Beliebige Aggregations-Kombinationen
- **Filtered Analytics**: Aggregationen nur für relevante Datensätze

## 🚀 Nächste Schritte

Die Aggregations- und Search-Implementation ist **vollständig produktionsreif**! Sie können jetzt:

1. **Analytische Dashboards** für Ihre Laufdaten erstellen
2. **Performance-KPIs** in Echtzeit berechnen
3. **Flexible Such-Queries** für beliebige Datenexploration
4. **Kombinierte Analytics** mit Filtern, Suche und Aggregationen

Die Features folgen den **SQL-Standards** und bieten die gleiche Mächtigkeit wie Business-Intelligence-Tools! 📊🚀
