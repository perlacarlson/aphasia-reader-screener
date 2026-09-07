"""
Proyecto Lectura Accesible — Complete Narrative Clinical Engine
Department of Speech & Hearing Sciences | Portland State University

Text: Jack London — To Build a Fire (Complete 10-Scene Narrative Arc)
Linguistic Framework: Bilingual Neurogenic Adaptation Rubric (BNAR)
Clinical Tiers:
  - Tier 1: Severe Acquired Alexia (10 Scenes; <25 chars/line; canonical SVO)
  - Tier 2: Moderate Acquired Alexia (10 Scenes; <50 chars/line; propositional rail)
  - Tier 3: Mild Alexia / Book Mode (5 Chapters; flowing prose + memory dropdowns)
Interface:
  - Tri-State Language: English Only | Español Only | Both (Bilingual Canalization)
  - Visual Ergonomics: Sage-green (EN) & Sky-blue (ES) columns, 68px ARASAAC tiles, 44px targets
  - Auditory: 0.85x Web Speech API with en-US and es-MX dialect priority
"""

import os
from typing import Dict, List, Optional
from src.arasaac_client import resolve_anchor_visual

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Proyecto Lectura Accesible | Jack London — To Build a Fire</title>
  <style>
  /* Guide Trigger Button */
.guide-trigger-btn {
  margin-top: 0.75rem;
  background-color: var(--btn-bg);
  border: 2px solid var(--accent-en);
  color: var(--accent-en);
}

/* Accessible Native Dialog Modal */
.clinical-modal {
  border: 2px solid var(--border-card);
  border-radius: 16px;
  padding: 0;
  max-width: 680px;
  width: 90vw;
  background-color: var(--bg-card);
  color: var(--text-main);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.25);
}

.clinical-modal::backdrop {
  background-color: rgba(15, 23, 42, 0.65);
  backdrop-filter: blur(2px);
}

body.high-contrast .clinical-modal {
  border-color: var(--accent-en);
  box-shadow: 0 0 20px rgba(52, 211, 153, 0.2);
}

.modal-wrapper {
  padding: 1.5rem;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 2px solid var(--border-card);
  padding-bottom: 0.75rem;
  margin-bottom: 1rem;
}

.modal-header h2 {
  font-size: 1.25rem;
  margin: 0;
  color: var(--text-main);
}

