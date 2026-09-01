// Document Cross-Examination and Discrepancy Analyzer
// Client-side app: collects documents, calls the Claude API directly from the
// browser with a strict system prompt, and forces structured JSON output via
// tool-use so results can be rendered mechanically (timeline + discrepancies).

const ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/messages';
const ANTHROPIC_MODEL = 'claude-sonnet-5';
const API_KEY_STORAGE_KEY = 'discrepancy-analyzer.anthropic-api-key';

const SYSTEM_PROMPT = `You are a meticulous "Document Cross-Examination and Discrepancy Analyzer."
Your sole purpose is to compare multiple legal, administrative, or factual documents and mechanically detect inconsistencies, numerical discrepancies, timeline shifts, and semantic contradictions.

[STRICT GUIDELINES]
1. Zero Legal Advice: Never provide legal conclusions (e.g., do not say "This is perjury" or "This constitutes fraud"). State only objective discrepancies (e.g., "Document A states X, whereas Document B states Y").
2. Evidence Grounding: Every detected discrepancy must cite exact document names, section/page numbers, and verbatim quotes. Do not extrapolate or assume unstated facts.
3. Chronological Anchoring: Map all mentioned dates, times, and events onto an absolute timeline.
4. Output Format: You must output ONLY valid JSON matching the provided schema, with no conversational filler.

You must call the "report_discrepancy_analysis" tool exactly once with your complete findings. Do not include any prose outside the tool call.`;

const RESULT_SCHEMA = {
  type: 'object',
  properties: {
    documents: {
      type: 'array',
      description: 'Every document that was analyzed.',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string', description: 'Exact document name as provided.' },
          summary: { type: 'string', description: 'One neutral sentence describing what the document is, with no interpretation.' }
        },
        required: ['name']
      }
    },
    timeline: {
      type: 'array',
      description: 'Every date/time and associated event mentioned across all documents, mapped onto an absolute timeline.',
      items: {
        type: 'object',
        properties: {
          date: { type: 'string', description: 'The date/time exactly as it can be resolved (ISO 8601 where possible, otherwise as stated).' },
          event: { type: 'string', description: 'Objective description of the event.' },
          source_document: { type: 'string', description: 'Exact name of the document this event was taken from.' },
          location: { type: 'string', description: 'Section/page/paragraph reference within the source document.' },
          quote: { type: 'string', description: 'Verbatim quote supporting this timeline entry.' }
        },
        required: ['date', 'event', 'source_document', 'quote']
      }
    },
    discrepancies: {
      type: 'array',
      description: 'Every detected inconsistency between documents.',
      items: {
        type: 'object',
        properties: {
          type: {
            type: 'string',
            enum: ['numerical', 'date_time', 'factual', 'semantic', 'other'],
            description: 'Category of discrepancy.'
          },
          description: {
            type: 'string',
            description: 'Objective, non-legal statement of the discrepancy, e.g. "Document A states X, whereas Document B states Y."'
          },
          document_a: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              location: { type: 'string', description: 'Section/page number.' },
              quote: { type: 'string', description: 'Verbatim quote.' }
            },
            required: ['name', 'location', 'quote']
          },
          document_b: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              location: { type: 'string', description: 'Section/page number.' },
              quote: { type: 'string', description: 'Verbatim quote.' }
            },
            required: ['name', 'location', 'quote']
          }
        },
        required: ['type', 'description', 'document_a', 'document_b']
      }
    },
    summary: {
      type: 'object',
      properties: {
        documents_analyzed: { type: 'integer' },
        discrepancies_found: { type: 'integer' }
      },
      required: ['documents_analyzed', 'discrepancies_found']
    }
  },
  required: ['documents', 'timeline', 'discrepancies', 'summary']
};

const documentsListEl = document.getElementById('documents-list');
const documentItemTemplate = document.getElementById('document-item-template');
const addDocumentBtn = document.getElementById('add-document-btn');

const apiKeyInput = document.getElementById('api-key');
const saveKeyBtn = document.getElementById('save-key-btn');
const clearKeyBtn = document.getElementById('clear-key-btn');
const keyStatusEl = document.getElementById('key-status');

const analyzeBtn = document.getElementById('analyze-btn');
const analyzeStatusEl = document.getElementById('analyze-status');
const errorBoxEl = document.getElementById('error-box');

