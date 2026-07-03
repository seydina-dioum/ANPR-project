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
    event.target.classList.add('active');

    // Si webcam → démarrer la caméra
    if (tab === 'webcam') {
        startWebcam();
    }
}

// =====================
// UPLOAD IMAGE
// =====================
document.getElementById('fileInput').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    selectedFile = file;
    const reader = new FileReader();
    reader.onload = function(e) {
        document.getElementById('preview').src = e.target.result;
        document.getElementById('detect-section').style.display = 'block';
        document.getElementById('results').style.display = 'none';
    };
    reader.readAsDataURL(file);
});

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
            alert("Impossible d'accéder à la webcam : " + err.message);
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
    }, 'image/jpeg');
}

// =====================
// DETECTION
// =====================
async function detectPlate() {
    if (!selectedFile) {
        alert("Veuillez choisir une image d'abord !");
        return;
    }

    // Afficher le chargement
    document.getElementById('loading').style.display = 'block';
    document.getElementById('results').style.display = 'none';

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

        // Afficher les résultats
        afficherResultats(data);

    } catch (error) {
        document.getElementById('loading').style.display = 'none';
        alert("Erreur : " + error.message);
    }
}

// =====================
// AFFICHAGE RESULTATS
// =====================
function afficherResultats(data) {
    const resultsDiv = document.getElementById('results');
    const contentDiv = document.getElementById('results-content');

    resultsDiv.style.display = 'block';

    if (data.nb_plaques === 0) {
        contentDiv.innerHTML = `
            <div class="no-result">
                ❌ Aucune plaque détectée dans cette image.
            </div>
        `;
        return;
    }

    let html = `<p style="color:#777; margin-bottom:15px;">
        ${data.nb_plaques} plaque(s) détectée(s) en ${data.temps_ms} ms
    </p>`;

    data.plaques.forEach((plaque, index) => {
        const classe = plaque.valide ? 'valide' : 'invalide';
        const badge = plaque.valide
            ? '<span class="badge valide">✅ Valide</span>'
            : '<span class="badge invalide">❌ Invalide</span>';

        html += `
            <div class="plaque-card ${classe}">
                <div class="plaque-texte">
                    🚗 ${plaque.texte} ${badge}
                </div>
                <div class="plaque-details">
                    <p>📝 Texte brut OCR : <strong>${plaque.texte_brut}</strong></p>
                    <p>🎯 Confiance détection : <strong>${(plaque.score_detection * 100).toFixed(1)}%</strong></p>
                    <p>🔤 Confiance OCR : <strong>${(plaque.conf_ocr * 100).toFixed(1)}%</strong></p>
                    <p>⚙️ Moteur OCR : <strong>${plaque.moteur_ocr || 'N/A'}</strong></p>
                    <p>📍 Position : <strong>[${plaque.bbox.join(', ')}]</strong></p>
                </div>
            </div>
        `;
    });

    contentDiv.innerHTML = html;
}