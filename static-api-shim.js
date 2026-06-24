(() => {
  const nativeFetch = window.fetch.bind(window);
  const mode = location.pathname.replace(/\/$/, '') === '/demo' ? 'demo' : 'app';
  const VERSION = 'v55';
  // Storage marker for tests and documentation: jobmeta_static_demo_jobs_v55
  const stateKey = mode === 'demo' ? `jobmeta_static_demo_jobs_${VERSION}` : `jobmeta_static_app_jobs_${VERSION}`;
  const profileKey = mode === 'demo' ? `jobmeta_static_demo_profile_${VERSION}` : `jobmeta_static_app_profile_${VERSION}`;
  const datasetKey = mode === 'demo' ? `jobmeta_static_demo_dataset_${VERSION}` : `jobmeta_static_app_dataset_${VERSION}`;
  const customProfileKey = mode === 'demo' ? `jobmeta_static_demo_custom_profile_${VERSION}` : `jobmeta_static_app_custom_profile_${VERSION}`;
  let staticDataPromise = null;

  function apiResponse(payload, status = 200, headers = {}) {
    return Promise.resolve(new Response(JSON.stringify(payload), {
      status,
      headers: { 'Content-Type': 'application/json; charset=utf-8', ...headers }
    }));
  }

  function textResponse(text, type = 'text/plain; charset=utf-8', status = 200) {
    return Promise.resolve(new Response(text, { status, headers: { 'Content-Type': type } }));
  }

  function apiError(message, status = 400) {
    return apiResponse({ ok: false, error: message }, status);
  }

  function normalizeUrl(input) {
    const url = typeof input === 'string' ? input : input && input.url;
    if (!url) return '';
    try { return new URL(url, location.origin).pathname; } catch (_) { return String(url); }
  }

  async function loadStaticData() {
    if (!staticDataPromise) {
      staticDataPromise = nativeFetch('/data/static-api-data.json').then(response => {
        if (!response.ok) throw new Error('Static demo data missing');
        return response.json();
      });
    }
    return staticDataPromise;
  }

  function getJobs() {
    try { return JSON.parse(localStorage.getItem(stateKey) || '[]'); } catch (_) { return []; }
  }

  function setJobs(jobs) {
    localStorage.setItem(stateKey, JSON.stringify(jobs || []));
  }

  function getCurrentProfileKey() {
    return localStorage.getItem(profileKey) || '';
  }

  function setCurrentProfileKey(key) {
    localStorage.setItem(profileKey, key || '');
  }

  function getCurrentDatasetKey() {
    return localStorage.getItem(datasetKey) || '';
  }

  function setCurrentDatasetKey(key) {
    localStorage.setItem(datasetKey, key || '');
  }

  function readCustomProfile() {
    try { return JSON.parse(localStorage.getItem(customProfileKey) || 'null'); } catch (_) { return null; }
  }

  function writeCustomProfile(profile) {
    localStorage.setItem(customProfileKey, JSON.stringify(profile || {}));
    setCurrentProfileKey('custom');
  }

  function stableKey(job) {
    return job.job_key || `${job.source || 'manual'}|${job.title || ''}|${job.company || ''}|${job.location_remote_start || job.location || ''}`.toLowerCase();
  }

  function upsertJobs(existing, incoming, resetDemo = false) {
    const current = resetDemo ? [] : existing.slice();
    const index = new Map(current.map((job, i) => [stableKey(job), i]));
    let added = 0;
    let updated = 0;
    for (const original of incoming) {
      const job = { ...original, job_key: stableKey(original) };
      const key = stableKey(job);
      const prior = index.get(key);
      if (prior === undefined) {
        current.push(job);
        index.set(key, current.length - 1);
        added += 1;
      } else {
        const old = current[prior];
        current[prior] = {
          ...old,
          ...job,
          application_status: old.application_status || job.application_status || '',
          notes: old.notes || job.notes || '',
          priority: old.priority || job.priority || '',
          application_deadline: old.application_deadline || job.application_deadline || '',
          next_action: old.next_action || job.next_action || '',
        };
        updated += 1;
      }
    }
    current.sort((a, b) => Number(b.match_score || 0) - Number(a.match_score || 0) || String(a.title || '').localeCompare(String(b.title || '')));
    return { jobs: current, stats: { incoming: incoming.length, new: added, updated, duplicates: Math.max(0, incoming.length - added - updated) } };
  }

  function splitTerms(value) {
    return String(value || '')
      .split(/[;,|/]+/)
      .map(term => term.trim())
      .filter(term => term.length >= 2)
      .slice(0, 12);
  }

  function countTerms(jobs, fieldNames) {
    const counts = new Map();
    jobs.forEach(job => fieldNames.forEach(field => splitTerms(job[field]).forEach(term => counts.set(term, (counts.get(term) || 0) + 1))));
    return [...counts.entries()]
      .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 8)
      .map(([label, count]) => ({ label, count }));
  }

  function analyticsFor(jobs) {
    return {
      learning_priorities: countTerms(jobs, ['gap_learnable', 'must_skills', 'nice_to_have']),
      blocking_gaps: countTerms(jobs, ['gap_blocking']),
      learnable_gaps: countTerms(jobs, ['gap_learnable']),
      tools: countTerms(jobs, ['tools_systems'])
    };
  }

  function csvEscape(value) {
    const text = String(value ?? '');
    return /[",\n]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
  }

  function csvFromJobs(jobs) {
    const fields = ['source','url','company','title','role_cluster','location_remote_start','industry','main_tasks','work_pattern','tools_systems','must_skills','nice_to_have','already_have','gap_blocking','gap_learnable','gap_bonus','experience_required','entry_realistic','growth_value','interest','decision','priority','application_deadline','next_action','notes','tags','date_posted','match_score','match_reason','keywords_found','application_status','job_key'];
    return [fields.join(','), ...jobs.map(job => fields.map(field => csvEscape(job[field] ?? '')).join(','))].join('\n');
  }

  function parseCsv(text) {
    const rows = [];
    let row = [];
    let cell = '';
    let quoted = false;
    const source = String(text || '').replace(/^\uFEFF/, '');
    for (let i = 0; i < source.length; i += 1) {
      const char = source[i];
      const next = source[i + 1];
      if (quoted) {
        if (char === '"' && next === '"') {
          cell += '"';
          i += 1;
        } else if (char === '"') {
          quoted = false;
        } else {
          cell += char;
        }
      } else if (char === '"') {
        quoted = true;
      } else if (char === ',') {
        row.push(cell);
        cell = '';
      } else if (char === '\n') {
        row.push(cell);
        rows.push(row);
        row = [];
        cell = '';
      } else if (char !== '\r') {
        cell += char;
      }
    }
    if (cell || row.length) {
      row.push(cell);
      rows.push(row);
    }
    if (!rows.length) return [];
    const headers = rows.shift().map(header => header.trim());
    return rows.filter(values => values.some(value => String(value || '').trim())).map(values => {
      const record = {};
      headers.forEach((header, index) => { record[header] = values[index] || ''; });
      return record;
    });
  }

  function plainTextFromBase64(base64) {
    try {
      const binary = atob(base64 || '');
      const bytes = new Uint8Array([...binary].map(char => char.charCodeAt(0)));
      return new TextDecoder('utf-8', { fatal: false }).decode(bytes);
    } catch (_) {
      return '';
    }
  }

  function profileFromText(text, filename = '') {
    const value = `${filename}\n${text}`.toLowerCase();
    const groups = [
      { key: 'statistics', label: 'Demo-Profil Statistik / Datenanalyse', terms: ['statistik', 'statistics', 'spss', 'rstudio', 'power bi', 'quantitative', 'datenanalyse', 'reporting'] },
      { key: 'it_support', label: 'Demo-Profil IT / Support / Systeme', terms: ['systemadministrator', 'linux', 'windows server', 'support', 'netzwerk', 'active directory', 'it-support', 'troubleshooting'] },
      { key: 'information_management', label: 'Demo-Profil Informationsmanagement', terms: ['metadaten', 'bibliothek', 'informationsmanagement', 'taxonomy', 'knowledge', 'dokumentation', 'data quality'] },
    ];
    let selected = groups[0];
    let best = -1;
    for (const group of groups) {
      const score = group.terms.reduce((sum, term) => sum + (value.includes(term) ? 1 : 0), 0);
      if (score > best) { best = score; selected = group; }
    }
    return {
      profile_name: selected.label,
      base_score: 24,
      profile_source: `static-demo-cv:${filename || 'upload'}`,
      profile_notes: 'In der statischen PWA aus einer Textdatei abgeleitet. PDF-CV-Import ist in der lokalen Vollversion robuster.',
      positive_keywords: Object.fromEntries(selected.terms.map((term, index) => [term, 10 - Math.min(index, 5)])),
      negative_keywords: { senior: -12, lead: -10, sales: -8 },
      preferred_locations: { remote: 4, hamburg: 3 },
      title_boost_keywords: Object.fromEntries(selected.terms.slice(0, 5).map(term => [term, 6]))
    };
  }

  async function currentProfile(data) {
    const key = getCurrentProfileKey();
    if (key === 'custom') return readCustomProfile() || data.profiles[0]?.profile || {};
    return (data.profiles.find(item => item.key === key) || data.profiles[0] || {}).profile || {};
  }

  function allSnapshotJobs(data, profileKey, limit) {
    const scored = data.scored?.[profileKey] || data.scored?.information_management || {};
    const merged = [];
    for (const dataset of data.datasets || []) {
      const jobs = scored[dataset.key]?.jobs || [];
      merged.push(...jobs);
    }
    const deduped = upsertJobs([], merged, true).jobs;
    return deduped.slice(0, Math.max(1, Math.min(Number(limit || 50), 500)));
  }

  function updateJob(jobKey, updates) {
    const jobs = getJobs();
    const idx = jobs.findIndex(job => String(job.job_key) === String(jobKey));
    if (idx === -1) return false;
    jobs[idx] = { ...jobs[idx], ...updates };
    setJobs(jobs);
    return true;
  }

  window.fetch = async (input, init = {}) => {
    const path = normalizeUrl(input);
    if (!path.startsWith('/api/')) return nativeFetch(input, init);

    if (path === '/api/jobs' && (!init.method || init.method === 'GET')) {
      return apiResponse({ jobs: getJobs() });
    }
    if (path === '/api/analytics') {
      return apiResponse({ analytics: analyticsFor(getJobs()) });
    }
    if (path === '/api/demo-options') {
      const data = await loadStaticData();
      return apiResponse({
        notice: data.notice,
        profiles: data.profiles.map(({ key, label, description, filename }) => ({ key, label, description, filename })),
        datasets: data.datasets.map(({ key, label, description, filename, row_count }) => ({ key, label, description: `${description} (${row_count} Jobs)`, filename })),
      });
    }
    if (path === '/api/load-demo' && init.method === 'POST') {
      const request = JSON.parse(init.body || '{}');
      const data = await loadStaticData();
      const selectedProfile = request.profile_key || 'information_management';
      const selectedDataset = request.dataset_key || 'information_management';
      const profile = data.profiles.find(item => item.key === selectedProfile);
      const dataset = data.datasets.find(item => item.key === selectedDataset);
      const bundle = data.scored?.[selectedProfile]?.[selectedDataset];
      if (!profile || !dataset || !bundle) return apiError('Demo-Daten konnten nicht gefunden werden.', 404);
      const result = upsertJobs(getJobs(), bundle.jobs || [], Boolean(request.reset_demo ?? true));
      setJobs(result.jobs);
      setCurrentProfileKey(selectedProfile);
      setCurrentDatasetKey(selectedDataset);
      return apiResponse({
        ok: true,
        profile_label: profile.label,
        dataset_label: dataset.label,
        stats: result.stats,
        deleted_demo_jobs: 0,
        signals: Object.keys(profile.profile?.positive_keywords || {}).slice(0, 4),
        jobs: result.jobs,
      });
    }
    if (path.startsWith('/api/jobs/') && init.method === 'POST') {
      const jobKey = decodeURIComponent(path.slice('/api/jobs/'.length));
      const updates = JSON.parse(init.body || '{}');
      return apiResponse({ ok: updateJob(jobKey, updates), jobs: getJobs() });
    }
    if (path === '/api/export-csv') {
      return textResponse(csvFromJobs(getJobs()), 'text/csv; charset=utf-8');
    }
    if (path === '/api/import-csv' && init.method === 'POST') {
      const request = JSON.parse(init.body || '{}');
      const records = parseCsv(request.csv_text || '').map((record, index) => ({
        ...record,
        source: record.source || 'csv-import',
        job_key: record.job_key || `${record.source || 'csv'}|${record.title || record.job_title || ''}|${record.company || ''}|${record.location_remote_start || record.location || ''}|${index}`.toLowerCase(),
        title: record.title || record.job_title || '',
        location: record.location || record.location_remote_start || '',
        match_score: record.match_score || 50,
        match_reason: record.match_reason || 'Aus CSV in der statischen Demo importiert.',
        first_seen: record.first_seen || new Date().toISOString().slice(0, 10),
        last_seen: new Date().toISOString().slice(0, 10),
        seen_count: record.seen_count || 1,
      }));
      const result = upsertJobs(getJobs(), records, false);
      setJobs(result.jobs);
      return apiResponse({ ok: true, stats: result.stats, jobs: result.jobs });
    }
    if (path === '/api/manual-job' && init.method === 'POST') {
      const request = JSON.parse(init.body || '{}');
      const record = request.record || {};
      const now = new Date().toISOString().slice(0, 10);
      const job = {
        ...record,
        source: record.source || 'manual-static',
        title: record.title || 'Manueller Job',
        company: record.company || 'Unbekannt',
        location: record.location || record.location_remote_start || '',
        match_score: record.match_score || 50,
        match_reason: record.match_reason || 'Manuell in der statischen Demo angelegt.',
        first_seen: now,
        last_seen: now,
        seen_count: 1,
      };
      job.job_key = stableKey(job);
      const result = upsertJobs(getJobs(), [job], false);
      setJobs(result.jobs);
      return apiResponse({ ok: true, stats: result.stats, jobs: result.jobs });
    }
    if (path === '/api/profile') {
      const data = await loadStaticData();
      const profile = await currentProfile(data);
      if (init.method === 'POST') {
        const request = JSON.parse(init.body || '{}');
        try {
          const updated = typeof request.profile_json === 'string' ? JSON.parse(request.profile_json) : request.profile;
          writeCustomProfile(updated || profile);
          return apiResponse({ ok: true, updated: getJobs().length, rescored: getJobs().length, profile: updated || profile, jobs: getJobs() });
        } catch (error) {
          return apiError(`JSON konnte nicht gespeichert werden: ${error.message}`);
        }
      }
      return apiResponse({ profile });
    }
    if (path === '/api/profile-from-cv' && init.method === 'POST') {
      const request = JSON.parse(init.body || '{}');
      const profile = profileFromText(plainTextFromBase64(request.content_base64), request.filename || 'cv.txt');
      writeCustomProfile(profile);
      return apiResponse({ ok: true, rescored: getJobs().length, signals: Object.keys(profile.positive_keywords || {}).slice(0, 6), jobs: getJobs() });
    }
    if (path === '/api/harvest' && init.method === 'POST') {
      const request = JSON.parse(init.body || '{}');
      const data = await loadStaticData();
      const selectedProfile = getCurrentProfileKey() && getCurrentProfileKey() !== 'custom' ? getCurrentProfileKey() : 'information_management';
      const incoming = allSnapshotJobs(data, selectedProfile, request.limit || 50);
      const result = upsertJobs(getJobs(), incoming, false);
      setJobs(result.jobs);
      return apiResponse({
        ok: true,
        stats: result.stats,
        jobs: result.jobs,
        plan: { mode: request.search_mode || 'profile', queries: ['statische Recherche-Snapshots'], source: 'snapshot-demo' },
        notice: 'Die statische Live-Demo nutzt Snapshot-Daten statt Live-API-Abruf. Die lokale Vollversion kann echte Quellen abrufen.'
      });
    }
    if (path === '/api/sample' && init.method === 'POST') {
      const data = await loadStaticData();
      const incoming = allSnapshotJobs(data, 'information_management', 20);
      const result = upsertJobs(getJobs(), incoming, false);
      setJobs(result.jobs);
      return apiResponse({ ok: true, stats: result.stats, jobs: result.jobs });
    }
    if (path === '/api/public-export') {
      return apiError('GitHub-Pakete werden in der statischen PWA nicht erzeugt. Nutze die lokale Vollversion oder das fertige Public-ZIP.', 501);
    }
    return apiError('Unbekannte Demo-API.', 404);
  };
})();
