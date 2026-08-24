import zipfile
import os

# Conteúdo dos arquivos do projeto
index_html = """<!DOCTYPE html>
<html lang="fr" data-theme="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Réussir sa Naturalisation Française</title>
  <link rel="stylesheet" href="styles.css">
</head>
<body>
  <div class="app-container">
    <aside class="sidebar">
      <div class="brand">
        <span class="flag">🇫🇷</span>
        <h2>Réussir sa Naturalisation</h2>
      </div>
      <nav class="menu">
        <button class="nav-btn active" onclick="switchTab('dashboard')"><span class="icon">📊</span> Dashboard</button>
        <button class="nav-btn" onclick="switchTab('modules')"><span class="icon">📚</span> Modules & Cours</button>
        <button class="nav-btn" onclick="switchTab('quiz-bank')"><span class="icon">📝</span> Banque de Questions</button>
        <button class="nav-btn" onclick="switchTab('flashcards')"><span class="icon">🎴</span> Flashcards</button>
        <button class="nav-btn" onclick="switchTab('interview')"><span class="icon">🎙️</span> Simulateur d'Entretien</button>
        <button class="nav-btn" onclick="switchTab('checklist')"><span class="icon">📄</span> Checklist & Dossier</button>
      </nav>
      <div class="sidebar-footer">
        <div class="user-profile"><span class="avatar">👤</span><span>Apprenant</span></div>
        <button class="theme-toggle" onclick="toggleTheme()" title="Changer le thème">🌓</button>
      </div>
    </aside>

    <main class="main-content">
      <header class="top-bar">
        <div class="search-box">
          <input type="text" id="global-search" placeholder="Rechercher (ex: Napoléon, Laïcité...)">
        </div>
        <div class="quick-actions">
          <button class="btn btn-warning" onclick="startEveMode()">⭐ Mode Veille d'Entretien</button>
        </div>
      </header>

      <section id="view-dashboard" class="tab-view active">
        <div class="welcome-card">
          <h1>Préparez votre entretien en 15 min par jour</h1>
          <p>Progression globale du programme</p>
          <div class="progress-bar-container"><div class="progress-bar" id="global-progress-bar" style="width: 0%"></div></div>
          <span id="global-progress-text">0% complété</span>
        </div>
        <div class="dashboard-grid">
          <div class="card">
            <h3>🎯 Objectif du jour</h3>
            <p>Complétez votre session quotidienne de 15 minutes.</p>
            <button class="btn btn-primary btn-block" onclick="switchTab('modules')">Commencer la session</button>
          </div>
        </div>
      </section>

      <section id="view-modules" class="tab-view">
        <h2>Modules de formation</h2>
        <div id="modules-list" class="modules-container"></div>
      </section>

      <section id="view-lesson" class="tab-view">
        <button class="btn btn-secondary" onclick="switchTab('modules')">← Retour aux modules</button>
        <div id="lesson-content-container" style="margin-top:1rem;"></div>
      </section>

      <section id="view-flashcards" class="tab-view">
        <h2>Révision par Flashcards (SRS)</h2>
        <div class="flashcard-wrapper">
          <div id="flashcard" class="flashcard" onclick="flipCard()">
            <div class="flashcard-front" id="card-front">Cliquez pour commencer</div>
            <div class="flashcard-back" id="card-back">Réponse ici</div>
          </div>
          <div class="flashcard-controls" style="margin-top:1rem; display:flex; gap:1rem;">
            <button class="btn btn-danger" onclick="answerCard(false)">À revoir ❌</button>
            <button class="btn btn-success" onclick="answerCard(true)">Mémorisé ✅</button>
          </div>
        </div>
      </section>

      <section id="view-interview" class="tab-view">
        <h2>Simulateur d'Entretien</h2>
        <div class="card interview-card">
          <div class="speech-bubble" id="interview-question">Bonjour. Pourquoi souhaitez-vous devenir Français ?</div>
          <button class="btn btn-secondary" onclick="speakCurrentQuestion()">🔊 Écouter la question</button>
          <div style="margin-top: 1rem;">
            <textarea id="user-interview-answer" placeholder="Formulez votre réponse ici..."></textarea>
            <button class="btn btn-primary" onclick="revealInterviewAnswer()">Afficher la réponse idéale</button>
          </div>
          <div id="ideal-answer-box" class="card hidden" style="margin-top: 1rem;">
            <h4>Exemple de réponse idéale :</h4>
            <p id="ideal-answer-text"></p>
          </div>
        </div>
      </section>

      <section id="view-checklist" class="tab-view">
        <h2>Checklist du Dossier de Naturalisation</h2>
        <div class="card">
          <ul style="list-style:none; display:flex; flex-direction:column; gap:0.75rem;">
            <li><label><input type="checkbox"> Formulaire Cerfa n°12753*02 rempli et signé</label></li>
            <li><label><input type="checkbox"> Timbre fiscal électronique (55 €)</label></li>
            <li><label><input type="checkbox"> Copie intégrale de l'acte de naissance</label></li>
            <li><label><input type="checkbox"> Justificatif de domicile récent (-3 mois)</label></li>
            <li><label><input type="checkbox"> Attestation de niveau linguistique B1 / B2</label></li>
          </ul>
        </div>
      </section>
    </main>
  </div>
  <script src="data.js"></script>
  <script src="app.js"></script>
</body>
</html>"""

