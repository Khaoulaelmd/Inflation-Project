import os
from datetime import timedelta

class Config:
    """Configuration de base"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'votre_cle_secrete_tres_longue_et_complexe_2025'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'votre_jwt_secret_tres_longue_et_complexe_2025'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)

class DevelopmentConfig(Config):
    """Configuration pour le développement"""
    DEBUG = True
                               SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                'mysql+pymysql://root:@localhost/inflation_db?charset=utf8mb4'
    CORS_ORIGINS = ['http://localhost:5000', 'http://127.0.0.1:5000']

class ProductionConfig(Config):
    """Configuration pour la production"""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '').split(',')

class TestingConfig(Config):
    """Configuration pour les tests"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CORS_ORIGINS = ['http://localhost:5000']

# Dictionnaire des configurations
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
