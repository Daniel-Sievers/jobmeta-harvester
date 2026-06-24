const extensionApi = globalThis.browser || globalThis.chrome;
const usesPromiseApi = Boolean(globalThis.browser);

const $ = (id) => document.getElementById(id);

function tabsQuery(query) {
  if (usesPromiseApi) return extensionApi.tabs.query(query);
  return new Promise((resolve) => extensionApi.tabs.query(query, resolve));
}

function tabsCreate(options) {
  if (usesPromiseApi) return extensionApi.tabs.create(options);
  return new Promise((resolve) => extensionApi.tabs.create(options, resolve));
}

function storageGet(defaults) {
  if (usesPromiseApi) return extensionApi.storage.local.get(defaults);
  return new Promise((resolve) => extensionApi.storage.local.get(defaults, resolve));
}

function storageSet(values) {
  if (usesPromiseApi) return extensionApi.storage.local.set(values);
  return new Promise((resolve) => extensionApi.storage.local.set(values, resolve));
}

function executeScript(options) {
  if (usesPromiseApi) return extensionApi.scripting.executeScript(options);
  return new Promise((resolve) => extensionApi.scripting.executeScript(options, resolve));
}

const fields = {
  endpoint: $("endpoint"),
  source: $("source"),
  location: $("location"),
  title: $("title"),
  company: $("company"),
  url: $("url"),
  description: $("description"),
  tags: $("tags"),
};

const statusBox = $("status");
const extractButton = $("extract");
const sendButton = $("send");
const openButton = $("openDashboard");
const checkButton = $("checkDashboard");

function setStatus(message, kind = "neutral") {
  statusBox.textContent = message;
  statusBox.className = `status ${kind}`;
}

function normalizeEndpoint(value) {
  const trimmed = String(value || "").trim().replace(/\/$/, "");
  return trimmed || "http://127.0.0.1:8765";
}

async function getActiveTab() {
  const [tab] = await tabsQuery({ active: true, currentWindow: true });
  if (!tab || !tab.id) {
    throw new Error("Kein aktiver Tab gefunden.");
  }
  return tab;
}

function inferSourceFromUrl(url) {
  try {
    const host = new URL(url).hostname.replace(/^www\./, "").toLowerCase();
    const sourceMap = [
      ["linkedin.", "LinkedIn"],
      ["stepstone.", "StepStone"],
      ["indeed.", "Indeed"],
      ["xing.", "XING"],
      ["kununu.", "kununu"],
      ["remotive.", "Remotive"],
      ["arbeitnow.", "Arbeitnow"],
      ["arbeitsagentur.", "Bundesagentur fuer Arbeit"],
      ["bund.de", "Bund.de"],
      ["greenhouse.io", "Greenhouse"],
      ["lever.co", "Lever"],
      ["ashbyhq.com", "Ashby"],
      ["workdayjobs.com", "Workday"],
      ["personio.", "Personio"],
      ["smartrecruiters.", "SmartRecruiters"],
      ["taleo.", "Taleo"],
    ];
    const match = sourceMap.find(([needle]) => host.includes(needle));
    if (match) return match[1];
    return host;
  } catch {
    return "browser-extension";
  }
}