const resultsPanel = document.getElementById('results-panel');
const resultsSummaryEl = document.getElementById('results-summary');
const timelineTableBody = document.querySelector('#timeline-table tbody');
const timelineEmptyEl = document.getElementById('timeline-empty');
const discrepanciesListEl = document.getElementById('discrepancies-list');
const discrepanciesEmptyEl = document.getElementById('discrepancies-empty');
const rawJsonEl = document.getElementById('raw-json');

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str == null ? '' : String(str);
  return div.innerHTML;
}

function addDocumentRow(name = '', text = '') {
  const fragment = documentItemTemplate.content.cloneNode(true);
  const item = fragment.querySelector('.document-item');
  const nameInput = item.querySelector('.doc-name');
  const textArea = item.querySelector('.doc-text');
  const fileInput = item.querySelector('.doc-file');
  const removeBtn = item.querySelector('.remove-document-btn');

  nameInput.value = name;
  textArea.value = text;

  fileInput.addEventListener('change', () => {
    const file = fileInput.files && fileInput.files[0];
    if (!file) return;
    if (!nameInput.value.trim()) {
      nameInput.value = file.name;
    }
    const reader = new FileReader();
    reader.onload = () => {
      textArea.value = String(reader.result || '');
    };
    reader.onerror = () => {
      showError(`Could not read file "${file.name}".`);
    };
    reader.readAsText(file);
  });

  removeBtn.addEventListener('click', () => {
    item.remove();
    ensureAtLeastOneDocument();
  });

  documentsListEl.appendChild(item);
}

function ensureAtLeastOneDocument() {
  if (documentsListEl.querySelectorAll('.document-item').length === 0) {
    addDocumentRow();
  }
}

function collectDocuments() {
  const items = Array.from(documentsListEl.querySelectorAll('.document-item'));
  const docs = [];
  for (const item of items) {
    const name = item.querySelector('.doc-name').value.trim();
    const text = item.querySelector('.doc-text').value.trim();
    if (!name && !text) continue;
    docs.push({ name, text });
  }
  return docs;
}

function loadStoredKey() {
  try {
    const stored = localStorage.getItem(API_KEY_STORAGE_KEY);
    if (stored) {
      apiKeyInput.value = stored;
      keyStatusEl.textContent = 'Using a saved API key from this browser.';
    }
  } catch (e) {
    // localStorage unavailable; ignore.
  }
}

saveKeyBtn.addEventListener('click', () => {
  const key = apiKeyInput.value.trim();
  if (!key) {
    keyStatusEl.textContent = 'Enter an API key before saving.';
    return;
  }
  try {
    localStorage.setItem(API_KEY_STORAGE_KEY, key);
    keyStatusEl.textContent = 'API key saved in this browser.';
  } catch (e) {
    keyStatusEl.textContent = 'Could not save key (local storage unavailable). It will still be used for this session.';
  }
});

clearKeyBtn.addEventListener('click', () => {
  apiKeyInput.value = '';
  try {
    localStorage.removeItem(API_KEY_STORAGE_KEY);
  } catch (e) {
    // ignore
  }
  keyStatusEl.textContent = 'API key cleared.';
});

addDocumentBtn.addEventListener('click', () => addDocumentRow());

function showError(message) {
  errorBoxEl.textContent = message;
  errorBoxEl.hidden = false;
}

function clearError() {
  errorBoxEl.hidden = true;
  errorBoxEl.textContent = '';
}

function setAnalyzing(isAnalyzing) {
  analyzeBtn.disabled = isAnalyzing;
  analyzeStatusEl.textContent = isAnalyzing ? 'Analyzing documents…' : '';
}

function buildUserMessage(docs) {
  const parts = docs.map((doc, i) => {
    return `--- DOCUMENT ${i + 1}: ${doc.name || `(Unnamed Document ${i + 1})`} ---\n${doc.text}`;
  });
  return `Compare the following ${docs.length} documents and detect all discrepancies per your instructions.\n\n${parts.join('\n\n')}`;
}

