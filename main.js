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

const DISCREPANCY_TYPES = ['수치_불일치', '시계열_모순', '사실관계_충돌', '진술_번복_뉘앙스변화'];

const RESULT_SCHEMA = {
  type: 'object',
  properties: {
    시계열_분석: {
      type: 'array',
      description: '모든 문서에 언급된 일시/날짜와 해당 사건을 시간 순서대로 재배열한 목록.',
      items: {
        type: 'object',
        properties: {
          일시: { type: 'string', description: 'YYYY-MM-DD 또는 문서에 명시된 시점 그대로.' },
          사건_내용: { type: 'string', description: '문서에 언급된 구체적 행위나 사건.' },
          출처: {
            type: 'array',
            items: { type: 'string' },
            description: '문서명 및 인용 위치 (예: "진술서(2024.3.2), 2문단").'
          }
        },
        required: ['일시', '사건_내용', '출처']
      }
    },
    탐지된_모순_목록: {
      type: 'array',
      description: '탐지된 모든 모순/불일치 사항.',
      items: {
        type: 'object',
        properties: {
          모순_유형: {
            type: 'string',
            enum: DISCREPANCY_TYPES,
            description: '수치_불일치 | 시계열_모순 | 사실관계_충돌 | 진술_번복_뉘앙스변화'
          },
          항목_제목: { type: 'string', description: '모순점 요약 제목.' },
          상세_대조: {
            type: 'object',
            properties: {
              문서A: {
                type: 'object',
                properties: {
                  문서명: { type: 'string' },
                  원문_인용: { type: 'string', description: '정확한 원문 문장.' },
                  주장_내용: { type: 'string', description: '해당 문서에서 주장하는 요점.' }
                },
                required: ['문서명', '원문_인용', '주장_내용']
              },
              문서B: {
                type: 'object',
                properties: {
                  문서명: { type: 'string' },
                  원문_인용: { type: 'string', description: '정확한 원문 문장.' },
                  주장_내용: { type: 'string', description: '해당 문서에서 주장하는 요점.' }
                },
                required: ['문서명', '원문_인용', '주장_내용']
              }
            },
            required: ['문서A', '문서B']
          },
          불일치_요약: { type: 'string', description: '두 진술/수치가 어떻게 충돌하는지에 대한 객관적 설명. 법적 판단 배제.' },
          중요도_점수: { type: 'integer', minimum: 1, maximum: 5, description: '1(경미)부터 5(중대)까지의 정수.' }
        },
        required: ['모순_유형', '항목_제목', '상세_대조', '불일치_요약', '중요도_점수']
      }
    }
  },
  required: ['시계열_분석', '탐지된_모순_목록']
};

const DISCREPANCY_TYPE_LABELS = {
  '수치_불일치': '수치 불일치',
  '시계열_모순': '시계열 모순',
  '사실관계_충돌': '사실관계 충돌',
  '진술_번복_뉘앙스변화': '진술 번복·뉘앙스 변화'
};