styles_css = """:root {
  --bg-primary: #121826;
  --bg-secondary: #1a2332;
  --bg-card: #222e42;
  --text-main: #f3f4f6;
  --text-muted: #9ca3af;
  --accent-blue: #2563eb;
  --success: #10b981;
  --warning: #f59e0b;
  --danger: #ef4444;
  --border-color: #374151;
  --font-family: system-ui, -apple-system, sans-serif;
}
[data-theme="light"] {
  --bg-primary: #f8fafc;
  --bg-secondary: #ffffff;
  --bg-card: #f1f5f9;
  --text-main: #0f172a;
  --text-muted: #64748b;
  --border-color: #e2e8f0;
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: var(--font-family); background-color: var(--bg-primary); color: var(--text-main); height: 100vh; overflow: hidden; }
.app-container { display: flex; height: 100vh; }
.sidebar { width: 280px; background-color: var(--bg-secondary); border-right: 1px solid var(--border-color); display: flex; flex-direction: column; padding: 1.5rem 1rem; }
.brand { display: flex; align-items: center; gap: 0.75rem; margin-bottom: 2rem; }
.menu { display: flex; flex-direction: column; gap: 0.5rem; flex: 1; }
.nav-btn { display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem 1rem; border: none; background: transparent; color: var(--text-muted); border-radius: 8px; cursor: pointer; text-align: left; transition: all 0.2s; }
.nav-btn:hover, .nav-btn.active { background-color: var(--accent-blue); color: #fff; }
.sidebar-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 1rem; border-top: 1px solid var(--border-color); }
.main-content { flex: 1; display: flex; flex-direction: column; overflow-y: auto; padding: 1.5rem 2rem; }
.top-bar { display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem; }
.search-box input { padding: 0.6rem 1rem; border-radius: 8px; border: 1px solid var(--border-color); background-color: var(--bg-secondary); color: var(--text-main); width: 300px; }
.tab-view { display: none; }
.tab-view.active { display: block; }
.card { background-color: var(--bg-secondary); border: 1px solid var(--border-color); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }
.welcome-card { background: linear-gradient(135deg, #1e3a8a, #2563eb); color: white; padding: 2rem; border-radius: 12px; margin-bottom: 2rem; }
.progress-bar-container { background: rgba(255,255,255,0.2); height: 12px; border-radius: 6px; margin: 1rem 0 0.5rem 0; overflow: hidden; }
.progress-bar { background-color: var(--success); height: 100%; transition: width 0.3s; }
.btn { padding: 0.6rem 1.2rem; border-radius: 8px; border: none; cursor: pointer; font-weight: 600; }
.btn-primary { background-color: var(--accent-blue); color: white; }
.btn-secondary { background-color: var(--bg-card); color: var(--text-main); }
.btn-success { background-color: var(--success); color: white; }
.btn-warning { background-color: var(--warning); color: #000; }
.btn-danger { background-color: var(--danger); color: white; }
.btn-block { width: 100%; margin-top: 1rem; }
.flashcard-wrapper { display: flex; flex-direction: column; align-items: center; margin-top: 2rem; }
.flashcard { width: 400px; height: 240px; background-color: var(--bg-secondary); border: 2px solid var(--accent-blue); border-radius: 16px; display: flex; justify-content: center; align-items: center; text-align: center; padding: 1.5rem; font-size: 1.2rem; cursor: pointer; }
.flashcard-back { display: none; color: var(--success); }
.flashcard.flipped .flashcard-front { display: none; }
.flashcard.flipped .flashcard-back { display: block; }
.speech-bubble { background-color: var(--bg-card); padding: 1.5rem; border-radius: 12px; font-size: 1.2rem; margin: 1.5rem 0; }
textarea { width: 100%; height: 100px; background-color: var(--bg-primary); color: var(--text-main); border: 1px solid var(--border-color); border-radius: 8px; padding: 1rem; margin-bottom: 1rem; }
.hidden { display: none !important; }"""

