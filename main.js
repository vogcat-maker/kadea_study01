// Document Cross-Examination and Discrepancy Analyzer
// Client-side app: collects documents, calls the Claude API directly from the
// browser with a strict system prompt, and forces structured JSON output via
// tool-use so results can be rendered mechanically (timeline + discrepancies).

const ANTHROPIC_API_URL = 'https://api.anthropic.com/v1/messages';
const ANTHROPIC_MODEL = 'claude-sonnet-5';
const API_KEY_STORAGE_KEY = 'discrepancy-analyzer.anthropic-api-key';

const SYSTEM_PROMPT = `당신은 다중 문서 간의 사실관계 교차 검증 및 모순 탐지를 전문으로 수행하는 '문서 교차 분석 AI 엔진'입니다.
제공된 여러 건의 진술서, 준비서면, 증거 자료 등을 정밀 대조하여 서술의 불일치, 수치 왜곡, 시계열 모순, 진술 번복(의미 축소/변형)을 기계적이고 객관적으로 적발합니다.

[절대 준수 원칙]
1. 법적 판단 금지: "이는 사기죄에 해당함", "명백한 위증임"과 같은 법적 단정을 절대 내리지 마십시오. 철저히 사실관계의 불일치(예: "문서 A에서는 X라고 명시했으나, 문서 B에서는 Y라고 번복함")만을 서술하십시오.
2. 엄격한 근거 기반(Grounding): 모든 모순 지적은 반드시 해당 문서명, 원문 인용(verbatim quote), 페이지/단락 정보를 포함해야 합니다. 문서에 없는 내용을 추측하거나 지어내지 마십시오.
3. 시계열 재구성: 문서에 등장하는 모든 사건 발생일, 작성일, 진술일을 절대적 시간 순서로 정렬하여 모순을 파악하십시오.
4. 출력 형식: 대화형 설명이나 인사말 없이 지정된 JSON 포맷으로만 응답하십시오.

반드시 "report_discrepancy_analysis" 도구를 정확히 한 번 호출하여 분석 결과 전체를 전달하십시오. 도구 호출 외의 어떠한 설명 텍스트도 포함하지 마십시오.`;