const DISCREPANCY_TYPE_STYLE = {
  '수치_불일치': 'numerical',
  '시계열_모순': 'date_time',
  '사실관계_충돌': 'factual',
  '진술_번복_뉘앙스변화': 'semantic'
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

function addDocumentRow(name = '', text = '', date = '') {
  const fragment = documentItemTemplate.content.cloneNode(true);
  const item = fragment.querySelector('.document-item');
  const nameInput = item.querySelector('.doc-name');
  const dateInput = item.querySelector('.doc-date');
  const textArea = item.querySelector('.doc-text');
  const fileInput = item.querySelector('.doc-file');
  const removeBtn = item.querySelector('.remove-document-btn');

  nameInput.value = name;
  dateInput.value = date;
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
    const date = item.querySelector('.doc-date').value.trim();
    const text = item.querySelector('.doc-text').value.trim();
    if (!name && !text) continue;
    docs.push({ name, date, text });
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
  const docBlocks = docs.map((doc, i) => {
    const name = doc.name || `(문서 ${i + 1}, 이름 없음)`;
    const date = doc.date || '미상';
    return `---\n문서 ${i + 1} (문서명: ${name}, 작성일자: ${date}):\n${doc.text}`;
  });

  return `제공된 문서들을 상호 대조하여 진술의 모순, 수치 왜곡, 시간 순서의 불일치, 미세한 표현 변화(책임 회피성 의미 축소 등)를 찾아내 분석하십시오.

[분석 대상 문서 목록]
${docBlocks.join('\n')}
---

[분석 단계]
1. 시계열 통합: 모든 문서에 언급된 일시/날짜와 해당 사건을 시간 순서대로 재배열하십시오.
2. 핵심 팩트 및 수치 앵커링: 금액, 수량, 횟수, 위치, 핵심 행위 등 변동되면 안 되는 데이터를 추적하십시오.
3. 불일치/모순 탐지:
   - 직접적 사실 충돌 (A문서와 B문서의 주장이 정면 배치되는 경우)
   - 수치/일시 변형 (단순 오타인지 의도적 변경인지 맥락 포함)
   - 표현 및 뉘앙스 변화 (예: "본 적 없다" -> "기억나지 않는다" -> "그 자리에 없었다" 등 진술 연성화)

지정된 "report_discrepancy_analysis" 도구를 통해 시계열_분석과 탐지된_모순_목록을 정확히 준수하여 출력하십시오.`;
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
        description: '문서 교차 분석 결과(시계열_분석, 탐지된_모순_목록)를 구조화된 형태로 보고합니다.',
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

function importanceDots(score) {
  const n = Math.max(1, Math.min(5, Number(score) || 0));
  return '●'.repeat(n) + '○'.repeat(5 - n);
}

function renderResults(result, docCount) {
  rawJsonEl.textContent = JSON.stringify(result, null, 2);

  const discCount = (result.탐지된_모순_목록 || []).length;
  resultsSummaryEl.innerHTML =
    `분석 문서 <strong>${escapeHtml(docCount)}</strong>건 &middot; ` +
    `적발된 불일치 <strong>${escapeHtml(discCount)}</strong>건`;

  timelineTableBody.innerHTML = '';
  const timeline = (result.시계열_분석 || []).slice().sort((a, b) => {
    const da = Date.parse(a.일시);
    const db = Date.parse(b.일시);
    if (isNaN(da) && isNaN(db)) return 0;
    if (isNaN(da)) return 1;
    if (isNaN(db)) return -1;
    return da - db;
  });
  timelineEmptyEl.hidden = timeline.length > 0;
  for (const entry of timeline) {
    const sources = Array.isArray(entry.출처) ? entry.출처 : [entry.출처].filter(Boolean);
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>${escapeHtml(entry.일시)}</td>
      <td>${escapeHtml(entry.사건_내용)}</td>
      <td>${sources.map((s) => `<div>${escapeHtml(s)}</div>`).join('')}</td>
    `;
    timelineTableBody.appendChild(tr);
  }

  discrepanciesListEl.innerHTML = '';
  const discrepancies = result.탐지된_모순_목록 || [];
  discrepanciesEmptyEl.hidden = discrepancies.length > 0;
  discrepancies.forEach((d, i) => {
    const docA = d.상세_대조?.문서A;
    const docB = d.상세_대조?.문서B;
    const card = document.createElement('div');
    card.className = 'discrepancy-card';
    card.innerHTML = `
      <div class="discrepancy-header">
        <span class="discrepancy-index">#${i + 1}</span>
        <span class="discrepancy-type badge badge-${escapeHtml(DISCREPANCY_TYPE_STYLE[d.모순_유형] || 'other')}">${escapeHtml(DISCREPANCY_TYPE_LABELS[d.모순_유형] || d.모순_유형 || '기타')}</span>
        <span class="importance-score" title="중요도 ${escapeHtml(d.중요도_점수)}/5">${importanceDots(d.중요도_점수)}</span>
      </div>
      <h4 class="discrepancy-title">${escapeHtml(d.항목_제목)}</h4>
      <p class="discrepancy-description">${escapeHtml(d.불일치_요약)}</p>
      <div class="discrepancy-sources">
        <div class="source-block">
          <div class="source-name">${escapeHtml(docA?.문서명)}</div>
          <blockquote>${escapeHtml(docA?.원문_인용)}</blockquote>
          <div class="source-claim">${escapeHtml(docA?.주장_내용)}</div>
        </div>
        <div class="source-block">
          <div class="source-name">${escapeHtml(docB?.문서명)}</div>
          <blockquote>${escapeHtml(docB?.원문_인용)}</blockquote>
          <div class="source-claim">${escapeHtml(docB?.주장_내용)}</div>
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
    renderResults(result, docs.length);
  } catch (err) {
    showError(err.message || String(err));
  } finally {
    setAnalyzing(false);
  }
});

loadStoredKey();
addDocumentRow();
addDocumentRow();
