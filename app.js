let state = {
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

function startEveMode() { switchTab('interview'); }