.modal-close-btn {
  min-width: 44px;
  min-height: 44px;
  background: transparent;
  border: none;
  font-size: 1.25rem;
  cursor: pointer;
  color: var(--text-muted);
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-close-btn:hover {
  background-color: var(--btn-bg);
  color: var(--text-main);
}

.modal-body {
  font-size: 0.92rem;
  line-height: 1.6;
  max-height: 65vh;
  overflow-y: auto;
  padding-right: 0.5rem;
}

.modal-intro {
  margin-top: 0;
  color: var(--text-muted);
  border-left: 3px solid var(--accent-en);
  padding-left: 0.75rem;
}

.modal-section {
  margin-top: 1.25rem;
}

.modal-section h3 {
  font-size: 1rem;
  margin: 0 0 0.4rem 0;
  color: var(--accent-en);
}

.modal-list {
  margin: 0;
  padding-left: 1.25rem;
}

.modal-list li {
  margin-bottom: 0.5rem;
}

.modal-note {
  margin: 0;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  border-top: 2px solid var(--border-card);
  padding-top: 1rem;
  margin-top: 1.25rem;
}
    :root {
      --reader-font-size: 19px;
      --reader-line-height: 1.85;

      /* Standard Palette (WCAG AA Compliant) */
      --bg-canvas: #F8FAFC;
      --bg-card: #FFFFFF;
      --text-main: #0F172A;
      --text-muted: #475569;
      --border-card: #CBD5E1;
      --accent-en: #047857;
      --accent-es: #1D4ED8;
      --sync-highlight: #FEF08A;
      --sync-border: #EAB308;
      --speaking-glow-en: #A7F3D0;
      --speaking-glow-es: #BFDBFE;
      --flag-bg: #FEF3C7;
      --flag-text: #92400E;
      --btn-bg: #F1F5F9;
      --btn-border: #94A3B8;
      --anchor-bg: #EEF2F6;
      --anchor-border: #CBD5E1;

      /* Chromatic Column Separation */
      --col-en-bg: #F0FDF4;
      --col-en-border: #BBF7D0;
      --col-es-bg: #EFF6FF;
      --col-es-border: #BFDBFE;

      /* Memory Dropdown Styling */
      --recap-bg: #FAF5FF;
      --recap-border: #D8B4FE;
      --recap-text: #6B21A8;
    }

    /* High-Contrast / Glare-Reduction Mode (21:1 Contrast Ratio) */
    body.high-contrast {
      --bg-canvas: #090D16;
      --bg-card: #000000;
      --text-main: #FFFFFF;
      --text-muted: #CBD5E1;
      --border-card: #64748B;
      --accent-en: #34D399;
      --accent-es: #60A5FA;
      --sync-highlight: #FDE047;
      --sync-border: #FACC15;
      --speaking-glow-en: #064E3B;
      --speaking-glow-es: #1E3A8A;
      --flag-bg: #78350F;
      --flag-text: #FEF3C7;
      --btn-bg: #1E293B;
      --btn-border: #94A3B8;
      --anchor-bg: #1E293B;
      --anchor-border: #64748B;

      --col-en-bg: #042419;
      --col-en-border: #059669;
      --col-es-bg: #0B1E3B;
      --col-es-border: #2563EB;

      --recap-bg: #2E1065;
      --recap-border: #A855F7;
      --recap-text: #F3E8FF;
    }

    * { box-sizing: border-box; }

    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      font-size: var(--reader-font-size);
      line-height: var(--reader-line-height);
      letter-spacing: 0.02em;
      word-spacing: 0.04em;
      color: var(--text-main);
      background-color: var(--bg-canvas);
      margin: 0;
      padding: 2rem 1.5rem;
      transition: background-color 0.2s ease, color 0.2s ease;
    }

    .container {
      max-width: 1200px;
      margin: 0 auto;
    }

    header {
      margin-bottom: 1.5rem;
      border-bottom: 2px solid var(--border-card);
      padding-bottom: 1rem;
    }

    h1 {
      font-size: 1.85rem;
      margin: 0 0 0.35rem 0;
      color: var(--text-main);
      letter-spacing: -0.02em;
    }

    .metadata {
      font-size: 0.95rem;
      color: var(--text-muted);
      font-weight: 500;
    }

    .voice-badge {
      display: inline-block;
      margin-top: 0.75rem;
      font-size: 0.78rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      color: var(--text-muted);
      background: var(--bg-card);
      border: 1px solid var(--border-card);
      padding: 0.35rem 0.7rem;
      border-radius: 6px;
    }
    .voice-badge strong { color: var(--accent-en); }

    /* Accessibility Toolbar */
    .a11y-toolbar {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 1rem;
      background: var(--bg-card);
      border: 2px solid var(--border-card);
      border-radius: 12px;
      padding: 0.85rem 1.25rem;
      margin-bottom: 2rem;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
    }

    .a11y-group {
      display: flex;
      align-items: center;
      gap: 0.45rem;
    }

    .a11y-label {
      font-size: 0.8rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      color: var(--text-muted);
      margin-right: 0.2rem;
    }

    /* 44x44px Motor-Accessible Target Rules */
    .a11y-btn {
      min-width: 44px;
      min-height: 44px;
      background-color: var(--btn-bg);
      color: var(--text-main);
      border: 2px solid var(--btn-border);
      border-radius: 8px;
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 0.4rem 0.85rem;
      transition: transform 0.1s ease, border-color 0.15s ease;
    }

    .a11y-btn:hover {
      border-color: var(--accent-en);
      transform: translateY(-1px);
    }

    .a11y-btn:focus-visible {
      outline: 3px solid var(--accent-en);
      outline-offset: 2px;
    }

    .a11y-btn.is-active {
      background-color: var(--accent-en);
      color: #FFFFFF;
      border-color: var(--accent-en);
    }

    /* Bilateral Reading Grid */
    .reading-grid {
      display: grid;
      transition: all 0.2s ease;
      margin-bottom: 1rem;
    }

    .lang-column {
      border-radius: 12px;
      padding: 1.25rem;
      transition: background-color 0.2s ease, border-color 0.2s ease;
    }

    /* English Monolingual Mode */
    body.lang-en .reading-grid {
      grid-template-columns: 1fr;
      max-width: 760px;
      margin: 0 auto 1rem auto;
    }
    body.lang-en .col-en,
    body.lang-en .lang-column.en-col { display: block; background-color: var(--col-en-bg); border: 1.5px solid var(--col-en-border); }
    body.lang-en .col-es,
    body.lang-en .lang-column.es-col { display: none !important; }

    /* Spanish Monolingual Mode */
    body.lang-es .reading-grid {
      grid-template-columns: 1fr;
      max-width: 760px;
      margin: 0 auto 1rem auto;
    }
    body.lang-es .col-es,
    body.lang-es .lang-column.es-col { display: block; background-color: var(--col-es-bg); border: 1.5px solid var(--col-es-border); }
    body.lang-es .col-en,
    body.lang-es .lang-column.en-col { display: none !important; }

    /* Bilingual Dual-Column Mode */
    body.lang-both .reading-grid {
      grid-template-columns: 1fr 1fr;
      max-width: 100%;
      gap: 2rem;
    }
    body.lang-both .col-en,
    body.lang-both .lang-column.en-col {
      display: block;
      background-color: var(--col-en-bg);
      border: 2px solid var(--col-en-border);
    }
    body.lang-both .col-es,
    body.lang-both .lang-column.es-col {
      display: block;
      background-color: var(--col-es-bg);
      border: 2px solid var(--col-es-border);
    }

    .column-title {
      font-size: 0.85rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      padding-bottom: 0.5rem;
      border-bottom: 2px solid var(--border-card);
    }
    .col-en { color: var(--accent-en); }
    .col-es { color: var(--accent-es); }

    .sentence-block {
      background: var(--bg-card);
      border: 1.5px solid var(--border-card);
      border-radius: 14px;
      padding: 1.75rem;
      margin-bottom: 2rem;
      box-shadow: 0 3px 6px rgba(0, 0, 0, 0.04);
      transition: all 0.2s ease;
    }

    /* 68px ARASAAC Visual Tile */
    .anchor-header {
      display: flex;
      align-items: center;
      gap: 1.25rem;
      margin-bottom: 1.35rem;
      padding-bottom: 1rem;
      border-bottom: 2px dashed var(--border-card);
    }

    .anchor-icon-wrapper {
      width: 68px;
      height: 68px;
      background-color: var(--anchor-bg);
      border: 2px solid var(--anchor-border);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 6px;
      font-size: 2.75rem;
      flex-shrink: 0;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
      overflow: hidden;
    }

    .arasaac-icon {
      width: 100%;
      height: 100%;
      object-fit: contain;
      display: block;
    }

    body.high-contrast .arasaac-icon {
      filter: invert(1) hue-rotate(180deg) brightness(1.2);
    }

    .anchor-text-group {
      display: flex;
      flex-direction: column;
      gap: 0.2rem;
    }

    .anchor-tag {
      font-size: 0.75rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--accent-en);
    }

    .anchor-concept {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
      letter-spacing: -0.01em;
    }

    .unit-wrapper {
      display: flex;
      align-items: center;
      gap: 0.6rem;
      margin-bottom: 0.55rem;
    }

    .idea-unit {
      flex-grow: 1;
      padding: 0.45rem 0.85rem;
      border-radius: 8px;
      border-left: 4px solid transparent;
      cursor: pointer;
      text-align: left;
      background-color: var(--bg-card);
      transition: all 0.15s ease-in-out;
    }

    .idea-unit.en { border-left-color: var(--accent-en); }
    .idea-unit.es { border-left-color: var(--accent-es); color: var(--text-muted); }

    /* Cross-Linguistic Hover Synchrony */
    .idea-unit.is-active {
      background-color: var(--sync-highlight) !important;
      color: #000000 !important;
      border-left-color: var(--sync-border) !important;
      font-weight: 600;
    }

    .idea-unit.en.is-speaking {
      background-color: var(--speaking-glow-en) !important;
      border-left-color: var(--accent-en) !important;
      color: #000000 !important;
    }

    .idea-unit.es.is-speaking {
      background-color: var(--speaking-glow-es) !important;
      border-left-color: var(--accent-es) !important;
      color: #000000 !important;
    }

    body.high-contrast .idea-unit.en.is-speaking,
    body.high-contrast .idea-unit.es.is-speaking {
      color: #FFFFFF !important;
    }

    .tts-btn {
      min-width: 44px;
      min-height: 44px;
      background: var(--bg-card);
      border: 1.5px solid var(--border-card);
      border-radius: 8px;
      font-size: 1.15rem;
      cursor: pointer;
      line-height: 1;
      color: var(--text-muted);
      transition: background 0.15s ease, transform 0.1s ease;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }

    .tts-btn:hover {
      background: var(--border-card);
      transform: scale(1.05);
    }

    .tts-btn.en:focus-visible { outline: 2px solid var(--accent-en); }
    .tts-btn.es:focus-visible { outline: 2px solid var(--accent-es); }

    .clinical-alert {
      display: inline-block;
      font-size: 0.78rem;
      font-weight: 600;
      background-color: var(--flag-bg);
      color: var(--flag-text);
      padding: 0.3rem 0.7rem;
      border-radius: 6px;
      margin-bottom: 1.15rem;
    }

    /* Tier 3 Continuous Prose Mode */
    body.tier-3 .sentence-block {
      border: none;
      box-shadow: none;
      background: transparent;
      padding: 0;
      margin-bottom: 2.5rem;
    }

    body.tier-3 .anchor-header,
    body.tier-3 .clinical-alert,
    body.tier-3 .tts-btn {
      display: none;
    }

    body.tier-3 .unit-wrapper {
      display: inline;
      margin: 0;
    }

    body.tier-3 .idea-unit {
      display: inline;
      padding: 0.15rem 0.35rem;
      margin: 0;
      border-left: none;
      border-radius: 4px;
      background-color: transparent;
      line-height: 2.1;
      cursor: pointer;
    }

    body.tier-3 .idea-unit:hover {
      background-color: var(--sync-highlight) !important;
      color: #000000 !important;
    }

    body.tier-3 .idea-unit.is-speaking {
      background-color: var(--speaking-glow-en) !important;
      color: #000000 !important;
      text-decoration: underline;
    }

    /* Tier 3 Metacognitive Retrieval Accordion */
    .chapter-recap-dropdown {
      background-color: var(--recap-bg);
      border: 2px solid var(--recap-border);
      border-radius: 12px;
      margin-top: 1.35rem;
      overflow: hidden;
      transition: all 0.2s ease;
    }

    .chapter-recap-dropdown[open] {
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.06);
    }

    .recap-summary {
      min-height: 48px;
      padding: 0.75rem 1.25rem;
      font-size: 1rem;
      font-weight: 700;
      color: var(--recap-text);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: space-between;
      user-select: none;
      outline: none;
      list-style: none;
    }

    .recap-summary::-webkit-details-marker { display: none; }

    .recap-summary:hover {
      background-color: rgba(168, 85, 247, 0.08);
    }

    .recap-summary:focus-visible {
      outline: 3px solid var(--accent-en);
      outline-offset: -2px;
    }

    .recap-summary::after {
      content: '▼';
      font-size: 0.8rem;
      transition: transform 0.2s ease;
      color: var(--recap-text);
    }

    .chapter-recap-dropdown[open] .recap-summary::after {
      transform: rotate(180deg);
    }

    .recap-content-body {
      padding: 0 1.25rem 1.25rem 1.25rem;
      border-top: 1px dashed var(--recap-border);
      padding-top: 1rem;
    }

    .recap-list {
      margin: 0;
      padding-left: 1.4rem;
      font-size: 0.96rem;
      line-height: 1.7;
    }

    .recap-list li {
      margin-bottom: 0.45rem;
    }

    body.lang-en .recap-content-body [lang="es"],
    body.lang-en .recap-summary .recap-title-es { display: none !important; }

    body.lang-es .recap-content-body [lang="en"],
    body.lang-es .recap-summary .recap-title-en { display: none !important; }

    body.lang-both .recap-summary .recap-title-en,
    body.lang-both .recap-summary .recap-title-es { display: inline; }
    body.lang-both .recap-content-body [lang="en"],
    body.lang-both .recap-content-body [lang="es"] { display: block; }
  </style>
