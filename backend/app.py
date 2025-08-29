from flask import Flask, request, jsonify, session, send_from_directory, redirect
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_cle_secrete_tres_longue_et_complexe'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inflation.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
CORS(app, supports_credentials=True)

# Dossier racine pour servir les fichiers frontend
BASE_DIR = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend', 'public'))

# Routes pour servir le frontend
@app.route('/')
def root():
    # Redirige vers home.html pour la page d'accueil
    return redirect('/home.html')

@app.route('/<path:filename>')
def serve_static_file(filename):
    # Sert tout fichier présent dans le dossier frontend/public
    return send_from_directory(BASE_DIR, filename)

# Modèles de base de données
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='analyste')  # admin_principal, admin_secondaire, analyste
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

class Indicator(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(50), unique=True, nullable=False)
    current_value = db.Column(db.Float, nullable=False)
    previous_value = db.Column(db.Float, nullable=False)
    change_percent = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class IndicatorHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    indicator_id = db.Column(db.Integer, db.ForeignKey('indicator.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    period = db.Column(db.String(10), nullable=False)  # 6m, 12m, 24m

class Forecast(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    inflation_forecast = db.Column(db.Float, nullable=False)
    scenario = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status = db.Column(db.String(20), default='pending')

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    period = db.Column(db.String(50), nullable=False)
    inflation_observed = db.Column(db.Float, nullable=False)
    analysis = db.Column(db.Text, nullable=False)
    decision = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Recommendation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recommendation_type = db.Column(db.String(100), nullable=False)
    institution = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    forecast_id = db.Column(db.Integer, db.ForeignKey('forecast.id'), nullable=True)
    period = db.Column(db.String(50), nullable=True)
    feedback_type = db.Column(db.String(20), nullable=False)  # positif, neutre, negatif
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)

class RegionalAlert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(50), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    description = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

# Décorateur pour vérifier l'authentification
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token manquant'}), 401
        
        try:
            token = token.split(' ')[1]  # Enlever 'Bearer '
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.get(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Utilisateur invalide'}), 401
        except:
            return jsonify({'message': 'Token invalide'}), 401
        
        return f(current_user, *args, **kwargs)
    return decorated

# Décorateur pour vérifier les rôles
def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(current_user, *args, **kwargs):
            if current_user.role not in allowed_roles:
                return jsonify({'message': 'Accès non autorisé'}), 403
            return f(current_user, *args, **kwargs)
        return decorated
    return decorator

# Routes d'authentification
@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    if not email or not password or not role:
        return jsonify({'message': 'Tous les champs sont requis'}), 400
    
    user = User.query.filter_by(email=email, role=role).first()
    
    if user and check_password_hash(user.password_hash, password):
        if not user.is_active:
            return jsonify({'message': 'Compte désactivé'}), 401
        
        token = jwt.encode({
            'user_id': user.id,
            'email': user.email,
            'role': user.role,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, app.config['SECRET_KEY'], algorithm='HS256')
        
        return jsonify({
            'token': token,
            'user': {
                'id': user.id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'role': user.role
            }
        })
    
    return jsonify({'message': 'Identifiants invalides'}), 401

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email déjà utilisé'}), 400
    
    hashed_password = generate_password_hash(data['password'])
    new_user = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password_hash=hashed_password,
        role=data.get('role', 'analyste')
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'Utilisateur créé avec succès'}), 201

# Routes pour les indicateurs
@app.route('/api/indicators', methods=['GET'])
@token_required
def get_indicators(current_user):
    indicators = Indicator.query.all()
    return jsonify([{
        'id': ind.id,
        'name': ind.name,
        'code': ind.code,
        'current_value': ind.current_value,
        'previous_value': ind.previous_value,
        'change_percent': ind.change_percent,
        'unit': ind.unit,
        'category': ind.category,
        'last_updated': ind.last_updated.isoformat()
    } for ind in indicators])

# Routes pour la gestion des analystes (admin secondaire)
@app.route('/api/analystes', methods=['GET'])
@token_required
@role_required(['admin_principal', 'admin_secondaire'])
def get_analystes(current_user):
    analystes = User.query.filter_by(role='analyste').all()
    return jsonify([{
        'id': user.id,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_active': user.is_active,
        'created_at': user.created_at.isoformat()
    } for user in analystes])

@app.route('/api/analystes', methods=['POST'])
@token_required
@role_required(['admin_principal', 'admin_secondaire'])
def create_analyste(current_user):
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email déjà utilisé'}), 400
    
    hashed_password = generate_password_hash(data['password'])
    new_analyste = User(
        first_name=data['first_name'],
        last_name=data['last_name'],
        email=data['email'],
        password_hash=hashed_password,
        role='analyste',
        is_active=data.get('is_active', True)
    )
    
    db.session.add(new_analyste)
    db.session.commit()
    
    return jsonify({'message': 'Analyste créé avec succès'}), 201

@app.route('/api/analystes/<int:user_id>', methods=['PUT'])
@token_required
@role_required(['admin_principal', 'admin_secondaire'])
def update_analyste(current_user, user_id):
    user = User.query.get_or_404(user_id)
    if user.role != 'analyste':
        return jsonify({'message': 'Utilisateur non trouvé'}), 404
    
    data = request.get_json()
    
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'email' in data:
        if User.query.filter_by(email=data['email']).filter(User.id != user_id).first():
            return jsonify({'message': 'Email déjà utilisé'}), 400
        user.email = data['email']
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    db.session.commit()
    return jsonify({'message': 'Analyste mis à jour avec succès'})

@app.route('/api/analystes/<int:user_id>', methods=['DELETE'])
@token_required
@role_required(['admin_principal', 'admin_secondaire'])
def delete_analyste(current_user, user_id):
    user = User.query.get_or_404(user_id)
    if user.role != 'analyste':
        return jsonify({'message': 'Utilisateur non trouvé'}), 404
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Analyste supprimé avec succès'})

# Routes pour les prévisions
@app.route('/api/forecasts', methods=['GET'])
@token_required
def get_forecasts(current_user):
    if current_user.role in ['admin_principal', 'admin_secondaire']:
        forecasts = Forecast.query.all()
    else:
        forecasts = Forecast.query.filter_by(user_id=current_user.id).all()
    
    return jsonify([{
        'id': f.id,
        'start_date': f.start_date.isoformat(),
        'end_date': f.end_date.isoformat(),
        'inflation_forecast': f.inflation_forecast,
        'scenario': f.scenario,
        'status': f.status,
        'created_at': f.created_at.isoformat()
    } for f in forecasts])

@app.route('/api/forecasts', methods=['POST'])
@token_required
def create_forecast(current_user):
    data = request.get_json()
    
    new_forecast = Forecast(
        user_id=current_user.id,
        start_date=datetime.datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
        inflation_forecast=data['inflation_forecast'],
        scenario=data['scenario']
    )
    
    db.session.add(new_forecast)
    db.session.commit()
    
    return jsonify({'message': 'Prévision créée avec succès'}), 201

# Routes pour les rapports
@app.route('/api/reports', methods=['GET'])
@token_required
def get_reports(current_user):
    reports = Report.query.all()
    return jsonify([{
        'id': r.id,
        'title': r.title,
        'period': r.period,
        'inflation_observed': r.inflation_observed,
        'analysis': r.analysis,
        'decision': r.decision,
        'created_at': r.created_at.isoformat()
    } for r in reports])

# Route pour obtenir les statistiques des analystes
@app.route('/api/analystes/stats', methods=['GET'])
@token_required
@role_required(['admin_principal', 'admin_secondaire'])
def get_analystes_stats(current_user):
    total_analystes = User.query.filter_by(role='analyste').count()
    analystes_actifs = User.query.filter_by(role='analyste', is_active=True).count()
    analystes_inactifs = User.query.filter_by(role='analyste', is_active=False).count()
    
    # Nouveaux analystes ce mois
    now = datetime.datetime.utcnow()
    debut_mois = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    nouveaux_analystes = User.query.filter(
        User.role == 'analyste',
        User.created_at >= debut_mois
    ).count()
    
    return jsonify({
        'total_analystes': total_analystes,
        'analystes_actifs': analystes_actifs,
        'analystes_inactifs': analystes_inactifs,
        'nouveaux_analystes': nouveaux_analystes
    })

# Route pour rediriger vers la bonne page selon le rôle
@app.route('/api/auth/redirect', methods=['POST'])
@token_required
def redirect_user(current_user):
    if current_user.role == 'admin_principal':
        return jsonify({'redirect': '/index.html'})
    elif current_user.role == 'admin_secondaire':
        return jsonify({'redirect': '/index2.html'})
    else:
        return jsonify({'redirect': '/index.html'})

# Création de la base de données
with app.app_context():
    db.create_all()
    
    # Créer des utilisateurs de test si la base est vide
    if not User.query.first():
        # Admin Principal
        admin_principal = User(
            first_name='Admin',
            last_name='Principal',
            email='admin.principal@bgi.gov.ma',
            password_hash=generate_password_hash('admin123'),
            role='admin_principal'
        )
        
        # Admin Secondaire
        admin_secondaire = User(
            first_name='Admin',
            last_name='Secondaire',
            email='admin.secondaire@bgi.gov.ma',
            password_hash=generate_password_hash('admin123'),
            role='admin_secondaire'
        )
        
        # Analyste de test
        analyste = User(
            first_name='Analyste',
            last_name='Test',
            email='analyste@bgi.gov.ma',
            password_hash=generate_password_hash('analyste123'),
            role='analyste'
        )
        
        db.session.add(admin_principal)
        db.session.add(admin_secondaire)
        db.session.add(analyste)
        db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
