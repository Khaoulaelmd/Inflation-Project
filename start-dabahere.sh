#!/bin/bash

# Script de démarrage pour dabahere.com
echo "🚀 Démarrage de dabahere.com..."

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker d'abord."
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez installer Docker Compose d'abord."
    exit 1
fi

# Arrêter les conteneurs existants
echo "🛑 Arrêt des conteneurs existants..."
docker compose down

# Supprimer les conteneurs orphelins
echo "🧹 Nettoyage des conteneurs orphelins..."
docker container prune -f

# Démarrer les services
echo "🔧 Démarrage des services..."
docker compose up -d

# Attendre que les services soient prêts
echo "⏳ Attente du démarrage des services..."
sleep 10

# Vérifier le statut des conteneurs
echo "📊 Statut des conteneurs :"
docker compose ps

# Afficher les URLs d'accès
echo ""
echo "🌐 URLs d'accès :"
echo "   Application principale : http://localhost"
echo "   Application principale : http://dabahere.com (si DNS configuré)"
echo "   phpMyAdmin : http://localhost/phpmyadmin/"
echo "   API Backend : http://localhost/api/"
echo ""
echo "📝 Logs en temps réel :"
echo "   docker compose logs -f"
echo ""
echo "🛑 Pour arrêter :"
echo "   docker compose down"
echo ""
echo "✅ dabahere.com est prêt !"
