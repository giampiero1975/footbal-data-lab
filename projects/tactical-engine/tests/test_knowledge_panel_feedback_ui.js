const assert = require('assert');
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const panelPath = path.join(__dirname, '..', 'api', 'knowledge_panel.html');
const html = fs.readFileSync(panelPath, 'utf8');
const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(match => match[1]);

class ClassList {
  constructor(element) { this.element = element; }
  values() { return new Set((this.element.className || '').split(/\s+/).filter(Boolean)); }
  contains(value) { return this.values().has(value); }
  toggle(value, force) {
    const values = this.values();
    if (force === undefined ? !values.has(value) : force) values.add(value);
    else values.delete(value);
    this.element.className = [...values].join(' ');
  }
  add(value) { this.toggle(value, true); }
  remove(value) { this.toggle(value, false); }
}

class Element {
  constructor() {
    this.textContent = '';
    this.innerHTML = '';
    this.className = '';
    this.disabled = false;
    this.attributes = {};
    this.style = {};
    this.value = '';
    this.classList = new ClassList(this);
  }
  setAttribute(name, value) { this.attributes[name] = String(value); }
  getAttribute(name) { return this.attributes[name]; }
}

const elements = new Map();
const document = {
  getElementById(id) {
    if (!elements.has(id)) elements.set(id, new Element());
    return elements.get(id);
  },
};
const context = vm.createContext({
  console,
  document,
  fetch: async () => { throw new Error('fetch non previsto nel test'); },
  Blob: class {},
  URL: { createObjectURL() { return 'blob:test'; }, revokeObjectURL() {} },
  setTimeout,
  clearTimeout,
});
for (const script of scripts) vm.runInContext(script, context, { filename: panelPath });

function run(code) { return vm.runInContext(code, context); }
function element(id) { return document.getElementById(id); }
function resetFeedbackElements() {
  for (const id of ['useful', 'notUseful', 'feedbackStatus', 'message']) elements.set(id, new Element());
  run('feedbackSaving=false; currentView=null');
}

async function main() {
  assert(html.includes('renderFeedbackState(job.feedback)'), 'la riapertura deve usare il feedback restituito dal job');

  resetFeedbackElements();
  run('renderFeedbackState()');
  assert.strictEqual(element('useful').disabled, true);
  assert.strictEqual(element('notUseful').disabled, true);
  assert.strictEqual(element('feedbackStatus').textContent, '');
  assert(!element('useful').textContent.includes('✓'));

  run("currentView={job:{id:'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'}}; renderFeedbackState({helpful:true})");
  assert(element('useful').classList.contains('feedback-selected'));
  assert.strictEqual(element('useful').getAttribute('aria-pressed'), 'true');
  assert(element('useful').textContent.includes('✓'));
  assert.strictEqual(element('feedbackStatus').textContent, 'Feedback registrato.');

  resetFeedbackElements();
  run("currentView={job:{id:'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'}}");
  run(`
    feedbackTestCalls=0;
    feedbackTestResolve=null;
    api=async function(){feedbackTestCalls++;return await new Promise(resolve=>{feedbackTestResolve=resolve})};
  `);
  const first = run('sendFeedback(true)');
  const duplicate = run('sendFeedback(false)');
  assert.strictEqual(run('feedbackTestCalls'), 1, 'un secondo clic durante il salvataggio non deve inviare');
  assert.strictEqual(element('useful').disabled, true);
  assert.strictEqual(element('notUseful').disabled, true);
  assert.strictEqual(element('feedbackStatus').textContent, 'Salvataggio feedback…');
  run("feedbackTestResolve({job_id:'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb',helpful:true,created_at:1})");
  await Promise.all([first, duplicate]);
  assert(element('useful').classList.contains('feedback-selected'));
  assert.strictEqual(element('feedbackStatus').textContent, 'Feedback registrato.');
  assert.strictEqual(element('useful').disabled, false);

  resetFeedbackElements();
  run(`
    currentView={job:{id:'cccccccccccccccccccccccccccccccc',feedback:{helpful:false}}};
    renderFeedbackState(currentView.job.feedback);
    api=async function(){throw new Error('errore simulato')};
  `);
  await run('sendFeedback(true)');
  assert(!element('useful').classList.contains('feedback-selected'), 'un errore non deve confermare il nuovo voto');
  assert(element('notUseful').classList.contains('feedback-selected'), 'il voto già persistito deve restare visibile');
  assert.strictEqual(element('feedbackStatus').textContent, 'Feedback non registrato. Riprova.');
  assert.strictEqual(element('notUseful').disabled, false);

  console.log('feedback UI differential: 4/4 PASS');
}

main().catch(error => {
  console.error(error);
  process.exitCode = 1;
});