function extractPageData() {
  const normalize = (value) => String(value || "").replace(/\s+/g, " ").trim();
  const text = (node) => normalize(node?.textContent || "");
  const meta = (selector, attr = "content") => normalize(document.querySelector(selector)?.getAttribute(attr) || "");
  const htmlToText = (html) => {
    const div = document.createElement("div");
    div.innerHTML = html || "";
    return text(div);
  };
  const first = (selectors) => {
    for (const selector of selectors) {
      const value = text(document.querySelector(selector));
      if (value) return value;
    }
    return "";
  };
  const allJsonLd = () => {
    const scripts = [...document.querySelectorAll('script[type="application/ld+json"]')];
    const values = [];
    for (const script of scripts) {
      try {
        const parsed = JSON.parse(script.textContent || "{}");
        const items = Array.isArray(parsed) ? parsed : [parsed];
        for (const item of items) {
          if (item && Array.isArray(item["@graph"])) values.push(...item["@graph"]);
          values.push(item);
        }
      } catch {
        // Ignore invalid structured data.
      }
    }
    return values.filter(Boolean);
  };
  const jsonLdItems = allJsonLd();
  const jobPosting = jsonLdItems.find((item) => {
    const type = item["@type"];
    const types = Array.isArray(type) ? type : [type];
    return types.some((entry) => String(entry || "").toLowerCase() === "jobposting");
  }) || {};
  const getOrgName = (value) => {
    if (!value) return "";
    if (typeof value === "string") return normalize(value);
    if (Array.isArray(value)) return getOrgName(value[0]);
    return normalize(value.name || value.legalName || "");
  };
  const getLocation = (job) => {
    if (job.jobLocationType && String(job.jobLocationType).toUpperCase().includes("TELECOMMUTE")) {
      return "Remote";
    }
    const location = Array.isArray(job.jobLocation) ? job.jobLocation[0] : job.jobLocation;
    const address = location?.address || location;
    const parts = [
      address?.addressLocality,
      address?.addressRegion,
      address?.addressCountry?.name || address?.addressCountry,
    ].map(normalize).filter(Boolean);
    return parts.join(" / ");
  };
  const cleanTitle = (value) => normalize(value).replace(/\s+\|\s+LinkedIn.*$/i, "");
  const inferCompanyFromTitle = (value) => {
    const title = normalize(value);
    const atMatch = title.match(/@\s*([^|\-–—,]+)/);
    if (atMatch) return normalize(atMatch[1]);
    const separators = [" bei ", " at ", " - ", " | ", " – ", " — "];
    for (const separator of separators) {
      const parts = title.split(separator).map(normalize).filter(Boolean);
      if (parts.length >= 2) {
        const candidate = parts[parts.length - 1].replace(/^(jobs?|karriere)\s*/i, "");
        if (candidate && candidate.length <= 80) return candidate;
      }
    }
    return "";
  };

  const title = cleanTitle(jobPosting.title)
    || cleanTitle(meta('meta[property="og:title"]'))
    || cleanTitle(first(["h1", "[data-testid*=title i]", "[class*=job-title i]", ".job-title"]))
    || cleanTitle(document.title);
  const company = getOrgName(jobPosting.hiringOrganization)
    || first([
      '[data-testid*=company i]',
      '[data-testid*=employer i]',
      '[data-testid*=organization i]',
      '[class*=company i]',
      '[class*=employer i]',
      '[class*=organization i]',
      '[class*=arbeitgeber i]',
      'a[href*="company"]',
      'a[href*="firma"]',
    ])
    || inferCompanyFromTitle(document.title)
    || inferCompanyFromTitle(title);
  const locationText = getLocation(jobPosting) || first([
    '[data-testid*=location i]',
    '[class*=location i]',
    '[class*=ort i]',
    '[class*=remote i]',
    '[class*=standort i]',
  ]);
  const description = htmlToText(jobPosting.description) || first([
    "main article",
    "main",
    "article",
    '[data-testid*=description i]',
    '[class*=description i]',
    '[class*=jobDescription i]',
    '[class*=stellenbeschreibung i]',
    '[id*=description i]',
  ]) || text(document.body);
  const url = jobPosting.url || meta('meta[property="og:url"]') || window.location.href;
  const datePosted = normalize(jobPosting.datePosted || meta('meta[property="article:published_time"]'));
  const validThrough = normalize(jobPosting.validThrough || "");
  const employmentType = Array.isArray(jobPosting.employmentType)
    ? jobPosting.employmentType.join(", ")
    : normalize(jobPosting.employmentType || "");

  return {
    title,
    company,
    location: locationText,
    url,
    description: description.slice(0, 4500),
    source: window.location.hostname ? window.location.hostname.replace(/^www\./, "") : "browser-extension",
    datePosted,
    validThrough,
    employmentType,
    extractionQuality: jobPosting.title ? "structured" : "heuristic",
  };
}

function fillForm(data) {
  fields.title.value = data.title || fields.title.value;
  fields.company.value = data.company || fields.company.value;
  fields.location.value = data.location || fields.location.value;
  fields.url.value = data.url || fields.url.value;
  fields.description.value = data.description || fields.description.value;
  fields.source.value = inferSourceFromUrl(data.url || fields.url.value || data.source || "");
  if (data.datePosted || data.validThrough || data.employmentType) {
    const extraTags = [data.datePosted && `date_posted:${data.datePosted}`, data.validThrough && `deadline:${data.validThrough}`, data.employmentType && `employment:${data.employmentType}`]
      .filter(Boolean)
      .join(", ");
    const current = fields.tags.value.trim();
    fields.tags.value = [current, extraTags].filter(Boolean).join(", ");
  }
}