</head>
<body class="tier-2 lang-both">
  <div class="container">
  <!-- Clinical Quick-Start Guide Modal -->
<dialog id="quickstart-modal" class="clinical-modal" aria-labelledby="modal-title">
  <div class="modal-wrapper">
    <div class="modal-header">
      <h2 id="modal-title">📋 Clinical Quick-Start Guide / Guía Rápida</h2>
      <button type="button" class="modal-close-btn" onclick="closeQuickStart()" aria-label="Close Guide">✕</button>
    </div>

    <div class="modal-body">
      <p class="modal-intro">
        Designed under <strong>SCA™</strong>, <strong>Dual Coding Theory</strong>, and <strong>LPAA</strong> principles for adult neurogenic reading rehabilitation (acquired alexia, aphasia, and right-hemisphere cognitive-communication disorders).
      </p>

      <div class="modal-section">
        <h3>1. The 3-Tier Severity Continuum</h3>
        <ul class="modal-list">
          <li><strong>Tier 1 (Severe):</strong> Ultra-short canonical S-V-O clauses (&lt;25 chars/line). Deconstructs compound syntax into isolated agent-action pairs anchored by standardized 68px ARASAAC pictograms.</li>
          <li><strong>Tier 2 (Moderate):</strong> Standard propositional rail (&lt;50 chars/line). Eliminates subordinate clause regressive saccades; features salient lexical bolding and 0.85x line-level speech verification.</li>
          <li><strong>Tier 3 (Mild / Book Mode):</strong> Continuous literary paragraph layout. Integrates on-demand click-to-speak prose with collapsible (<code>&lt;details&gt;</code>) <strong>Chapter Memory Checks</strong> to scaffold macrostructural discourse recall.</li>
        </ul>
      </div>

      <div class="modal-section">
        <h3>2. Tri-State Language Scaffolding</h3>
        <ul class="modal-list">
          <li><strong>English:</strong> Displays a single, centered column (760px max-width) optimized for monolingual clients without lateral visual distraction.</li>
          <li><strong>Español:</strong> Displays a single, centered Spanish column for L1 assessment or Spanish-dominant recovery.</li>
          <li><strong>Both (Bilingual):</strong> Expands into dual-column layout with <em>bilateral chromatic canalization</em> (Sage Green for English, Sky Blue for Spanish) to prevent horizontal line bleeding and saccadic drift. Includes real-time cross-linguistic hover highlighting.</li>
        </ul>
      </div>

      <div class="modal-section">
        <h3>3. Auditory Engine Calibration</h3>
        <p class="modal-note">
          Audio playback via Web Speech API is hard-locked to <strong>0.85x speed</strong> (~125 WPM) to preserve natural prosody while accommodating reduced auditory processing speeds. Voice resolution automatically prioritizes <code>en-US</code> and Latin American / Mexican Spanish (<code>es-MX</code>).
        </p>
      </div>
    </div>

    <div class="modal-footer">
      <button type="button" class="a11y-btn is-active" onclick="closeQuickStart()">Got It / Entendido</button>
    </div>
  </div>
</dialog>
    <header>
      <h1>To Build a Fire — Jack London</h1><button type="button" class="a11y-btn guide-trigger-btn" onclick="openQuickStart()" aria-haspopup="dialog">
  📋 Clinical Evaluator Guide
</button>
      <div class="metadata">Proyecto Lectura Accesible • Department of Speech & Hearing Sciences • Portland State University</div>
      <div id="voice-status" class="voice-badge">Resolving clinical speech engines...</div>
    </header>

    <section class="a11y-toolbar" aria-label="Reading Controls">
      <div class="a11y-group">
        <span class="a11y-label">Tier:</span>
        <button type="button" id="btn-tier-1" class="a11y-btn" onclick="setSeverityTier('tier-1')">Tier 1 (Severe)</button>
        <button type="button" id="btn-tier-2" class="a11y-btn is-active" onclick="setSeverityTier('tier-2')">Tier 2 (Moderate)</button>
        <button type="button" id="btn-tier-3" class="a11y-btn" onclick="setSeverityTier('tier-3')">Tier 3 (Mild/Book)</button>
      </div>

      <div class="a11y-group">
        <span class="a11y-label">Language:</span>
        <button type="button" id="btn-lang-en" class="a11y-btn" onclick="setLanguageMode('en')">English</button>
        <button type="button" id="btn-lang-es" class="a11y-btn" onclick="setLanguageMode('es')">Español</button>
        <button type="button" id="btn-lang-both" class="a11y-btn is-active" onclick="setLanguageMode('both')">Both</button>
      </div>

      <div class="a11y-group">
        <span class="a11y-label">Size:</span>
        <button type="button" class="a11y-btn is-active" onclick="setFontSize('19px', this)">A</button>
        <button type="button" class="a11y-btn" onclick="setFontSize('23px', this)">A+</button>
        <button type="button" class="a11y-btn" onclick="setFontSize('27px', this)">A++</button>
      </div>

      <div class="a11y-group">
        <span class="a11y-label">Visual:</span>
        <button type="button" id="contrast-toggle" class="a11y-btn" onclick="toggleContrast()" aria-pressed="false">
          🌓 High Contrast
        </button>
      </div>
    </section>

    <div class="reading-grid">
      <div class="column-title col-en">English (Primary Adapted)</div>
      <div class="column-title col-es">Español (Andamiaje Clínico)</div>
    </div>

    <main id="narrative-canvas">
      <div id="content-tier-1" class="tier-view" style="display: none;">
        __TIER_1_BLOCKS__
      </div>

      <div id="content-tier-2" class="tier-view">
        __TIER_2_BLOCKS__
      </div>

      <div id="content-tier-3" class="tier-view" style="display: none;">
        __TIER_3_BLOCKS__
      </div>
    </main>

    <footer style="margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--border-card); font-size: 0.75rem; color: var(--text-muted); text-align: center;">
      Pictographic symbols used in this reader are property of the Government of Aragón and were created by Sergio Palao for 
      <a href="http://www.arasaac.org" target="_blank" rel="noopener" style="color: inherit; font-weight: 700;">ARASAAC</a>, 
      licensed under Creative Commons (BY-NC-SA). Adapted for clinical speech-language pathology research at Portland State University.
    </footer>
  </div>

  <script>
  const quickstartModal = document.getElementById('quickstart-modal');