data_js = """const courseData = [
  {
    id: "mod-1",
    title: "Módulo 1: Les Valeurs de la République",
    lessons: [
      {
        id: "m1-l1",
        title: "Aula 1: O que significa tornar-se francês",
        duration: "15 min",
        reading: "Devenir Français est un acte engagé qui signifie adhérer pleinement aux principes, droits et devoirs de la République.",
        summary: "L'intégration exige la maîtrise du français et le respect des lois républicaines.",
        warning: "C'est la question systématique de l'entretien préfectoral.",
        interviewQuestions: [{ q: "Pourquoi souhaitez-vous devenir Français ?", a: "Pour concrétiser mon intégration, partager les valeurs républicaines et m'investir pleinement dans la société." }],
        quiz: [{ q: "Quel document officialise la naturalisation ?", options: ["Le décret de naturalisation", "Le passeport", "Le visa"], correct: 0, exp: "La publication au Journal Officiel scelle la nationalité." }],
        flashcards: [{ front: "Devise républicaine", back: "Liberté, Égalité, Fraternité" }]
      },
      {
        id: "m1-l2",
        title: "Aula 2: Liberté",
        duration: "15 min",
        reading: "La liberté consiste à pouvoir faire tout ce qui ne nuit pas à autrui (Article 4 de la Déclaration de 1789).",
        summary: "Inclus la liberté d'expression, de conscience, de réunion et de circulation.",
        warning: "La liberté d'expression a pour limite le respect d'autrui et l'absence de propos haineux.",
        interviewQuestions: [{ q: "Quelles sont les libertés fondamentales en France ?", a: "Liberté d'expression, de conscience, de religion, de réunion et de presse." }],
        quiz: [{ q: "Où est définie la liberté pour la première fois ?", options: ["Déclaration de 1789", "Constitution de 1958", "Code Civil"], correct: 0, exp: "Elle apparaît dès la Déclaration des Droits de l'Homme et du Citoyen." }],
        flashcards: [{ front: "Limite de la liberté ?", back: "Elle s'arrête là où commence celle des autres." }]
      }
    ]
  },
  {
    id: "mod-2",
    title: "Módulo 2: Histoire et Symboles de la France",
    lessons: [
      {
        id: "m2-l1",
        title: "Aula 1: La Révolution Française de 1789",
        duration: "15 min",
        reading: "La Révolution marque la fin de la monarchie absolue et le début de la République.",
        summary: "Prise de la Bastille le 14 juillet 1789 et Déclaration des Droits de l'Homme.",
        warning: "Connaître impérativement la date exacte de la prise de la Bastille.",
        interviewQuestions: [{ q: "Quand a eu lieu la Révolution française ?", a: "En 1789 (Prise de la Bastille le 14 juillet 1789)." }],
        quiz: [{ q: "Que fête-t-on le 14 juillet ?", options: ["La Fête Nationale", "La fin de la guerre", "L'armistice"], correct: 0, exp: "Célébration de la Fête de la Fédération et de la prise de la Bastille." }],
        flashcards: [{ front: "Année de la Révolution", back: "1789" }]
      }
    ]
  }
];"""

