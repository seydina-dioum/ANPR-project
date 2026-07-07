let selectedFile = null;

// =====================
// ONGLETS
// =====================
function showTab(tab) {
    // Cacher tous les contenus
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));

    // Afficher le bon onglet
    document.getElementById('tab-' + tab).classList.add('active');
    document.getElementById('tab-btn-' + tab).classList.add('active');

    // Si webcam → démarrer la caméra
    if (tab === 'webcam') {
        startWebcam();
    }
}

// =====================
// DRAG & DROP
// =====================
document.addEventListener('DOMContentLoaded', function() {
    const uploadZone = document.getElementById('upload-zone');
    if (!uploadZone) return;

    ['dragenter', 'dragover'].forEach(evt => {
        uploadZone.addEventListener(evt, function(e) {
            e.preventDefault();
            e.stopPropagation();
            uploadZone.classList.add('drag-over');
        });
    });

    ['dragleave', 'drop'].forEach(evt => {
        uploadZone.addEventListener(evt, function(e) {
            e.preventDefault();
            e.stopPropagation();
            uploadZone.classList.remove('drag-over');
        });
    });

    uploadZone.addEventListener('drop', function(e) {
        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    });
});

// =====================
// UPLOAD IMAGE
// =====================
document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;
    handleFile(file);
});

function handleFile(file) {
    // Vérifier le type (avec fallback par extension si file.type est vide)
    const validExtensions = ['jpg', 'jpeg', 'png', 'webp', 'gif', 'bmp'];
    const ext = file.name.split('.').pop().toLowerCase();
    const isImage = file.type.startsWith('image/') || validExtensions.includes(ext);

    if (!isImage) {
        showNotification('Veuillez sélectionner une image (JPG, PNG, WEBP).', 'error');
        return;
    }

    selectedFile = file;
    const reader = new FileReader();
    reader.onload = function(e) {
        const preview = document.getElementById('preview');
        const detectSection = document.getElementById('detect-section');
        const results = document.getElementById('results');

        if (preview) preview.src = e.target.result;
        if (detectSection) detectSection.style.display = 'block';
        if (results) results.style.display = 'none';

        // Scroll vers la preview
        if (detectSection) {
            setTimeout(function() {
                detectSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
            }, 100);
        }
    };
    reader.onerror = function() {
        showNotification('Erreur lors de la lecture du fichier.', 'error');
    };
    reader.readAsDataURL(file);
}

// =====================
// WEBCAM
// =====================
function startWebcam() {
    const video = document.getElementById('video');
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
        })
        .catch(err => {
            showNotification("Impossible d'accéder à la webcam : " + err.message, 'error');
        });
}

function captureWebcam() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    canvas.getContext('2d').drawImage(video, 0, 0);

    // Convertir en fichier
    canvas.toBlob(function(blob) {
        selectedFile = new File([blob], "webcam.jpg", { type: "image/jpeg" });
        document.getElementById('preview').src = canvas.toDataURL('image/jpeg');
        document.getElementById('detect-section').style.display = 'block';
        document.getElementById('results').style.display = 'none';
        document.getElementById('detect-section').scrollIntoView({ behavior: 'smooth', block: 'center' });
    }, 'image/jpeg');
}

// =====================
// DETECTION
// =====================
async function detectPlate() {
    if (!selectedFile) {
        showNotification("Veuillez choisir une image d'abord !", 'error');
        return;
    }

    // Afficher le chargement
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';

    // Désactiver le bouton
    const btnDetect = document.getElementById('btn-detect');
    btnDetect.disabled = true;
    btnDetect.textContent = '⏳ Analyse en cours…';

    // Préparer la requête
    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
        const response = await fetch('/api/detect', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        // Cacher le chargement
        document.getElementById('loading').style.display = 'none';

        // Réactiver le bouton
        btnDetect.disabled = false;
        btnDetect.textContent = '🔍 Détecter la plaque';

        if (!response.ok) {
            showNotification('Erreur : ' + (data.detail || 'Erreur serveur'), 'error');
            return;
        }

        // Afficher les résultats
        afficherResultats(data);

    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        btnDetect.disabled = false;
        btnDetect.textContent = '🔍 Détecter la plaque';
        showNotification("Erreur de connexion : " + error.message, 'error');
    }
}