const RESULT_SCHEMA = {
  type: 'object',
  properties: {
    documents: {
      type: 'array',
      description: '분석 대상이 된 모든 문서.',
      items: {
        type: 'object',
        properties: {
          name: { type: 'string', description: '제공된 그대로의 정확한 문서명.' },
          summary: { type: 'string', description: '해석을 배제한, 문서 성격에 대한 한 문장의 중립적 설명.' }
        },
        required: ['name']
      }
    },
    timeline: {
      type: 'array',
      description: '모든 문서에 등장하는 일자/시각과 관련 사건을 절대적 시간 순서로 정렬한 항목.',
      items: {
        type: 'object',
        properties: {
          date: { type: 'string', description: '가능한 경우 ISO 8601 형식, 그렇지 않으면 문서에 기재된 그대로의 일자/시각.' },
          event: { type: 'string', description: '사건에 대한 객관적 서술.' },
          source_document: { type: 'string', description: '해당 사건의 출처가 된 정확한 문서명.' },
          location: { type: 'string', description: '출처 문서 내 조항/페이지/단락 정보.' },
          quote: { type: 'string', description: '이 시계열 항목을 뒷받침하는 원문 그대로의 인용.' }
        },
        required: ['date', 'event', 'source_document', 'quote']
      }
    },
    discrepancies: {
      type: 'array',
      description: '문서 간 적발된 모든 불일치 사항.',
      items: {
        type: 'object',
        properties: {
          type: {
            type: 'string',
            enum: ['numerical', 'date_time', 'factual', 'semantic', 'other'],
            description: '불일치 유형: numerical(수치 왜곡), date_time(시계열 모순), factual(서술의 불일치), semantic(진술 번복/의미 축소·변형), other(기타).'
          },
          description: {
            type: 'string',
            description: '법적 판단을 배제한 객관적 불일치 서술. 예: "문서 A에서는 X라고 명시했으나, 문서 B에서는 Y라고 번복함."'
          },
          document_a: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              location: { type: 'string', description: '조항/페이지 번호.' },
              quote: { type: 'string', description: '원문 그대로의 인용.' }
            },
            required: ['name', 'location', 'quote']
          },
          document_b: {
            type: 'object',
            properties: {
              name: { type: 'string' },
              location: { type: 'string', description: '조항/페이지 번호.' },
              quote: { type: 'string', description: '원문 그대로의 인용.' }
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

const DISCREPANCY_TYPE_LABELS = {
  numerical: '수치 왜곡',
  date_time: '시계열 모순',
  factual: '서술의 불일치',
  semantic: '진술 번복',
  other: '기타'
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
      showError(`"${file.name}" 파일을 읽을 수 없습니다.`);
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
      keyStatusEl.textContent = '이 브라우저에 저장된 API 키를 사용합니다.';
    }
  } catch (e) {
    // localStorage unavailable; ignore.
  }
}

saveKeyBtn.addEventListener('click', () => {
  const key = apiKeyInput.value.trim();
  if (!key) {
    keyStatusEl.textContent = '저장하기 전에 API 키를 입력하세요.';
    return;
  }
  try {
    localStorage.setItem(API_KEY_STORAGE_KEY, key);
    keyStatusEl.textContent = '이 브라우저에 API 키가 저장되었습니다.';
  } catch (e) {
    keyStatusEl.textContent = '키를 저장할 수 없습니다(로컬 저장소 사용 불가). 이번 세션 동안은 계속 사용됩니다.';
  }
});

clearKeyBtn.addEventListener('click', () => {
  apiKeyInput.value = '';
  try {
    localStorage.removeItem(API_KEY_STORAGE_KEY);
  } catch (e) {
    // ignore
  }
  keyStatusEl.textContent = 'API 키가 삭제되었습니다.';
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
  analyzeStatusEl.textContent = isAnalyzing ? '문서를 분석하는 중…' : '';
}

function buildUserMessage(docs) {
  const parts = docs.map((doc, i) => {
    return `--- 문서 ${i + 1}: ${doc.name || `(문서 ${i + 1}, 이름 없음)`} ---\n${doc.text}`;
  });
  return `다음 ${docs.length}개 문서를 대조하여 지침에 따라 모든 불일치 사항을 적발하십시오.\n\n${parts.join('\n\n')}`;
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
    throw new Error('모델이 구조화된 결과를 반환하지 않았습니다. 다시 시도해 주세요.');
  }
  return toolUse.input;
}

function renderResults(result) {
  rawJsonEl.textContent = JSON.stringify(result, null, 2);

  const docCount = result.summary?.documents_analyzed ?? (result.documents || []).length;
  const discCount = result.summary?.discrepancies_found ?? (result.discrepancies || []).length;
  resultsSummaryEl.innerHTML =
    `분석 문서 <strong>${escapeHtml(docCount)}</strong>건 &middot; ` +
    `적발된 불일치 <strong>${escapeHtml(discCount)}</strong>건`;

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
        <span class="discrepancy-type badge badge-${escapeHtml(d.type || 'other')}">${escapeHtml(DISCREPANCY_TYPE_LABELS[d.type] || DISCREPANCY_TYPE_LABELS.other)}</span>
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
    showError('분석 전에 위에 Anthropic API 키를 입력하세요.');
    return;
  }

  const docs = collectDocuments();
  if (docs.length < 2) {
    showError('분석 전에 텍스트가 포함된 문서를 2건 이상 추가하세요.');
    return;
  }
  const unnamed = docs.find((d) => !d.name);
  if (unnamed) {
    showError('인용 출처를 명확히 하기 위해 모든 문서에 이름이 필요합니다.');
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