app_js = """let state = {
  currentTab: 'dashboard',
  theme: 'dark',
  progress: JSON.parse(localStorage.getItem('nat_progress')) || { completedLessons: [] }
};

document.addEventListener("DOMContentLoaded", () => {
  renderModules();
  updateDashboard();
  loadFlashcard();
});

function switchTab(tabId) {
  document.querySelectorAll('.tab-view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  const target = document.getElementById(`view-${tabId}`);
  if (target) target.classList.add('active');
}

function renderModules() {
  const container = document.getElementById('modules-list');
  if (!container) return;
  container.innerHTML = courseData.map(mod => `
    <div class="card">
      <h3>${mod.title}</h3>
      ${mod.lessons.map(l => `
        <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.5rem; padding:0.5rem 0; border-bottom:1px solid var(--border-color);">
          <span>${l.title} (${l.duration})</span>
          <button class="btn btn-primary" onclick="openLesson('${l.id}')">Ouvrir</button>
        </div>
      `).join('')}
    </div>
  `).join('');
}

function openLesson(lessonId) {
  let lesson = null;
  courseData.forEach(m => {
    const found = m.lessons.find(l => l.id === lessonId);
    if (found) lesson = found;
  });

  if (!lesson) return;

  const container = document.getElementById('lesson-content-container');
  container.innerHTML = `
    <div class="card">
      <h2>${lesson.title}</h2>
      <p><strong>Temps :</strong> ${lesson.duration}</p>
      <hr style="margin:1rem 0; border-color:var(--border-color);">
      <h3>Lecture principale</h3>
      <p style="margin-top:0.5rem;">${lesson.reading}</p>
      <br>
      <h3>Résumé</h3>
      <p style="margin-top:0.5rem;">${lesson.summary}</p>
      <br>
      <div style="background:rgba(245, 158, 11, 0.1); padding:1rem; border-left:4px solid var(--warning); margin:1rem 0;">
        <strong>⚠️ Point Entretien :</strong> ${lesson.warning}
      </div>
      <button class="btn btn-success" onclick="markLessonComplete('${lesson.id}')">Marquer comme terminée ✅</button>
    </div>
  `;
  switchTab('lesson');
}

function markLessonComplete(id) {
  if (!state.progress.completedLessons.includes(id)) {
    state.progress.completedLessons.push(id);
    localStorage.setItem('nat_progress', JSON.stringify(state.progress));
    updateDashboard();
  }
  switchTab('modules');
}

function updateDashboard() {
  let total = 0;
  courseData.forEach(m => total += m.lessons.length);
  const percentage = Math.round((state.progress.completedLessons.length / total) * 100) || 0;
  
  const bar = document.getElementById('global-progress-bar');
  const txt = document.getElementById('global-progress-text');
  if (bar) bar.style.width = percentage + '%';
  if (txt) txt.innerText = percentage + '% complété';
}

function toggleTheme() {
  state.theme = state.theme === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', state.theme);
}

function flipCard() { document.getElementById('flashcard').classList.toggle('flipped'); }

function loadFlashcard() {
  const card = courseData[0].lessons[0].flashcards[0];
  document.getElementById('card-front').innerText = card.front;
  document.getElementById('card-back').innerText = card.back;
}

function answerCard(success) {
  document.getElementById('flashcard').classList.remove('flipped');
  loadFlashcard();
}

function speakCurrentQuestion() {
  const text = document.getElementById('interview-question').innerText;
  if ('speechSynthesis' in window) {
    const u = new SpeechSynthesisUtterance(text);
    u.lang = 'fr-FR';
    window.speechSynthesis.speak(u);
  }
}

function revealInterviewAnswer() {
  document.getElementById('ideal-answer-text').innerText = courseData[0].lessons[0].interviewQuestions[0].a;
  document.getElementById('ideal-answer-box').classList.remove('hidden');
}

function startEveMode() { switchTab('interview'); }"""

# Criação do arquivo ZIP
zip_name = "reussir-sa-naturalisation.zip"
with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
    zipf.writestr("index.html", index_html)
    zipf.writestr("styles.css", styles_css)
    zipf.writestr("data.js", data_js)
    zipf.writestr("app.js", app_js)

print(f"✅ Arquivo ZIP gerado com sucesso: {os.path.abspath(zip_name)}")