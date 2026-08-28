const ideaInput = document.querySelector('#idea');
const planButton = document.querySelector('#plan');
const result = document.querySelector('#result');
const error = document.querySelector('#error');

const escapeHtml = (value) => String(value ?? '').replace(/[&<>'"]/g, (char) => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
}[char]));

function renderPlan(plan) {
  const layers = (plan.blueprint?.layers || []).map((layer) => `
    <div class="layer">
      <strong>${escapeHtml(layer.name)}</strong>
      <div class="muted">${escapeHtml(layer.purpose)}</div>
      <ul>${(layer.components || []).map((item) => `<li>${escapeHtml(item)}</li>`).join('')}</ul>
    </div>`).join('');

  const tasks = (plan.tasks || []).map((task) => `
    <div class="task">
      <strong>${escapeHtml(task.description)}</strong>
      <div class="muted">${escapeHtml(task.required_capability)} · ${escapeHtml(task.recommended?.agent_name)} · $${Number(task.recommended?.estimated_cost || 0).toFixed(4)}</div>
    </div>`).join('');

  const rationale = (plan.recommendation?.rationale || []).map((item) => `<li>${escapeHtml(item)}</li>`).join('');
  const diy = (plan.diy?.steps || []).map((item) => `<li>${escapeHtml(item)}</li>`).join('');

  result.innerHTML = `
    <section class="card">
      <h2>What CAOS understood</h2>
      <div class="summary">${escapeHtml(plan.understanding)}</div>
    </section>
    <section class="card">
      <h2>Blueprint</h2>
      <div class="grid">${layers}</div>
    </section>
    <section class="card">
      <h2>Work to complete</h2>
      <div class="grid">${tasks}</div>
    </section>
    <section class="card">
      <div class="recommendation">
        <div>
          <h2>CAOS recommendation</h2>
          <div class="summary">${escapeHtml(plan.recommendation?.title)}</div>
          <div class="muted">${escapeHtml(plan.recommendation?.resource)}</div>
          <ul>${rationale}</ul>
        </div>
        <div class="price">$${Number(plan.recommendation?.estimated_cost || 0).toFixed(4)}</div>
      </div>
    </section>
    <section class="card">
      <h2>Show me how</h2>
      <ul>${diy}</ul>
    </section>`;
}

async function planIdea() {
  const idea = ideaInput.value.trim();
  error.textContent = '';
  result.innerHTML = '';
  if (!idea) {
    error.textContent = 'Tell CAOS what you want to build first.';
    ideaInput.focus();
    return;
  }

  planButton.disabled = true;
  planButton.textContent = 'Planning...';
  try {
    const response = await fetch('/api/plan', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ idea })
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || 'CAOS could not create a plan.');
    renderPlan(payload);
  } catch (err) {
    error.textContent = err.message;
  } finally {
    planButton.disabled = false;
    planButton.textContent = 'Plan with CAOS';
  }
}

planButton.addEventListener('click', planIdea);
ideaInput.addEventListener('keydown', (event) => {
  if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') planIdea();
});