async function callClaude(apiKey, docs) {
  const body = {
    model: ANTHROPIC_MODEL,
    max_tokens: 8000,
    system: SYSTEM_PROMPT,
    messages: [
      { role: 'user', content: buildUserMessage(docs) }
    ],
    tools: [
      {
        name: 'report_discrepancy_analysis',
        description: 'Report the structured results of the document cross-examination and discrepancy analysis.',
        input_schema: RESULT_SCHEMA
      }
    ],
    tool_choice: { type: 'tool', name: 'report_discrepancy_analysis' }
  };

  const response = await fetch(ANTHROPIC_API_URL, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': apiKey,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true'
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    let detail = '';
    try {
      const errJson = await response.json();
      detail = errJson?.error?.message || JSON.stringify(errJson);
    } catch (e) {
      detail = await response.text().catch(() => '');
    }
    throw new Error(`API request failed (${response.status}): ${detail || response.statusText}`);
  }

  const data = await response.json();
  const toolUse = (data.content || []).find((block) => block.type === 'tool_use');
  if (!toolUse) {
    throw new Error('The model did not return structured results. Please try again.');
  }
  return toolUse.input;
}

function renderResults(result) {
  rawJsonEl.textContent = JSON.stringify(result, null, 2);

  const docCount = result.summary?.documents_analyzed ?? (result.documents || []).length;
  const discCount = result.summary?.discrepancies_found ?? (result.discrepancies || []).length;
  resultsSummaryEl.innerHTML =
    `<strong>${escapeHtml(docCount)}</strong> document(s) analyzed &middot; ` +
    `<strong>${escapeHtml(discCount)}</strong> discrepanc${discCount === 1 ? 'y' : 'ies'} found`;

  timelineTableBody.innerHTML = '';
  const timeline = (result.timeline || []).slice().sort((a, b) => {
    const da = Date.parse(a.date);
    const db = Date.parse(b.date);
    if (isNaN(da) && isNaN(db)) return 0;
    if (isNaN(da)) return 1;
    if (isNaN(db)) return -1;
    return da - db;
  });
  timelineEmptyEl.hidden = timeline.length > 0;
  for (const entry of timeline) {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${escapeHtml(entry.date)}</td>
      <td>${escapeHtml(entry.event)}</td>
      <td>${escapeHtml(entry.source_document)}</td>
      <td>${escapeHtml(entry.location ? `${entry.location} — ` : '')}<em>"${escapeHtml(entry.quote)}"</em></td>
    `;
    timelineTableBody.appendChild(tr);
  }

  discrepanciesListEl.innerHTML = '';
  const discrepancies = result.discrepancies || [];
  discrepanciesEmptyEl.hidden = discrepancies.length > 0;
  discrepancies.forEach((d, i) => {
    const card = document.createElement('div');
    card.className = 'discrepancy-card';
    card.innerHTML = `
      <div class="discrepancy-header">
        <span class="discrepancy-index">#${i + 1}</span>
        <span class="discrepancy-type badge badge-${escapeHtml(d.type || 'other')}">${escapeHtml(d.type || 'other')}</span>
      </div>
      <p class="discrepancy-description">${escapeHtml(d.description)}</p>
      <div class="discrepancy-sources">
        <div class="source-block">
          <div class="source-name">${escapeHtml(d.document_a?.name)}</div>
          <div class="source-location">${escapeHtml(d.document_a?.location)}</div>
          <blockquote>${escapeHtml(d.document_a?.quote)}</blockquote>
        </div>
        <div class="source-block">
          <div class="source-name">${escapeHtml(d.document_b?.name)}</div>
          <div class="source-location">${escapeHtml(d.document_b?.location)}</div>
          <blockquote>${escapeHtml(d.document_b?.quote)}</blockquote>
        </div>
      </div>
    `;
    discrepanciesListEl.appendChild(card);
  });

  resultsPanel.hidden = false;
  resultsPanel.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

analyzeBtn.addEventListener('click', async () => {
  clearError();

  const apiKey = apiKeyInput.value.trim();
  if (!apiKey) {
    showError('Enter your Anthropic API key above before analyzing.');
    return;
  }

  const docs = collectDocuments();
  if (docs.length < 2) {
    showError('Add at least two documents with text before analyzing.');
    return;
  }
  const unnamed = docs.find((d) => !d.name);
  if (unnamed) {
    showError('Every document needs a name so citations are unambiguous.');
    return;
  }

  setAnalyzing(true);
  try {
    const result = await callClaude(apiKey, docs);
    renderResults(result);
  } catch (err) {
    showError(err.message || String(err));
  } finally {
    setAnalyzing(false);
  }
});

loadStoredKey();
addDocumentRow();
addDocumentRow();
