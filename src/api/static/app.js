(function(){
  'use strict';

  const API_BASE = '';
  const QUERY_URL = API_BASE + '/query';
  const HEALTH_URL = API_BASE + '/health';

  const SESSION_KEY = 'artefact_session_id';
  let sessionId = localStorage.getItem(SESSION_KEY);
  if (!sessionId) {
    sessionId = crypto.randomUUID();
    localStorage.setItem(SESSION_KEY, sessionId);
  }

  const dom = {
    form: document.getElementById('inputForm'),
    input: document.getElementById('userInput'),
    sendBtn: document.getElementById('sendBtn'),
    messages: document.getElementById('messages'),
    emptyState: document.getElementById('emptyState'),
    loadingIndicator: document.getElementById('loadingIndicator'),
    suggestions: document.getElementById('suggestions'),
    statusDot: document.getElementById('statusDot'),
    statusLabel: document.getElementById('statusLabel'),
    errorToast: document.getElementById('errorToast'),
    errorMessage: document.getElementById('errorMessage'),
    toastClose: document.querySelector('.toast-close'),
  };

  let isLoading = false;

  function showError(msg) {
    dom.errorMessage.textContent = msg;
    dom.errorToast.classList.remove('hidden');
    setTimeout(() => dom.errorToast.classList.add('hidden'), 6000);
  }

  dom.toastClose.addEventListener('click', () => {
    dom.errorToast.classList.add('hidden');
  });

  function setLoading(state) {
    isLoading = state;
    dom.sendBtn.disabled = state || !dom.input.value.trim();
    dom.input.disabled = state;
    dom.loadingIndicator.classList.toggle('hidden', !state);
  }

  function scrollToBottom() {
    const chat = document.getElementById('chat');
    requestAnimationFrame(() => {
      chat.scrollTop = chat.scrollHeight;
    });
  }

  function autoResize(el) {
    el.style.height = 'auto';
    el.style.height = Math.min(el.scrollHeight, 200) + 'px';
  }

  function getMessageHtml(role, content, toolCalls) {
    const isUser = role === 'user';
    const label = isUser ? 'Você' : 'Artefact';
    let toolHtml = '';

    if (toolCalls && toolCalls.length > 0) {
      toolHtml = '<div class="tool-calls">';
      for (const tc of toolCalls) {
        const duration = tc.duration_ms != null ? tc.duration_ms + 'ms' : '';
        toolHtml += '<details class="tool-call">';
        toolHtml += '<summary>';
        toolHtml += '<span class="tool-call-icon">&#x2699;</span>';
        toolHtml += '<span class="tool-call-name">' + esc(tc.tool_name) + '</span>';
        if (duration) toolHtml += '<span class="tool-call-duration">' + duration + '</span>';
        toolHtml += '</summary>';
        toolHtml += '<div class="tool-call-detail">';
        if (tc.input) toolHtml += '<strong>Input:</strong> ' + esc(tc.input) + '\n';
        if (tc.output) toolHtml += '<strong>Output:</strong> ' + esc(tc.output);
        toolHtml += '</div>';
        toolHtml += '</details>';
      }
      toolHtml += '</div>';
    }

    return '<div class="message ' + role + '">'
      + '<div class="message-label">' + label + '</div>'
      + '<div class="message-content">' + content + '</div>'
      + toolHtml
      + '</div>';
  }

  function esc(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
  }

  function renderContent(text) {
    let html = esc(text);
    html = html.replace(/\n/g, '<br>');
    return html;
  }

  function addMessage(role, text, toolCalls) {
    dom.emptyState.style.display = 'none';
    const html = getMessageHtml(role, renderContent(text), toolCalls || null);
    dom.messages.insertAdjacentHTML('beforeend', html);
    scrollToBottom();
  }

  async function checkHealth() {
    dom.statusDot.className = 'status-dot checking';
    dom.statusLabel.textContent = 'verificando...';
    try {
      const res = await fetch(HEALTH_URL);
      const data = await res.json();
      if (data.status === 'ok') {
        dom.statusDot.className = 'status-dot online';
        dom.statusLabel.textContent = data.mode === 'full' ? 'online' : 'modo calculadora';
      } else {
        dom.statusDot.className = 'status-dot degraded';
        dom.statusLabel.textContent = 'modo limitado';
      }
    } catch {
      dom.statusDot.className = 'status-dot offline';
      dom.statusLabel.textContent = 'offline';
    }
  }

  async function sendQuery(text) {
    if (isLoading || !text.trim()) return;
    setLoading(true);

    addMessage('user', text);

    try {
      const res = await fetch(QUERY_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query: text, session_id: sessionId, verbose: true }),
      });

      if (!res.ok) {
        let detail = 'Erro do servidor (' + res.status + ')';
        try {
          const err = await res.json();
          if (err.detail) detail = err.detail;
        } catch {}
        if (res.status === 413) detail = 'Mensagem muito longa (máx. 10.000 caracteres)';
        if (res.status === 504) detail = 'O agente demorou muito para responder. Tente novamente.';
        showError(detail);
        addMessage('agent', 'Desculpe, ocorreu um erro: ' + detail);
        setLoading(false);
        return;
      }

      const data = await res.json();
      addMessage('agent', data.response, data.tool_calls || null);
    } catch (err) {
      const msg = 'Erro de conexão. Verifique se o servidor está rodando.';
      showError(msg);
      addMessage('agent', msg);
    }

    setLoading(false);
  }

  dom.form.addEventListener('submit', function(e) {
    e.preventDefault();
    const text = dom.input.value.trim();
    if (!text || isLoading) return;
    dom.input.value = '';
    dom.input.style.height = 'auto';
    sendQuery(text);
  });

  dom.input.addEventListener('input', function() {
    autoResize(this);
    dom.sendBtn.disabled = isLoading || !this.value.trim();
  });

  dom.input.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      dom.form.dispatchEvent(new Event('submit'));
    }
  });

  dom.suggestions.addEventListener('click', function(e) {
    const btn = e.target.closest('.suggestion-btn');
    if (!btn) return;
    dom.input.value = btn.dataset.query;
    dom.input.dispatchEvent(new Event('input'));
    dom.form.dispatchEvent(new Event('submit'));
  });

  checkHealth();
  setInterval(checkHealth, 30000);

})();
