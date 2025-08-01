#!/bin/bash

# Installationsskript für den Dimetrics MCP Server

echo "🚀 Installiere Dimetrics MCP Server..."

# Python-Abhängigkeiten installieren
echo "📦 Installiere Python-Abhängigkeiten..."
pip install -r requirements.txt

# .env Datei erstellen falls sie nicht existiert
if [ ! -f .env ]; then
    echo "🔧 Erstelle .env Datei..."
    cp .env.example .env
    echo "⚠️  Bitte bearbeiten Sie die .env Datei und tragen Sie Ihre Dimetrics API-Zugangsdaten ein!"
fi

# Test ob der Server startet
echo "🧪 Teste MCP Server..."
timeout 5s python -m dimetrics_mcp_server &
SERVER_PID=$!

sleep 2

if kill -0 $SERVER_PID 2>/dev/null; then
    echo "✅ MCP Server läuft erfolgreich!"
    kill $SERVER_PID
else
    echo "❌ Fehler beim Starten des MCP Servers."
    exit 1
fi

echo ""
echo "🎉 Installation abgeschlossen!"
echo ""
echo "Nächste Schritte:"
echo "1. Bearbeiten Sie die .env Datei mit Ihren Dimetrics API-Zugangsdaten"
echo "2. Konfigurieren Sie Ihren MCP-Client mit der Konfiguration aus mcp_config_example.json"
echo "3. Starten Sie den Server mit: python -m dimetrics_mcp_server"
echo ""
