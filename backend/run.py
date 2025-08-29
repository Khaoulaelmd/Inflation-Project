#!/usr/bin/env python3
"""
Script de démarrage pour l'application Flask
Usage: python run.py
"""

import os
from app import app, db

if __name__ == '__main__':
    # Configuration de l'environnement
    env = os.environ.get('FLASK_ENV', 'development')
    
    print(f"🚀 Démarrage du Dashboard d'Inflation en mode {env}")
    print("📊 Backend Flask avec base de données MySQL")
    print("🌐 Serveur accessible sur: http://localhost:5000")
    print("📖 Documentation API: http://localhost:5000/api/test")
    
    # Créer les tables si elles n'existent pas
    with app.app_context():
        try:
            db.create_all()
            print("✅ Base de données initialisée")
        except Exception as e:
            print(f"⚠️  Erreur base de données: {e}")
            print("💡 Assurez-vous que XAMPP et MySQL sont démarrés")
    
    # Démarrer l'application
    app.run(
    host='0.0.0.0',  # Permet l'accès depuis n'importe quelle IP
    port=5000,
    debug=(env == 'development')
)
@app.route("/")
def home():
    return "Bienvenue sur Inflation-Project !"

 

