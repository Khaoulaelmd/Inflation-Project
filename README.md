# 🚀 Dashboard d'Inflation - Backend Flask

Backend complet pour le système de gestion d'inflation avec authentification, base de données MySQL et API REST.

## 📋 Prérequis

- **Python 3.8+** installé
- **XAMPP** installé et configuré
- **MySQL** démarré via XAMPP
- **phpMyAdmin** accessible

## 🛠️ Installation

### 1. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

### 2. Démarrer XAMPP
- Lancer XAMPP Control Panel
- Démarrer **Apache** et **MySQL**
- Vérifier que MySQL fonctionne sur le port 3306

### 3. Créer la base de données
- Ouvrir phpMyAdmin: http://localhost/phpmyadmin
- Créer une nouvelle base de données: `inflation_db`
- Importer le fichier `database_setup.sql`

### 4. Vérifier la configuration
- Modifier `config.py` si nécessaire
- Vérifier les paramètres de connexion MySQL

## 🚀 Démarrage

### Option 1: Script de démarrage (recommandé)
```bash
python run.py
```

### Option 2: Directement avec Flask
```bash
python app.py
```

### Option 3: Variable d'environnement
```bash
set FLASK_ENV=development
flask run
```

## 🌐 Accès

- **Application**: http://localhost:5000
- **API Test**: http://localhost:5000/api/test
- **phpMyAdmin**: http://localhost/phpmyadmin

## 📊 Structure de la Base de Données

### Tables principales:
- **`user`** - Utilisateurs et authentification
- **`indicator`** - Indicateurs économiques
- **`indicator_history`** - Historique des indicateurs
- **`forecast`** - Prévisions d'inflation
- **`report`** - Rapports mensuels
- **`recommendation`** - Recommandations
- **`feedback`** - Retours utilisateurs
- **`regional_alert`** - Alertes régionales

## 🔐 Authentification

### Utilisateur par défaut:
- **Email**: admin@inflation.ma
- **Mot de passe**: admin123
- **Rôle**: admin

### Endpoints d'authentification:
- `POST /api/register` - Créer un compte
- `POST /api/login` - Se connecter
- `POST /api/forgot-password` - Mot de passe oublié

## 📡 API Endpoints

### Indicateurs
- `GET /api/indicators` - Liste des indicateurs
- `GET /api/indicators/<id>/history` - Historique d'un indicateur

### Prévisions
- `POST /api/forecasts` - Créer une prévision
- `GET /api/forecasts` - Liste des prévisions

### Rapports
- `GET /api/reports` - Liste des rapports

### Utilisateurs (Admin seulement)
- `GET /api/users` - Liste des utilisateurs
- `POST /api/users` - Créer un utilisateur

### Autres
- `GET /api/alerts` - Alertes régionales
- `GET /api/feedback` - Feedback utilisateurs
- `POST /api/feedback` - Créer un feedback

## 🔧 Configuration

### Variables d'environnement:
```bash
FLASK_ENV=development
SECRET_KEY=votre_cle_secrete
DATABASE_URL=mysql://root:@localhost/inflation_db
```

### Configuration MySQL:
- **Host**: localhost
- **Port**: 3306
- **Database**: inflation_db
- **User**: root
- **Password**: (vide par défaut)

## 🧪 Test de l'API

### Test de connexion:
```bash
curl http://localhost:5000/api/test
```

### Test d'authentification:
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@inflation.ma","password":"admin123"}'
```

## 🐛 Dépannage

### Erreur de connexion MySQL:
- Vérifier que XAMPP est démarré
- Vérifier le port MySQL (3306)
- Vérifier les paramètres de connexion

### Erreur de dépendances:
```bash
pip install --upgrade -r requirements.txt
```

### Erreur de port:
- Vérifier qu'aucune autre application n'utilise le port 5000
- Modifier le port dans `run.py` si nécessaire

## 📁 Structure des Fichiers

```
📁 Backend/
├── 📄 app.py              # Application Flask principale
├── 📄 config.py           # Configuration
├── 📄 run.py              # Script de démarrage
├── 📄 requirements.txt    # Dépendances Python
├── 📄 database_setup.sql  # Script SQL
└── 📄 README.md           # Documentation
```

## 🔄 Mise à jour

### Mettre à jour les dépendances:
```bash
pip install --upgrade -r requirements.txt
```

### Mettre à jour la base de données:
- Exécuter les nouveaux scripts SQL dans phpMyAdmin
- Ou utiliser les migrations Flask (à implémenter)

## 📞 Support

Pour toute question ou problème:
1. Vérifier la documentation
2. Consulter les logs Flask
3. Vérifier la connexion MySQL
4. Tester les endpoints API

---

**🎯 Objectif**: Fournir un backend robuste et sécurisé pour la gestion des indicateurs d'inflation avec authentification et base de données relationnelle.
