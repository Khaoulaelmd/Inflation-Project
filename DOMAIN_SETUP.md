# Configuration du domaine dabahere.com

## Vue d'ensemble

Ce projet est maintenant configuré pour fonctionner avec le domaine `dabahere.com`. La configuration utilise Nginx comme reverse proxy pour gérer le trafic HTTP/HTTPS et rediriger vers l'application Flask.

## Structure de configuration

```
nginx/
├── nginx.conf              # Configuration principale Nginx
├── conf.d/
│   └── dabahere.com.conf   # Configuration spécifique au domaine
└── ssl/
    ├── dabahere.com.crt    # Certificat SSL (à générer)
    ├── dabahere.com.key    # Clé privée SSL (à générer)
    └── generate-ssl.sh     # Script pour générer des certificats auto-signés
```

## Étapes de configuration

### 1. Configuration DNS sur Hostinger

Connectez-vous à votre compte Hostinger avec :
- **Email**: jbn.nsekuye@gmail.com
- **Mot de passe**: Isicod_2023.Remote

Dans le panneau de contrôle Hostinger :
1. Allez dans "Domaines" → "dabahere.com"
2. Configurez les enregistrements DNS :
   - **A Record**: `@` → `VOTRE_IP_SERVEUR`
   - **A Record**: `www` → `VOTRE_IP_SERVEUR`
   - **CNAME Record**: `www` → `dabahere.com`

### 2. Génération des certificats SSL

#### Pour le développement (certificats auto-signés) :
```bash
# Dans le conteneur Nginx
docker exec -it inflation_nginx bash
cd /etc/nginx/ssl
chmod +x generate-ssl.sh
./generate-ssl.sh
```

#### Pour la production (Let's Encrypt) :
```bash
# Installer Certbot
apt-get update
apt-get install certbot python3-certbot-nginx

# Générer le certificat
certbot --nginx -d dabahere.com -d www.dabahere.com
```

### 3. Démarrage de l'application

```bash
# Démarrer tous les services
docker compose up -d

# Vérifier que tous les conteneurs sont en cours d'exécution
docker compose ps
```

### 4. Test de l'application

- **Application principale**: https://dabahere.com
- **phpMyAdmin**: https://dabahere.com/phpmyadmin/
- **API Backend**: https://dabahere.com/api/

## Configuration des services

### Services Docker
- **nginx**: Reverse proxy (ports 80, 443)
- **backend**: Application Flask (port 5000)
- **mysql**: Base de données (port 3306)
- **phpmyadmin**: Interface d'administration MySQL (port 8081)
- **agents**: Service d'agents d'inflation
- **jobs**: Service de traitement des données

### Réseau
Tous les services sont connectés au réseau `inflation_network` pour la communication interne.

## Sécurité

### Headers de sécurité configurés :
- `X-Frame-Options: DENY`
- `X-Content-Type-Options: nosniff`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`

### Configuration SSL :
- Protocoles : TLSv1.2, TLSv1.3
- Chiffrement : ECDHE-RSA-AES128-GCM-SHA256, ECDHE-RSA-AES256-GCM-SHA384
- Cache de session SSL activé

## Dépannage

### Problème de port MySQL
Si vous obtenez une erreur de port MySQL :
```bash
# Arrêter le service MySQL local
sudo service mysql stop
# ou
sudo systemctl stop mysql
```

### Vérifier les logs Nginx
```bash
docker logs inflation_nginx
```

### Vérifier la configuration Nginx
```bash
docker exec inflation_nginx nginx -t
```

### Redémarrer les services
```bash
docker compose restart nginx
```

## Prochaines étapes

1. **Configurer les certificats SSL** avec Let's Encrypt pour la production
2. **Configurer un firewall** sur le serveur
3. **Mettre en place des sauvegardes** automatiques de la base de données
4. **Configurer la surveillance** et les alertes
5. **Optimiser les performances** (cache, compression, etc.)

## Support

Pour toute question ou problème, consultez :
- Les logs Docker : `docker compose logs`
- La documentation Nginx : https://nginx.org/en/docs/
- La documentation Hostinger : https://www.hostinger.com/help