async function extractCurrentPage() {
  extractButton.disabled = true;
  try {
    const tab = await getActiveTab();
    if (tab.url) {
      fields.url.value = tab.url;
      fields.source.value = inferSourceFromUrl(tab.url);
      if (tab.title && !fields.title.value) fields.title.value = tab.title;
    }
    const [{ result }] = await executeScript({
      target: { tabId: tab.id },
      func: extractPageData,
    });
    fillForm(result || {});
    const quality = result?.extractionQuality === "structured" ? "strukturierte Jobdaten erkannt" : "heuristisch ausgelesen";
    setStatus(`Seite ausgelesen (${quality}). Bitte kurz prüfen und senden.`, "ok");
  } catch (error) {
    setStatus(`Konnte Seite nicht auslesen: ${error.message}`, "error");
  } finally {
    extractButton.disabled = false;
  }
}

function buildRecord() {
  const tagText = fields.tags.value.trim() || "browser-extension, clipped";
  const deadlineTag = (tagText.match(/deadline:([^,]+)/i) || [])[1]?.trim() || "";
  const dateTag = (tagText.match(/date_posted:([^,]+)/i) || [])[1]?.trim() || "";
  return {
    source: fields.source.value.trim() || inferSourceFromUrl(fields.url.value) || "browser-extension",
    url: fields.url.value.trim(),
    company: fields.company.value.trim(),
    title: fields.title.value.trim(),
    role_cluster: "",
    location_remote_start: fields.location.value.trim(),
    industry: "",
    main_tasks: fields.description.value.trim().slice(0, 1200),
    work_pattern: fields.location.value.toLowerCase().includes("remote") ? "Remote/unklar" : "",
    tools_systems: "",
    must_skills: "",
    nice_to_have: "",
    already_have: "",
    gap_blocking: "",
    gap_learnable: "",
    gap_bonus: "",
    experience_required: "",
    entry_realistic: "prüfen",
    growth_value: "prüfen",
    interest: "prüfen",
    decision: "prüfen",
    priority: "",
    application_deadline: deadlineTag,
    next_action: "",
    notes: "",
    tags: tagText,
    date_posted: dateTag,
  };
}

async function checkDashboardConnection({ silent = false } = {}) {
  const endpoint = normalizeEndpoint(fields.endpoint.value);
  fields.endpoint.value = endpoint;
  try {
    const response = await fetch(`${endpoint}/api/jobs`, { method: "GET" });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    if (!silent) setStatus("Dashboard erreichbar. Du kannst Anzeigen senden.", "ok");
    return true;
  } catch (error) {
    setStatus(`Dashboard nicht erreichbar. Starte zuerst: python -m jobmeta_harvester --dashboard (${error.message})`, "error");
    return false;
  }
}

async function sendToJobMeta() {
  const endpoint = normalizeEndpoint(fields.endpoint.value);
  fields.endpoint.value = endpoint;
  const record = buildRecord();
  if (!record.url || !record.title) {
    setStatus("Titel und Anzeigenlink sollten ausgefüllt sein.", "warn");
    return;
  }

  sendButton.disabled = true;
  try {
    const response = await fetch(`${endpoint}/api/manual-job`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ record }),
    });
    let payload = {};
    try {
      payload = await response.json();
    } catch {
      // Keep default payload for non-JSON error pages.
    }
    if (!response.ok || payload.ok === false) {
      throw new Error(payload.error || `HTTP ${response.status}`);
    }
    const stats = payload.stats || {};
    setStatus(`An JobMeta gesendet: ${stats.new || 0} neu, ${stats.updated || 0} aktualisiert.`, "ok");
  } catch (error) {
    setStatus(`Senden fehlgeschlagen. Läuft das Dashboard? Starte: python -m jobmeta_harvester --dashboard (${error.message})`, "error");
  } finally {
    sendButton.disabled = false;
  }
}

async function openDashboard() {
  const endpoint = normalizeEndpoint(fields.endpoint.value);
  await tabsCreate({ url: endpoint });
}

async function init() {
  const items = await storageGet({ endpoint: "http://127.0.0.1:8765" });
  fields.endpoint.value = items.endpoint;
  try {
    const tab = await getActiveTab();
    fillForm({
      title: tab.title || "",
      url: tab.url || "",
      source: inferSourceFromUrl(tab.url || ""),
    });
    setStatus("Tab erkannt. Klicke auf Seite auslesen oder sende manuell.", "neutral");
  } catch (error) {
    setStatus(error.message, "warn");
  }
}

fields.endpoint.addEventListener("change", () => {
  const endpoint = normalizeEndpoint(fields.endpoint.value);
  fields.endpoint.value = endpoint;
  storageSet({ endpoint });
});
extractButton.addEventListener("click", extractCurrentPage);
sendButton.addEventListener("click", sendToJobMeta);
openButton.addEventListener("click", openDashboard);
checkButton.addEventListener("click", () => checkDashboardConnection());

init();
