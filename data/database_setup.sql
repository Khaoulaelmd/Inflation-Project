<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>Rapport du projet – Inflation Project</title>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;line-height:1.45;padding:20px;}
    .btn{background:#394b76;color:#fff;border:none;padding:10px 16px;border-radius:6px;cursor:pointer}
  </style>
  <script>
    function buildReportDoc(){
      const { jsPDF } = window.jspdf;
      const doc = new jsPDF({ unit:'pt', format:'a4' });
      const left = 40, line = 18; let y = 60;

      function h1(text){ doc.setFontSize(18); doc.text(text, left, y); y += 28; }
      function h2(text){ doc.setFontSize(14); doc.text(text, left, y); y += 22; }
      function p(text){
        doc.setFontSize(11);
        const lines = doc.splitTextToSize(text, 515);
        doc.text(lines, left, y); y += line * lines.length + 6;
      }
      function bullet(items){
        doc.setFontSize(11);
        items.forEach(t=>{ const lines = doc.splitTextToSize('• '+t, 515); doc.text(lines, left, y); y += line * lines.length; });
        y += 6;
      }
      function pageBreak(min){ if(y>740-min){ doc.addPage(); y=60; } }

      // Cover
      doc.setFontSize(22); doc.text('Rapport détaillé – Inflation Project', left, y); y+=34;
      doc.setFontSize(12); doc.text('Date: '+new Date().toLocaleDateString(), left, y); y+=30;
      p('Objectif: Construire un tableau de bord d’inflation avec authentification, visualisation, prévisions et rapports. Données applicatives en SQLite pour le développement et espace "agents" en MySQL pour l’ingestion fine.');

      pageBreak(300); h1('Architecture');
      h2('Frontend');
      bullet([
        'Pages: login.html, signup.html, index.html (dashboard)',
        'Librairies: TailwindCSS, Font Awesome, Chart.js, jsPDF',
        'Servi statiquement par le backend (GET / redirige vers login.html)'
      ]);
      h2('Backend (Flask)');
      bullet([
        'Auth JWT, CORS, SQLAlchemy',
        'API REST pour indicateurs, prévisions, rapports, utilisateurs',
        'SQLite par défaut: sqlite:///inflation.db',
        'Blueprints optionnels: api/agents, api/indicators (MySQL)'
      ]);
      h2('Agents (MySQL)');
      bullet([
        'Tables: data_source, sub_indicator, sub_indicator_history, ingest_run',
        'Endpoints: GET /api/agents/sources, GET /api/agents/subindicators, POST /api/agents/run/{code}'
      ]);

      pageBreak(360); h1('Flux utilisateur');
      bullet([
        'Accès http://localhost:5000 → redirection vers login.html',
        'Connexion (POST /api/login) → stockage token JWT',
        'Redirection vers index.html, vérification de session, chargement /api/indicators',
        'Sections: Dashboard, Prévisions (avec export PDF), Rapports, Recommandations, Qualité, Alertes'
      ]);

      h1('API principale (SQLite)');
      p('Principales routes: /api/register, /api/login, /api/indicators, /api/indicators/{id}/history, /api/forecasts, /api/reports, /api/recommendations, /api/feedback, /api/users, /api/init-db.');

      pageBreak(380); h1('Démarrage (dev – SQLite)');
      p('1) cd backend; créer venv; pip install -r requirements.txt; python app.py. 2) Initialiser la base: POST /api/init-db. 3) Ouvrir http://localhost:5000, se connecter (admin@inflation.ma / admin123).');

      h1('Démarrage (MySQL / Agents)');
      p('1) Créer base inflation_db et importer le schéma agents minimal. 2) Lancer le backend avec DATABASE_URL=mysql+pymysql://root:@localhost:3306/inflation_db. 3) Tester: /api/agents/sources, /api/agents/subindicators?code=..., POST /api/agents/run/{code}.');

      pageBreak(380); h1('Sécurité & bonnes pratiques');
      bullet([
        'JWT signé par SECRET_KEY (env en production)',
        'Mots de passe hashés (Werkzeug)',
        'CORS activé',
        'Envisager cookies HttpOnly et migrations (Flask-Migrate) pour la prod'
      ]);

      h1('Évolutions réalisées');
      bullet([
        'Backend sert frontend/public et redirige / vers login.html',
        'Redirection post-login → index.html',
        'Blueprints agents/indicators enregistrés si présents',
        'Guide d’utilisation PowerShell (Invoke-WebRequest vs curl.exe)'
      ]);

      h1('Pistes d’amélioration');
      bullet([
        'Worker agents qui consomme ingest_run et enrichit sub_indicator_history',
        'Unifier stockage sur MySQL en staging/prod',
        'Tests automatisés, CI/CD, monitoring'
      ]);

      return doc;
    }

    function downloadReport(){ const doc = buildReportDoc(); doc.save('Rapport_Inflation_Project.pdf'); }

    window.addEventListener('DOMContentLoaded', ()=>{
      // Téléchargement auto, laisser aussi un bouton manuel
      downloadReport();
    });
  </script>
</head>
<body>
  <h1>Rapport du projet – Inflation Project</h1>
  <p>Si le téléchargement ne démarre pas automatiquement, cliquez:</p>
  <button class="btn" onclick="downloadReport()">Télécharger le PDF</button>
</body>
</html>


