# Script PowerShell de démarrage pour dabahere.com
Write-Host "Demarrage de dabahere.com..." -ForegroundColor Green

# Vérifier si Docker est installé
try {
    docker --version | Out-Null
    Write-Host "Docker detecte" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker n'est pas installé. Veuillez installer Docker Desktop d'abord." -ForegroundColor Red
    exit 1
}

# Vérifier si Docker Compose est installé
try {
    docker compose version | Out-Null
    Write-Host "Docker Compose detecte" -ForegroundColor Green
} catch {
    Write-Host "❌ Docker Compose n'est pas installé." -ForegroundColor Red
    exit 1
}

# Arrêter les conteneurs existants
Write-Host "Arret des conteneurs existants..." -ForegroundColor Yellow
docker compose down

# Supprimer les conteneurs orphelins
Write-Host "Nettoyage des conteneurs orphelins..." -ForegroundColor Yellow
docker container prune -f

# Démarrer les services
Write-Host "Demarrage des services..." -ForegroundColor Yellow
docker compose up -d

# Attendre que les services soient prêts
Write-Host "Attente du demarrage des services..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Vérifier le statut des conteneurs
Write-Host "Statut des conteneurs :" -ForegroundColor Cyan
docker compose ps

# Afficher les URLs d'accès
Write-Host ""
Write-Host "URLs d'acces :" -ForegroundColor Green
Write-Host "   Application principale : http://localhost" -ForegroundColor White
Write-Host "   Application principale : http://dabahere.com (si DNS configuré)" -ForegroundColor White
Write-Host "   phpMyAdmin : http://localhost/phpmyadmin/" -ForegroundColor White
Write-Host "   API Backend : http://localhost/api/" -ForegroundColor White
Write-Host ""
Write-Host "Logs en temps reel :" -ForegroundColor Cyan
Write-Host "   docker compose logs -f" -ForegroundColor White
Write-Host ""
Write-Host "Pour arrêter :" -ForegroundColor Cyan
Write-Host "   docker compose down" -ForegroundColor White
Write-Host ""
Write-Host "dabahere.com est pret !" -ForegroundColor Green