function openQuickStart() {
  if (quickstartModal) {
    quickstartModal.showModal();
  }
}

function closeQuickStart() {
  if (quickstartModal) {
    quickstartModal.close();
  }
}

// Close when clicking the backdrop outside the modal card
if (quickstartModal) {
  quickstartModal.addEventListener('click', (event) => {
    const rect = quickstartModal.getBoundingClientRect();
    const isInDialog = (
      rect.top <= event.clientY &&
      event.clientY <= rect.top + rect.height &&
      rect.left <= event.clientX &&
      event.clientX <= rect.left + rect.width
    );
    if (!isInDialog) {
      quickstartModal.close();
    }
  });
}
    function setSeverityTier(tierName) {
      document.body.classList.remove('tier-1', 'tier-2', 'tier-3');
      document.body.classList.add(tierName);

      document.querySelectorAll('.tier-view').forEach(el => el.style.display = 'none');
      document.getElementById('content-' + tierName).style.display = 'block';

      ['tier-1', 'tier-2', 'tier-3'].forEach(t => {
        const btn = document.getElementById('btn-' + t);
        if (btn) btn.classList.toggle('is-active', t === tierName);
      });
    }

    function setLanguageMode(mode) {
      document.body.classList.remove('lang-en', 'lang-es', 'lang-both');
      document.body.classList.add('lang-' + mode);

      ['en', 'es', 'both'].forEach(m => {
        const btn = document.getElementById('btn-lang-' + m);
        if (btn) btn.classList.toggle('is-active', m === mode);
      });
    }

    function setFontSize(sizeValue, buttonEl) {
      document.documentElement.style.setProperty('--reader-font-size', sizeValue);
      document.querySelectorAll('.a11y-group .a11y-btn').forEach(btn => {
        if (['A', 'A+', 'A++'].includes(btn.innerText)) btn.classList.remove('is-active');
      });
      if (buttonEl) buttonEl.classList.add('is-active');
    }

    function toggleContrast() {
      const body = document.body;
      const toggleBtn = document.getElementById('contrast-toggle');
      const isHighContrast = body.classList.toggle('high-contrast');
      toggleBtn.setAttribute('aria-pressed', isHighContrast ? 'true' : 'false');
      toggleBtn.classList.toggle('is-active', isHighContrast);
    }

    document.addEventListener('DOMContentLoaded', () => {
      const units = document.querySelectorAll('.idea-unit');
      units.forEach(unit => {
        const syncId = unit.dataset.sync;
        if (!syncId) return;

        unit.addEventListener('mouseenter', () => {
          document.querySelectorAll(`[data-sync="${syncId}"]`).forEach(el => el.classList.add('is-active'));
        });
        unit.addEventListener('mouseleave', () => {
          document.querySelectorAll(`[data-sync="${syncId}"]`).forEach(el => el.classList.remove('is-active'));
        });

        unit.addEventListener('click', () => {
          if (document.body.classList.contains('tier-3')) {
            const lang = unit.classList.contains('en') ? 'en-US' : 'es-US';
            playSpeech(unit.innerText, syncId, lang);
          }
        });
      });
    });

    let availableVoices = [];

    function updateBadge() {
      const enVoice = getBestVoice('en');
      const esVoice = getBestVoice('es');
      const badge = document.getElementById('voice-status');
      if (!badge) return;

      const enName = enVoice ? `${enVoice.name} (${enVoice.lang})` : 'Default System Voice';
      const esName = esVoice ? `${esVoice.name} (${esVoice.lang})` : 'Voz por defecto';

      badge.innerHTML = `🎙️ <strong>EN (0.85x):</strong> ${enName} &nbsp;|&nbsp; <strong>ES (0.85x):</strong> ${esName}`;
    }

    function populateVoices() {
      availableVoices = window.speechSynthesis.getVoices();
      if (availableVoices.length > 0) updateBadge();
    }

    populateVoices();
    if (speechSynthesis.onvoiceschanged !== undefined) {
      speechSynthesis.onvoiceschanged = populateVoices;
    }

    function getBestVoice(langPrefix) {
      if (!availableVoices.length) availableVoices = window.speechSynthesis.getVoices();

      if (langPrefix.startsWith('es')) {
        return (
          availableVoices.find(v => v.lang === 'es-MX' || v.name.toLowerCase().includes('mexico') || v.name.includes('Paulina')) ||
          availableVoices.find(v => v.lang === 'es-US') ||
          availableVoices.find(v => v.lang === 'es-419') ||
          availableVoices.find(v => v.lang.startsWith('es')) ||
          null
        );
      } else {
        return (
          availableVoices.find(v => v.lang === 'en-US' || v.name.includes('Samantha') || v.name.includes('US')) ||
          availableVoices.find(v => v.lang.startsWith('en')) ||
          null
        );
      }
    }

    function playSpeech(text, syncId, targetLang) {
      if (!('speechSynthesis' in window)) {
        alert('Web Speech API is not supported in this browser.');
        return;
      }

      window.speechSynthesis.cancel();
      window.speechSynthesis.resume();

      const cleanText = text.replace(/<[^>]*>/g, '').replace(/[—–-]/g, '').trim();
      const utterance = new SpeechSynthesisUtterance(cleanText);
      utterance.rate = 0.85;
      utterance.pitch = 1.0;

      const voice = getBestVoice(targetLang);
      if (voice) {
        utterance.voice = voice;
        utterance.lang = voice.lang;
      } else {
        utterance.lang = targetLang;
      }

      const targetClass = targetLang.startsWith('en') ? '.idea-unit.en' : '.idea-unit.es';
      const activeUnit = document.querySelector(`${targetClass}[data-sync="${syncId}"]`);

      utterance.onstart = () => { if (activeUnit) activeUnit.classList.add('is-speaking'); };
      utterance.onend = () => { if (activeUnit) activeUnit.classList.remove('is-speaking'); };
      utterance.onerror = () => { if (activeUnit) activeUnit.classList.remove('is-speaking'); };

      window.speechSynthesis.speak(utterance);
    }
  </script>
