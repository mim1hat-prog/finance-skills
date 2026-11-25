(() => {
  'use strict';
  const $ = (id) => document.getElementById(id);
  const theme = $('theme');
  const darkPreference = window.matchMedia('(prefers-color-scheme: dark)');
  let storedTheme = 'system';
  try { storedTheme = localStorage.getItem('finance-skills-theme') || 'system'; } catch (_) { /* Private/file browser contexts may disable storage. */ }
  if (!['system', 'light', 'dark'].includes(storedTheme)) storedTheme = 'system';
  theme.value = storedTheme;
  function applyTheme() { document.documentElement.dataset.dotTheme = theme.value === 'system' ? (darkPreference.matches ? 'dark' : 'light') : theme.value; }
  theme.addEventListener('change', () => { applyTheme(); try { localStorage.setItem('finance-skills-theme', theme.value); } catch (_) {} });
  if (darkPreference.addEventListener) darkPreference.addEventListener('change', applyTheme);
  applyTheme();

  const data = window.FINANCE_SKILLS;
  const namePattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
  if (!data || !Array.isArray(data.skills) || !data.skills.length || data.skills.some((skill) => !skill || typeof skill.name !== 'string' || !namePattern.test(skill.name) || typeof skill.title !== 'string' || typeof skill.summary !== 'string' || typeof skill.category !== 'string')) {
    $('data-error').hidden = false;
    $('results-count').textContent = 'Catalogue unavailable';
    document.querySelectorAll('.library-controls input, .library-controls select').forEach((control) => { control.disabled = true; });
    return;
  }
  const skills = data.skills;
  const search = $('search');
  const category = $('category');
  const list = $('skill-list');
  const editionRadios = [...document.querySelectorAll('input[name="edition"]')];
  let edition = 'copilot';

  if (typeof data.repoUrl === 'string' && /^https:\/\/github\.com\/[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+\/?$/.test(data.repoUrl)) {
    document.querySelectorAll('.repository-link').forEach((link) => { link.href = data.repoUrl; });
  }
  const date = /^\d{4}-\d{2}-\d{2}$/.test(data.reviewedOn || '') ? data.reviewedOn : null;
  const version = /^[0-9]+\.[0-9]+\.[0-9]+(?:[-.][A-Za-z0-9.-]+)?$/.test(data.version || '') ? data.version : null;
  $('library-meta').textContent = [version ? `Version ${version}` : null, date ? `Reviewed ${date}` : null].filter(Boolean).join(' / ') || 'Versioned instructions. Separate editions.';
  const categories = [...new Set(skills.map((skill) => skill.category))].sort((a, b) => a.localeCompare(b));
  categories.forEach((value) => { const option = document.createElement('option'); option.value = value; option.textContent = value; category.append(option); });
  const query = new URLSearchParams(window.location.search);
  if (query.get('edition') === 'gemini') edition = 'gemini';
  editionRadios.forEach((radio) => { radio.checked = radio.value === edition; });
  if (categories.includes(query.get('category'))) category.value = query.get('category');
  search.value = (query.get('q') || '').slice(0, 200);

  function element(tag, className, text) {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  }
  function link(label, href, suffix, accessibleLabel) {
    const node = element('a', '', label);
    node.href = href;
    if (accessibleLabel) node.setAttribute('aria-label', accessibleLabel);
    if (suffix) { /* Labels state the action; no decorative arrow is needed. */ }
    return node;
  }
  function makeRow(skill) {
    const row = element('article', 'skill-row');
    const headingId = `skill-${skill.name}`;
    row.setAttribute('aria-labelledby', headingId);
    const meta = element('div', 'skill-category');
    const index = element('span', 'skill-index', String(skills.indexOf(skill) + 1).padStart(2, '0'));
    index.setAttribute('aria-hidden', 'true');
    meta.append(index, element('span', '', skill.category));
    const body = element('div', 'skill-body');
    const heading = element('h3', '', skill.title); heading.id = headingId;
    body.append(heading, element('p', '', skill.summary));
    if (typeof skill.prompt === 'string' && skill.prompt.trim()) {
      const details = element('details', 'skill-prompt');
      details.append(element('summary', '', 'Try this prompt'));
      const prompt = element('div', 'prompt-content');
      prompt.append(element('p', '', skill.prompt));
      const copy = element('button', 'copy-prompt', 'Copy prompt');
      copy.type = 'button';
      copy.setAttribute('aria-label', `Copy prompt for ${skill.title}`);
      copy.addEventListener('click', async () => {
        try {
          if (!navigator.clipboard?.writeText) throw new Error('Clipboard unavailable');
          await navigator.clipboard.writeText(skill.prompt);
          copy.textContent = 'Copied';
          $('copy-status').textContent = `Copied the prompt for ${skill.title}.`;
          window.setTimeout(() => { copy.textContent = 'Copy prompt'; }, 1800);
        } catch (_) {
          const range = document.createRange(); range.selectNodeContents(prompt.querySelector('p'));
          const selection = window.getSelection(); selection.removeAllRanges(); selection.addRange(range);
          copy.textContent = 'Select text and copy';
          $('copy-status').textContent = 'Automatic copy is unavailable. The prompt text is selected; use your browser’s Copy command.';
        }
      });
      prompt.append(copy); details.append(prompt); body.append(details);
    }
    const actions = element('div', 'skill-actions');
    const assistant = edition === 'copilot' ? 'Copilot' : 'Gemini';
    const download = link('Download ZIP', `../packages/${edition}/${skill.name}.zip`, '↓', `Download ${skill.title} for ${assistant}`);
    download.setAttribute('download', `${skill.name}.zip`);
    actions.append(download, link('Read skill', `../editions/${edition}/${skill.name}/SKILL.md`, '↗', `Read ${skill.title} for ${assistant}`));
    row.append(meta, body, actions); return row;
  }
  function updateURL() {
    const parameters = new URLSearchParams();
    if (edition !== 'copilot') parameters.set('edition', edition);
    if (category.value !== 'all') parameters.set('category', category.value);
    if (search.value.trim()) parameters.set('q', search.value.trim());
    const queryString = parameters.toString();
    try { window.history.replaceState(null, '', `${window.location.pathname}${queryString ? `?${queryString}` : ''}${window.location.hash}`); } catch (_) { /* file:// may forbid history updates. */ }
  }
  function render() {
    const terms = search.value.trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
    const selected = skills.filter((skill) => {
      const haystack = `${skill.name} ${skill.title} ${skill.summary} ${skill.category} ${skill.prompt || ''}`.toLocaleLowerCase();
      return (category.value === 'all' || skill.category === category.value) && terms.every((term) => haystack.includes(term));
    });
    list.replaceChildren(...selected.map(makeRow));
    $('empty-state').hidden = selected.length > 0;
    const assistant = edition === 'copilot' ? 'Copilot' : 'Gemini';
    $('results-count').textContent = `${selected.length} of ${skills.length} skills / ${assistant} edition`;
    const guide = $('edition-guide');
    guide.href = `../docs/${edition.toUpperCase()}.md`;
    guide.replaceChildren(document.createTextNode(`Read the ${assistant} setup guide `));
    
    updateURL();
  }
  search.addEventListener('input', render);
  category.addEventListener('change', render);
  editionRadios.forEach((radio) => radio.addEventListener('change', () => { edition = radio.value; render(); }));
  $('clear-filters').addEventListener('click', () => { search.value = ''; category.value = 'all'; render(); search.focus(); });
  render();
})();