// =====================
// AFFICHAGE RESULTATS
// =====================
function afficherResultats(data) {
    const resultsDiv = document.getElementById('results');
    const contentDiv = document.getElementById('results-content');
    const metaSpan = document.getElementById('results-meta');

    resultsDiv.style.display = 'block';

    if (data.nb_plaques === 0) {
        metaSpan.textContent = '';
        contentDiv.innerHTML = `
            <div class="no-result">
                <span class="no-result-icon">🔍</span>
                <div class="no-result-text">Aucune plaque détectée dans cette image.</div>
            </div>
        `;
        resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'center' });
        return;
    }

    metaSpan.textContent = `${data.nb_plaques} plaque(s) · ${data.temps_ms} ms`;

    let html = '';

    data.plaques.forEach((plaque, index) => {
        const classe = plaque.valide ? 'valide' : (plaque.verdict === 'DOUTEUSE' ? 'douteuse' : 'invalide');
        
        let badgeLabel, badgeClass;
        if (plaque.verdict === 'VALIDE') {
            badgeLabel = '✅ Valide';
            badgeClass = 'valide';
        } else if (plaque.verdict === 'DOUTEUSE') {
            badgeLabel = '⚠️ Douteuse';
            badgeClass = 'douteuse';
        } else {
            badgeLabel = '❌ Illisible';
            badgeClass = 'invalide';
        }

        const confDetect = (plaque.score_detection * 100).toFixed(1);
        const confOcr = (plaque.conf_ocr * 100).toFixed(1);

        // Déterminer la classe de la barre de confiance
        const confBarClass = confOcr >= 70 ? 'high' : confOcr >= 40 ? 'medium' : 'low';

        html += `
            <div class="plaque-card ${classe}" style="animation-delay: ${index * 0.1}s">
                <div class="plaque-texte">
                    ${plaque.texte}
                    <span class="badge ${badgeClass}">${badgeLabel}</span>
                </div>
                <div class="plaque-details">
                    <div class="detail-item">
                        <div class="detail-label">📝 Texte brut OCR</div>
                        <strong>${plaque.texte_brut || '—'}</strong>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">🎯 Confiance détection</div>
                        <strong>${confDetect}%</strong>
                        <div class="conf-bar-wrapper">
                            <div class="conf-bar ${parseFloat(confDetect) >= 70 ? 'high' : parseFloat(confDetect) >= 40 ? 'medium' : 'low'}" style="width: ${confDetect}%"></div>
                        </div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">🔤 Confiance OCR</div>
                        <strong>${confOcr}%</strong>
                        <div class="conf-bar-wrapper">
                            <div class="conf-bar ${confBarClass}" style="width: ${confOcr}%"></div>
                        </div>
                    </div>
                    <div class="detail-item">
                        <div class="detail-label">⚙️ Moteur OCR</div>
                        <strong>${plaque.moteur_ocr || 'EasyOCR'}</strong>
                    </div>
                </div>
            </div>
        `;
    });

    contentDiv.innerHTML = html;
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

// =====================
// NOTIFICATION
// =====================
function showNotification(message, type = 'info') {
    // Supprimer une notification existante
    const existing = document.querySelector('.notification');
    if (existing) existing.remove();

    const notif = document.createElement('div');
    notif.className = 'notification';
    notif.style.cssText = `
        position: fixed;
        top: 24px;
        right: 24px;
        padding: 16px 24px;
        border-radius: 12px;
        font-size: 14px;
        font-weight: 600;
        z-index: 1000;
        animation: fadeSlideIn 0.3s ease;
        max-width: 400px;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255,255,255,0.1);
        font-family: 'Inter', sans-serif;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    `;

    if (type === 'error') {
        notif.style.background = 'rgba(239,68,68,0.2)';
        notif.style.color = '#fca5a5';
        notif.style.borderColor = 'rgba(239,68,68,0.3)';
    } else {
        notif.style.background = 'rgba(59,130,246,0.2)';
        notif.style.color = '#93c5fd';
        notif.style.borderColor = 'rgba(59,130,246,0.3)';
    }

    notif.textContent = message;
    document.body.appendChild(notif);

    setTimeout(() => {
        notif.style.opacity = '0';
        notif.style.transform = 'translateY(-10px)';
        notif.style.transition = 'all 0.3s ease';
        setTimeout(() => notif.remove(), 300);
    }, 4000);
}