</body>
</html>
"""

def generate_sentence_block(block_idx: int, prefix: str, en_lines: List[str], es_lines: List[str], anchor: Dict, recap: Optional[Dict] = None) -> str:
    """Assembles an accessible bilingual block with dedicated language column containers."""
    en_markup = []
    for l_idx, line in enumerate(en_lines):
        sync_key = f"{prefix}-b{block_idx}-l{l_idx}"
        clean_js = line.replace('"', '&quot;').replace("'", "\\'")
        en_markup.append(f"""
        <div class="unit-wrapper">
          <button class="tts-btn en" onclick="playSpeech('{clean_js}', '{sync_key}', 'en-US')" title="Listen in English" aria-label="Listen in English">🔊</button>
          <div class="idea-unit en" data-sync="{sync_key}">{line}</div>
        </div>
        """)

    es_markup = []
    for l_idx, line in enumerate(es_lines):
        sync_key = f"{prefix}-b{block_idx}-l{l_idx}"
        clean_js = line.replace('"', '&quot;').replace("'", "\\'")
        es_markup.append(f"""
        <div class="unit-wrapper">
          <button class="tts-btn es" onclick="playSpeech('{clean_js}', '{sync_key}', 'es-US')" title="Escuchar en español" aria-label="Escuchar en español">🔊</button>
          <div class="idea-unit es" data-sync="{sync_key}">{line}</div>
        </div>
        """)

    alert_html = f'<div class="clinical-alert">{anchor["alert"]}</div>' if anchor.get("alert") else ""

    recap_html = ""
    if recap:
        en_recap_items = "".join(f"<li>{item}</li>" for item in recap["en"])
        es_recap_items = "".join(f"<li>{item}</li>" for item in recap["es"])
        recap_html = f"""
        <details class="chapter-recap-dropdown">
          <summary class="recap-summary">
            <span class="recap-title-en">🧠 Chapter Memory Check (Tap to expand)</span>
            <span class="recap-title-es">🧠 Repaso del Capítulo (Tocar para ver)</span>
          </summary>
          <div class="recap-content-body">
            <div lang="en">
              <strong style="color: var(--accent-en); display: block; margin-bottom: 0.5rem;">Key Takeaways:</strong>
              <ul class="recap-list">{en_recap_items}</ul>
            </div>
            <div lang="es" style="margin-top: 0.75rem;">
              <strong style="color: var(--accent-es); display: block; margin-bottom: 0.5rem;">Puntos Principales:</strong>
              <ul class="recap-list">{es_recap_items}</ul>
            </div>
          </div>
        </details>
        """

    return f"""
    <div class="sentence-block">
      <div class="anchor-header">
        <div class="anchor-icon-wrapper" aria-hidden="true">{anchor['icon']}</div>
        <div class="anchor-text-group">
          <span class="anchor-tag">{anchor['tag']}</span>
          <span class="anchor-concept">{anchor['concept']}</span>
        </div>
      </div>
      {alert_html}
      <div class="reading-grid">
        <div class="lang-column en-col" lang="en">{''.join(en_markup)}</div>
        <div class="lang-column es-col" lang="es">{''.join(es_markup)}</div>
      </div>
      {recap_html}
    </div>
    """

def build_master_reader(output_path: str = "output/bilingual_preview.html"):
    """Compiles the complete 10-scene narrative arc into the 3-tier clinical reader."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # =========================================================================
    # TIER 1: SEVERE ACQUIRED ALEXIA (10 Complete Scenes; <25 Chars/Line; SVO)
    # =========================================================================
    t1_en = [
        # Scene 1: The Trail
        ["The day was <strong>cold</strong>.", "The snow was <strong>deep</strong>.", "A man <strong>walked</strong>.", "A dog <strong>followed</strong>."],
        # Scene 2: Nine O'Clock
        ["It was <strong>nine o'clock</strong>.", "There was <strong>no sun</strong>.", "The sky was <strong>gray</strong>."],
        # Scene 3: Extreme Cold
        ["The air was <strong>freezing</strong>.", "Spit <strong>cracked</strong> in air.", "It was <strong>fifty below</strong>."],
        # Scene 4: The Dog
        ["The dog had <strong>gray fur</strong>.", "The dog was a <strong>husky</strong>.", "The dog felt the <strong>cold</strong>."],
        # Scene 5: Hidden Springs
        ["Water ran under <strong>snow</strong>.", "The ice was <strong>thin</strong>.", "It was a hidden <strong>trap</strong>."],
        # Scene 6: Breaking the Ice
        ["The dog broke the <strong>ice</strong>.", "Its paws got <strong>wet</strong>.", "The dog bit the <strong>ice off</strong>."],
        # Scene 7: The Man Falls In
        ["The man fell in <strong>water</strong>.", "His feet got <strong>wet</strong>.", "He must make a <strong>fire</strong>."],
        # Scene 8: Building the Fire
        ["He gathered dry <strong>twigs</strong>.", "He lit a small <strong>fire</strong>.", "The flame grew <strong>warm</strong>."],
        # Scene 9: The Snow Falls
        ["Snow fell from a <strong>tree</strong>.", "Snow hit the <strong>fire</strong>.", "The fire went <strong>out</strong>."],
        # Scene 10: The Sleep & The Dog
        ["His hands were <strong>frozen</strong>.", "The man went to <strong>sleep</strong>.", "The dog ran to <strong>camp</strong>."]
    ]

    t1_es = [
        # Scene 1: El camino
        ["El día estaba <strong>frío</strong>.", "La nieve era <strong>profunda</strong>.", "Un hombre <strong>caminaba</strong>.", "Un perro lo <strong>seguía</strong>."],
        # Scene 2: Las nueve
        ["Eran las <strong>nueve</strong>.", "No había <strong>sol</strong>.", "El cielo estaba <strong>gris</strong>."],
        # Scene 3: Frío extremo
        ["El aire era <strong>helado</strong>.", "La saliva <strong>tronó</strong> al caer.", "Hacía <strong>mucho frío</strong>."],
        # Scene 4: El perro
        ["El perro tenía <strong>pelo gris</strong>.", "El perro era un <strong>husky</strong>.", "El perro sentía el <strong>peligro</strong>."],
        # Scene 5: Manantiales ocultos
        ["Había agua bajo la <strong>nieve</strong>.", "El hielo era muy <strong>delgado</strong>.", "Era una <strong>trampa</strong> oculta."],
        # Scene 6: El perro en el agua
        ["El perro rompió el <strong>hielo</strong>.", "Sus patas se <strong>mojaron</strong>.", "El perro mordió el <strong>hielo</strong>."],
        # Scene 7: El hombre cae
        ["El hombre cayó al <strong>agua</strong>.", "Sus pies se <strong>mojaron</strong>.", "Él debe hacer un <strong>fuego</strong>."],
        # Scene 8: Encender el fuego
        ["Juntó ramas <strong>secas</strong>.", "Encendió un pequeño <strong>fuego</strong>.", "La llama daba <strong>calor</strong>."],
        # Scene 9: Cae la nieve
        ["Cayó nieve de un <strong>pino</strong>.", "La nieve apagó el <strong>fuego</strong>.", "El fuego se <strong>murió</strong>."],
        # Scene 10: El sueño y el perro
        ["Sus manos se <strong>congelaron</strong>.", "El hombre se quedó <strong>dormido</strong>.", "El perro corrió al <strong>campamento</strong>."]
    ]

    t1_anchors = [
        {"tag": "Tier 1 • Scene 1", "icon": resolve_anchor_visual("pine_forest", "🌲"), "concept": "The Cold Trail / El camino frío", "alert": None},
        {"tag": "Tier 1 • Scene 2", "icon": resolve_anchor_visual("clock", "⏱️"), "concept": "Nine O'Clock / Las nueve de la mañana", "alert": None},
        {"tag": "Tier 1 • Scene 3", "icon": resolve_anchor_visual("extreme_cold", "❄️"), "concept": "Extreme Cold (-50°) / Frío extremo", "alert": None},
        {"tag": "Tier 1 • Scene 4", "icon": resolve_anchor_visual("husky_wolf_dog", "🐺"), "concept": "The Wolf-Dog / El perro husky", "alert": None},
        {"tag": "Tier 1 • Scene 5", "icon": resolve_anchor_visual("danger", "⚠️"), "concept": "Hidden Water Traps / Trampas de agua", "alert": None},
        {"tag": "Tier 1 • Scene 6", "icon": resolve_anchor_visual("boots", "🐾"), "concept": "The Dog Breaks Through / El perro cae", "alert": None},
        {"tag": "Tier 1 • Scene 7", "icon": resolve_anchor_visual("boots", "🥾"), "concept": "Wet Boots / Las botas mojadas", "alert": "⚠️ Critical Event: Wet feet in freezing air"},
        {"tag": "Tier 1 • Scene 8", "icon": resolve_anchor_visual("fire", "🔥"), "concept": "The Life-Saving Fire / El fuego", "alert": None},
        {"tag": "Tier 1 • Scene 9", "icon": resolve_anchor_visual("extreme_cold", "🌲❄️"), "concept": "The Snow Falls / Cae la nieve", "alert": "⚠️ Disaster: Fire extinguished"},
        {"tag": "Tier 1 • Scene 10", "icon": resolve_anchor_visual("husky_wolf_dog", "💤"), "concept": "Peaceful Sleep / Sueño y supervivencia", "alert": None}
    ]

    t1_blocks = [generate_sentence_block(i, "t1", t1_en[i], t1_es[i], t1_anchors[i]) for i in range(len(t1_en))]

    # =========================================================================
    # TIER 2: MODERATE ACQUIRED ALEXIA (10 Complete Scenes; <50 Chars; SVO)
    # =========================================================================
    t2_en = [
        # Scene 1: The Trail
        [
            "The morning was <strong>cold and gray</strong>.",
            "A man walked on the <strong>Yukon trail</strong>.",
            "He climbed up a <strong>steep dirt hill</strong>.",
            "A narrow path led into the <strong>forest</strong>.",
            "The forest was full of <strong>pine trees</strong>."
        ],
        # Scene 2: Nine O'Clock
        [
            "The man stopped to <strong>check the time</strong>.",
            "It was <strong>nine o'clock</strong> in the morning.",
            "There was <strong>no sun</strong> in the sky.",
            "A thick white fog covered the <strong>entire land</strong>."
        ],
        # Scene 3: Extreme Cold
        [
            "The man spat into the <strong>freezing air</strong>.",
            "There was a sharp <strong>crackling noise</strong>.",
            "His spit <strong>turned to ice</strong> in mid-air.",
            "He knew the cold was <strong>fifty degrees below zero</strong>."
        ],
        # Scene 4: The Dog
        [
            "A large dog walked <strong>behind the man</strong>.",
            "The dog was a <strong>husky wolf-dog</strong>.",
            "The dog was <strong>afraid of the terrible cold</strong>.",
            "The animal knew it was <strong>too cold to travel</strong>."
        ],
        # Scene 5: Hidden Springs
        [
            "The man walked along a <strong>frozen creek</strong>.",
            "Hidden water ran under the <strong>soft snow</strong>.",
            "The deep pools were <strong>dangerous traps</strong>.",
            "He watched the snow with <strong>great care</strong>."
        ],
        # Scene 6: The Dog Breaks Ice
        [
            "The man forced the dog to <strong>walk ahead</strong>.",
            "The dog fell through a <strong>sheet of ice</strong>.",
            "The animal wet its <strong>legs and paws</strong>.",
            "It bit the ice off between its <strong>toes</strong>."
        ],
        # Scene 7: The Accident
        [
            "The man stepped on a <strong>patch of soft snow</strong>.",
            "He broke through the <strong>hidden ice</strong>.",
            "The freezing water soaked his <strong>boots and socks</strong>.",
            "He was angry because he had to <strong>stop and dry off</strong>."
        ],
        # Scene 8: Building the Fire
        [
            "He built a fire under a <strong>large pine tree</strong>.",
            "He gathered dry <strong>grass and pine needles</strong>.",
            "A match produced a small <strong>warm flame</strong>.",
            "He added larger twigs and the <strong>fire grew strong</strong>."
        ],
        # Scene 9: The Snow Extinguishes Fire
        [
            "The tree branches held a heavy <strong>pile of snow</strong>.",
            "The man pulled twigs and <strong>shook the tree</strong>.",
            "A heavy load of snow fell <strong>onto the fire</strong>.",
            "The fire was completely <strong>put out</strong>."
        ],
        # Scene 10: The Sleep & The Dog Escapes
        [
            "His fingers were frozen like <strong>blocks of wood</strong>.",
            "He could not light a <strong>single match</strong>.",
            "The man sat in the snow and fell <strong>asleep</strong>.",
            "The dog smelled death and ran to the <strong>camp</strong>."
        ]
    ]

    t2_es = [
        # Scene 1: El camino
        [
            "La mañana estaba <strong>fría y gris</strong>.",
            "Un hombre caminaba por el <strong>camino de Yukón</strong>.",
            "Él subió por una <strong>colina de tierra</strong>.",
            "Un sendero estrecho entraba al <strong>bosque</strong>.",
            "El bosque estaba lleno de <strong>pinos</strong>."
        ],
        # Scene 2: Las nueve
        [
            "El hombre se detuvo a <strong>mirar la hora</strong>.",
            "Eran las <strong>nueve de la mañana</strong>.",
            "No había <strong>sol</strong> en el cielo.",
            "Una niebla blanca cubría <strong>toda la tierra</strong>."
        ],
        # Scene 3: Frío extremo
        [
            "El hombre escupió en el <strong>aire congelado</strong>.",
            "Hubo un sonido <strong>seco y crujiente</strong>.",
            "La saliva <strong>se convirtió en hielo</strong> en el aire.",
            "Él supo que el frío era de <strong>cincuenta grados bajo cero</strong>."
        ],
        # Scene 4: El perro
        [
            "Un perro grande caminaba <strong>detrás del hombre</strong>.",
            "El perro era un <strong>husky cruzado con lobo</strong>.",
            "El animal tenía <strong>miedo del frío extremo</strong>.",
            "El perro sabía que era <strong>peligroso viajar</strong>."
        ],
        # Scene 5: Manantiales ocultos
        [
            "El hombre caminaba junto al <strong>arroyo helado</strong>.",
            "El agua oculta corría bajo la <strong>nieve suave</strong>.",
            "Las pozas de agua eran <strong>trampas peligrosas</strong>.",
            "Él miraba la nieve con <strong>mucho cuidado</strong>."
        ],
        # Scene 6: El perro en el agua
        [
            "El hombre obligó al perro a <strong>caminar adelante</strong>.",
            "El perro cayó en una <strong>capa de hielo</strong>.",
            "El animal se mojó las <strong>patas</strong>.",
            "El perro mordió el hielo entre sus <strong>dedos</strong>."
        ],
        # Scene 7: El accidente
        [
            "El hombre pisó una <strong>zona de nieve blanda</strong>.",
            "Él rompió el <strong>hielo oculto</strong>.",
            "El agua congelada mojó sus <strong>botas y calcetines</strong>.",
            "Él se enojó porque debía <strong>parar a secarse</strong>."
        ],
        # Scene 8: Encender el fuego
        [
            "Él hizo una fogata debajo de un <strong>gran pino</strong>.",
            "Juntó pasto seco y <strong>hojas de pino</strong>.",
            "Un fósforo encendió una pequeña <strong>llama tibia</strong>.",
            "Añadió ramas más grandes y el <strong>fuego creció fuerte</strong>."
        ],
        # Scene 9: La nieve sobre el fuego
        [
            "Las ramas del pino tenían una <strong>carga de nieve</strong>.",
            "El hombre jaló ramas y <strong>sacudió el árbol</strong>.",
            "Un montón de nieve cayó <strong>sobre el fuego</strong>.",
            "El fuego se apagó por <strong>completo</strong>."
        ],
        # Scene 10: El sueño y el perro
        [
            "Sus dedos estaban duros como <strong>pedazos de madera</strong>.",
            "Él no pudo encender ningún <strong>otro fósforo</strong>.",
            "El hombre se sentó en la nieve y se quedó <strong>dormido</strong>.",
            "El perro olió la muerte y corrió al <strong>campamento</strong>."
        ]
    ]

    t2_anchors = [
        {"tag": "Tier 2 • Scene 1", "icon": resolve_anchor_visual("pine_forest", "🌲"), "concept": "The Yukon Trail / El camino de Yukón", "alert": None},
        {"tag": "Tier 2 • Scene 2", "icon": resolve_anchor_visual("clock", "⏱️"), "concept": "Nine O'Clock & No Sun / Las nueve de la mañana", "alert": None},
        {"tag": "Tier 2 • Scene 3", "icon": resolve_anchor_visual("extreme_cold", "❄️"), "concept": "Extreme Cold (-50°) / Frío extremo (-50 grados)", "alert": "⚠️ Sensory Landmark: Ice crackling in mid-air"},
        {"tag": "Tier 2 • Scene 4", "icon": resolve_anchor_visual("husky_wolf_dog", "🐺"), "concept": "The Husky Wolf-Dog / El perro husky", "alert": None},
        {"tag": "Tier 2 • Scene 5", "icon": resolve_anchor_visual("danger", "⚠️"), "concept": "Hidden Water Traps / Los manantiales ocultos", "alert": None},
        {"tag": "Tier 2 • Scene 6", "icon": resolve_anchor_visual("boots", "🐾"), "concept": "The Dog Tests the Ice / El perro prueba el hielo", "alert": None},
        {"tag": "Tier 2 • Scene 7", "icon": resolve_anchor_visual("boots", "🥾"), "concept": "The Boots Breakthrough / Las botas en el agua", "alert": "⚠️ High Risk: Wet feet require an immediate fire"},
        {"tag": "Tier 2 • Scene 8", "icon": resolve_anchor_visual("fire", "🔥"), "concept": "Building the Life Fire / Encender el fuego", "alert": None},
        {"tag": "Tier 2 • Scene 9", "icon": resolve_anchor_visual("extreme_cold", "🌲❄️"), "concept": "The Snow Avalanche / La nieve apaga el fuego", "alert": "⚠️ Catastrophic Event: Fire extinguished by snow"},
        {"tag": "Tier 2 • Scene 10", "icon": resolve_anchor_visual("husky_wolf_dog", "💤"), "concept": "The Final Sleep / El sueño final y la salvación", "alert": None}
    ]

    t2_blocks = [generate_sentence_block(i, "t2", t2_en[i], t2_es[i], t2_anchors[i]) for i in range(len(t2_en))]

    # =========================================================================
    # TIER 3: MILD / AUTONOMOUS BOOK MODE (5 Chapters with Memory Recaps)
    # =========================================================================
    t3_en = [
        # Chapter 1: The Trail and the Cold (Scenes 1-2)
        [
            "Day had broken cold and gray, exceedingly cold and gray, in the deep Yukon wilderness.",
            "A solitary traveler turned aside from the main trail and climbed the steep earth bank into the pine forest.",
            "He paused for breath at the top and checked his watch.",
            "It was nine o'clock in the morning, and there was no sun nor hint of sun in the clear, empty sky.",
            "A thick white gloom hung over the face of the frozen world."
        ],
        # Chapter 2: The Dog and the Cold (Scenes 3-4)
        [
            "The man spat into the freezing air, and there was a sharp, dry crackle before it touched the snow.",
            "He knew that at fifty degrees below zero spittle crackled on the snow, but this had crackled in mid-air.",
            "At the man's heels trotted a large native husky dog, gray-coated and looking like a wild timber wolf.",
            "The animal was depressed by the tremendous cold and knew by instinct that it was too dangerous to travel.",
            "In reality, the cold was seventy-five degrees below zero, and danger was everywhere."
        ],
        # Chapter 3: The Hidden Traps and the Accident (Scenes 5-7)
        [
            "The man continued walking along the frozen bed of Henderson Creek.",
            "He knew that unfrozen mountain springs flowed beneath the snow, creating deadly water traps.",
            "The man forced the dog to walk ahead, and the animal broke through a crust of ice, wetting its legs.",
            "A mile farther, the man himself stepped into a hidden spring and soaked his boots halfway to his knees.",
            "He cursed his bad luck, knowing he had to build a fire immediately to dry his feet or lose them to frostbite."
        ],
        # Chapter 4: The Fire and the Disaster (Scenes 8-9)
        [
            "The man worked carefully to build a fire beneath the sheltering boughs of a large spruce pine.",
            "He lit a dry curl of birch bark with a sulfur match and nurtured a small, crackling flame.",
            "The fire grew strong, and the man felt safe and triumphant over the deadly cold.",
            "Then disaster struck: the tree branches were overloaded with snow from weeks of winter storms.",
            "Each time he pulled a twig, the tree shook, until a huge avalanche of snow fell directly onto the fire and smothered it into smoke."
        ],
        # Chapter 5: The Frozen Matches, the Run, and the Sleep (Scene 10)
        [
            "The man panicked as the cold crept into his bones, and his fingers turned into frozen blocks of wood.",
            "He struck the entire bundle of seventy matches at once against his leg, but his numb hands dropped them into the snow.",
            "In a final burst of fear, he ran wildly down the trail, but his freezing legs gave out and he collapsed.",
            "A comfortable warmth came over him, and he sat against a pine tree, drifting into a peaceful, eternal sleep.",
            "The dog sat and waited, smelled the scent of death on the quiet body, and turned to trot toward the warm fires of the camp."
        ]
    ]

    t3_es = [
        # Capítulo 1: El camino y el frío
        [
            "El día había comenzado frío y gris, sumamente frío y gris, en el desierto blanco de Yukón.",
            "Un viajero solitario se desvió del camino principal y subió una pendiente de tierra para entrar al bosque de pinos.",
            "Se detuvo en la cima a tomar aire y miró su reloj.",
            "Eran las nueve de la mañana y no había rastro de sol en el cielo despejado y vacío.",
            "Una densa niebla blanca cubría por completo la tierra congelada."
        ],
        # Capítulo 2: El perro y el frío extremo
        [
            "El hombre escupió en el aire congelado y la saliva produjo un chasquido seco antes de tocar la nieve.",
            "Él sabía que a cincuenta bajo cero la saliva tronaba en la nieve, pero esta había tronado en el aire.",
            "Detrás del hombre caminaba un perro grande, un husky con pelo gris parecido a un lobo salvaje.",
            "El animal estaba desanimado por el frío tremendo y su instinto le advertía que era peligroso viajar.",
            "En realidad, la temperatura era de setenta y cinco grados bajo cero y el peligro estaba en todas partes."
        ],
        # Capítulo 3: Las trampas ocultas y el accidente
        [
            "El hombre continuó caminando junto al cauce congelado del arroyo.",
            "Él sabía que manantiales ocultos corrían bajo la nieve, creando peligrosas trampas de agua.",
            "El hombre obligó al perro a caminar adelante, y el animal rompió una capa de hielo y se mojó las patas.",
            "Una milla después, el hombre pisó una trampa oculta y el agua helada le cubrió las botas hasta las rodillas.",
            "Maldijo su mala suerte, sabiendo que debía encender un fuego de inmediato para secarse los pies antes de congelarse."
        ],
        # Capítulo 4: La fogata y el desastre
        [
            "El hombre trabajó con cuidado para hacer una fogata debajo de las ramas de un gran pino.",
            "Encendió un pedazo de corteza seca con un fósforo y cuidó una pequeña llama viva.",
            "El fuego creció con fuerza y el hombre se sintió a salvo del frío mortal.",
            "Pero ocurrió el desastre: las ramas del pino estaban cargadas de nieve acumulada durante semanas.",
            "Cada vez que él jalaba una ramita, el árbol se sacudía, hasta que un montón de nieve cayó sobre la fogata y la apagó por completo."
        ],
        # Capítulo 5: Los fósforos, la carrera y el descanso final
        [
            "El hombre sintió pánico cuando el frío se metió en su cuerpo y sus dedos se endurecieron como pedazos de madera.",
            "Frotó todo el paquete de setenta fósforos contra su pierna, pero sus manos sin fuerza los dejaron caer a la nieve.",
            "Desesperado, corrió por el sendero intentando entrar en calor, pero sus piernas congeladas fallaron y cayó al suelo.",
            "Una agradable sensación de calor lo envolvió, y se sentó junto a un pino, quedándose en un sueño tranquilo y eterno.",
            "El perro esperó sentado, olió la muerte en el cuerpo inmóvil y dio la vuelta para trotar hacia las fogatas del campamento."
        ]
    ]

    t3_anchors = [
        {"tag": "Tier 3 • Chapter 1", "icon": "🌲", "concept": "The Yukon Trail (Prose)", "alert": None},
        {"tag": "Tier 3 • Chapter 2", "icon": "🐺", "concept": "Extreme Cold & Animal Instinct", "alert": None},
        {"tag": "Tier 3 • Chapter 3", "icon": "🥾", "concept": "Hidden Springs & Wet Boots", "alert": "⚠️ Crisis: Wet feet in seventy-five below"},
        {"tag": "Tier 3 • Chapter 4", "icon": "🔥", "concept": "The Life Fire & The Avalanche", "alert": "⚠️ Catastrophe: Fire smothered by snow"},
        {"tag": "Tier 3 • Chapter 5", "icon": "📖", "concept": "The Final Run & Eternal Rest", "alert": None}
    ]

    t3_recaps = [
        # Recap Ch 1
        {
            "en": [
                "<strong>Setting:</strong> The Yukon forest at 9:00 AM in extreme cold.",
                "<strong>Atmosphere:</strong> Gray, sunless sky with pure unbroken snow.",
                "<strong>Action:</strong> A solitary traveler leaves the main trail into the pine woods."
            ],
            "es": [
                "<strong>Lugar:</strong> El bosque de Yukón a las 9:00 de la mañana con frío extremo.",
                "<strong>Ambiente:</strong> Cielo gris sin sol y nieve interminable.",
                "<strong>Acción:</strong> Un viajero solitario se desvía del camino hacia el bosque de pinos."
            ]
        },
        # Recap Ch 2
        {
            "en": [
                "<strong>The Real Temperature:</strong> 75 degrees below zero (spit freezes in mid-air).",
                "<strong>The Dog's Instinct:</strong> The wolf-dog knows it is too cold and dangerous to travel.",
                "<strong>Human Judgment:</strong> The man ignores the warning signs and continues walking."
            ],
            "es": [
                "<strong>La temperatura real:</strong> 75 grados bajo cero (la saliva se congela en el aire).",
                "<strong>El instinto del perro:</strong> El animal sabe que viajar con este frío es mortal.",
                "<strong>El juicio del hombre:</strong> El viajero ignora las señales y sigue caminando."
            ]
        },
        # Recap Ch 3
        {
            "en": [
                "<strong>The Water Traps:</strong> Warm springs flow beneath the snow without freezing.",
                "<strong>The Accident:</strong> The man falls through hidden ice, soaking his boots to his knees.",
                "<strong>Survival Rule:</strong> Wet feet require building an immediate fire to prevent losing toes."
            ],
            "es": [
                "<strong>Las trampas de agua:</strong> Manantiales corren bajo la nieve sin congelarse.",
                "<strong>El accidente:</strong> El hombre pisa nieve blanda y se empapa las botas hasta las rodillas.",
                "<strong>Regla de supervivencia:</strong> Pies mojados exigen encender fuego de inmediato para no congelarse."
            ]
        },
        # Recap Ch 4
        {
            "en": [
                "<strong>The First Fire:</strong> The man successfully starts a warm fire under a large pine.",
                "<strong>The Critical Mistake:</strong> Pulling twigs from the tree disturbs the heavy snow on the branches.",
                "<strong>The Tragedy:</strong> A small avalanche falls from the boughs and smothers the fire."
            ],
            "es": [
                "<strong>El primer fuego:</strong> El hombre logra encender una buena fogata bajo un pino grande.",
                "<strong>El grave error:</strong> Jalar ramas sacude la nieve acumulada en las partes altas del árbol.",
                "<strong>La tragedia:</strong> Una avalancha de nieve cae sobre la fogata y la apaga por completo."
            ]
        },
        # Recap Ch 5
        {
            "en": [
                "<strong>Frozen Hands:</strong> His fingers go completely numb; he burns his flesh lighting 70 matches at once.",
                "<strong>The Panic Run:</strong> He runs desperately to restore circulation, but his frozen legs give out.",
                "<strong>Peaceful Sleep:</strong> The man drifts into a painless final sleep; the dog survives and trots toward the camp."
            ],
            "es": [
                "<strong>Manos congeladas:</strong> Los dedos pierden sensibilidad; quema su piel encendiendo 70 fósforos a la vez.",
                "<strong>La carrera desesperada:</strong> Corre para recuperar calor, pero sus piernas congeladas colapsan.",
                "<strong>El descanso final:</strong> El hombre se duerme en paz; el perro sobrevive y busca el calor del campamento."
            ]
        }
    ]

    t3_blocks = [generate_sentence_block(i, "t3", t3_en[i], t3_es[i], t3_anchors[i], t3_recaps[i]) for i in range(len(t3_en))]

    # Assemble and compile template
    output_html = HTML_TEMPLATE.replace("__TIER_1_BLOCKS__", "\n".join(t1_blocks))
    output_html = output_html.replace("__TIER_2_BLOCKS__", "\n".join(t2_blocks))
    output_html = output_html.replace("__TIER_3_BLOCKS__", "\n".join(t3_blocks))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(output_html)

    print(f"✓ Complete Jack London narrative compiled successfully: {output_path}")

if __name__ == "__main__":
    build_master_reader()
