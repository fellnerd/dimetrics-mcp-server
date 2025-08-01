"""
Schnell-Demo der Attribute-Funktionalität für GitHub Copilot.
"""

import asyncio
from dimetrics_mcp_server.__main__ import list_attributes, create_attribute

async def quick_demo():
    """Schnelle Demo der wichtigsten Attribute-Funktionen."""
    print("🏷️  DIMETRICS ATTRIBUTE MANAGEMENT - QUICK DEMO")
    print("=" * 60)
    
    # Verwende eine bekannte Resource
    resource_name = "limgrLizenzverwaltung"
    print(f"🎯 Demo mit Resource: '{resource_name}'")
    print()
    
    # 1. Liste bestehende Attribute
    print("1️⃣  Aktuelle Attribute auflisten:")
    result = await list_attributes(resource_name, page_size=5)
    
    if result.get("success"):
        count = result.get("count", 0)
        print(f"   ✅ {count} Attribute gefunden")
        
        for i, attr in enumerate(result.get("attributes", [])[:3]):
            print(f"   {i+1}. {attr['name']} ({attr['type']}) - {attr['label']}")
    
    print()
    
    # 2. Erstelle ein neues Attribut
    print("2️⃣  Neues Attribut erstellen:")
    
    import time
    unique_name = f"demo_field_{int(time.time())}"
    
    create_result = await create_attribute(
        resource_name=resource_name,
        name=unique_name,
        attribute_type="INPUT_FIELD",
        label="Demo Feld",
        description="Von GitHub Copilot via MCP erstellt",
        placeholder="Beispiel-Eingabe...",
        required=False
    )
    
    if create_result.get("success"):
        print(f"   ✅ Attribut '{unique_name}' erfolgreich erstellt")
        print(f"   🆔 ID: {create_result['attribute']['object_id']}")
    else:
        print(f"   ❌ Fehler: {create_result.get('error')}")
    
    print()
    print("🏁 Demo abgeschlossen!")
    print()
    print("💡 GitHub Copilot kann jetzt folgende Attribute-Befehle nutzen:")
    print("   • list_attributes(resource_name)")
    print("   • create_attribute(resource_name, name, type, label, ...)")
    print("   • get_attribute_details(resource_name, attribute_id)")
    print("   • update_attribute(resource_name, attribute_id, ...)")
    print("   • delete_attribute(resource_name, attribute_id)")

if __name__ == "__main__":
    asyncio.run(quick_demo())
