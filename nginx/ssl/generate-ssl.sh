#!/bin/bash

# Script pour générer des certificats SSL auto-signés pour dabahere.com
# À utiliser uniquement pour le développement

DOMAIN="dabahere.com"
SSL_DIR="/etc/nginx/ssl"

# Créer le répertoire SSL s'il n'existe pas
mkdir -p $SSL_DIR

# Générer la clé privée
openssl genrsa -out $SSL_DIR/$DOMAIN.key 2048

# Générer le certificat auto-signé
openssl req -new -x509 -key $SSL_DIR/$DOMAIN.key -out $SSL_DIR/$DOMAIN.crt -days 365 -subj "/C=MA/ST=Morocco/L=Casablanca/O=Dabahere/OU=IT/CN=$DOMAIN"

# Définir les permissions appropriées
chmod 600 $SSL_DIR/$DOMAIN.key
chmod 644 $SSL_DIR/$DOMAIN.crt

echo "Certificats SSL générés pour $DOMAIN"
echo "Certificat: $SSL_DIR/$DOMAIN.crt"
echo "Clé privée: $SSL_DIR/$DOMAIN.key"
echo ""
echo "⚠️  ATTENTION: Ces certificats sont auto-signés et ne sont pas sécurisés pour la production."
echo "Pour la production, utilisez Let's Encrypt ou un autre fournisseur de certificats SSL."
