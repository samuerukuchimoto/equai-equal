import streamlit as st
import anthropic
import json
import random
import string

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EQUAI — Behavioral Capital Exchange",
    page_icon="⚖️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ── CSS — mirrors the HTML design: black/gold, IBM Plex Mono, Bebas Neue ─────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Serif+Display:ital@0;1&family=IBM+Plex+Mono:wght@300;400;500&family=Crimson+Pro:ital,wght@0,300;0,400;1,300&display=swap" rel="stylesheet">

<style>
  /* ── Root palette ── */
  :root {
    --black:    #080808;
    --white:    #F2EDE4;
    --gold:     #C9A84C;
    --gold-dim: #8B6E2E;
    --red:      #C0392B;
    --green:    #1A6B3C;
    --surface:  #111111;
    --border:   rgba(201,168,76,0.25);
  }

  /* ── Global overrides ── */
  html, body, [data-testid="stAppViewContainer"],
  [data-testid="stMain"], [data-testid="block-container"] {
    background-color: var(--black) !important;
    color: var(--white) !important;
    font-family: 'Crimson Pro', serif !important;
  }
  [data-testid="stSidebar"] { background: #0a0a0a !important; }
  section[data-testid="stMain"] > div { padding-top: 0 !important; }
  footer { visibility: hidden; }
  #MainMenu { visibility: hidden; }

  /* ── Typography helpers ── */
  .mono  { font-family: 'IBM Plex Mono', monospace; }
  .bebas { font-family: 'Bebas Neue', sans-serif; }
  .serif { font-family: 'DM Serif Display', serif; }

  /* ── Hero ── */
  .hero {
    padding: 4rem 0 3rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 3rem;
    position: relative;
  }
  .hero::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--gold), transparent);
  }
  .eyebrow {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.3em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 1rem;
  }
  .hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(4.5rem, 16vw, 10rem);
    line-height: 0.88;
    letter-spacing: -0.02em;
    color: var(--white);
    margin: 0;
  }
  .hero-title span { color: var(--gold); }
  .hero-sub {
    font-family: 'DM Serif Display', serif;
    font-style: italic;
    font-size: 1.15rem;
    color: rgba(242,237,228,0.55);
    margin-top: 1.5rem;
    line-height: 1.6;
    max-width: 520px;
  }
  .hero-axiom {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.65rem;
    color: var(--gold-dim);
    margin-top: 2rem;
    letter-spacing: 0.15em;
  }

  /* ── Section labels ── */
  .section-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.35em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 2rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
  }

  /* ── Asymmetry grid ── */
  .asym-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: var(--border);
    margin: 1.5rem 0 3rem;
  }
  .asym-cell {
    background: var(--black);
    padding: 1.8rem;
    transition: background 0.2s;
  }
  .asym-cell:hover { background: var(--surface); }
  .asym-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.55rem;
    letter-spacing: 0.25em;
    color: var(--gold-dim);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }
  .asym-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.8rem;
    color: var(--white);
    margin-bottom: 0.4rem;
  }
  .asym-desc {
    font-size: 0.9rem;
    color: rgba(242,237,228,0.5);
    line-height: 1.6;
  }
  .asym-bar {
    height: 2px;
    background: var(--gold);
    margin-top: 1rem;
    opacity: 0.6;
  }

  /* ── Mechanism stages ── */
  .stage {
    display: grid;
    grid-template-columns: 64px 1fr;
    gap: 1.5rem;
    padding: 1.5rem 0;
    border-top: 1px solid var(--border);
    align-items: start;
  }
  .stage-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3rem;
    color: var(--gold);
    opacity: 0.35;
    line-height: 1;
  }
  .stage-name {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.25em;
    color: var(--gold-dim);
    text-transform: uppercase;
    margin-bottom: 0.35rem;
  }
  .stage-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.2rem;
    color: var(--white);
    margin-bottom: 0.35rem;
  }
  .stage-desc {
    font-size: 0.9rem;
    color: rgba(242,237,228,0.5);
    line-height: 1.7;
  }

  /* ── Demo section ── */
  .demo-wrap {
    background: var(--surface);
    padding: 3rem;
    border: 1px solid var(--border);
    margin-bottom: 3rem;
  }
  .demo-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2rem, 6vw, 3.5rem);
    color: var(--white);
    margin-bottom: 0.25rem;
  }
  .demo-sub {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.6rem;
    color: var(--gold-dim);
    letter-spacing: 0.2em;
    margin-bottom: 2.5rem;
  }
  .input-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.25em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 0.6rem;
    display: block;
  }

  /* Streamlit multiselect / checkbox overrides */
  [data-baseweb="checkbox"] label span,
  [data-testid="stMultiSelect"] span {
    color: var(--white) !important;
    font-family: 'IBM Plex Mono', monospace !important;
  }
  [data-testid="stMultiSelect"] > div {
    background: transparent !important;
    border-color: var(--border) !important;
  }
  div[data-baseweb="tag"] {
    background-color: var(--gold) !important;
    color: var(--black) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.65rem !important;
    letter-spacing: 0.1em !important;
  }

  /* ── Result box ── */
  .result-box {
    border: 1px solid var(--border);
    margin-top: 2rem;
  }
  .result-header {
    background: var(--gold);
    color: var(--black);
    padding: 0.9rem 1.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
  .result-body { padding: 2rem; }
  .capital-statement {
    font-family: 'DM Serif Display', serif;
    font-size: 1.5rem;
    color: var(--gold);
    margin-bottom: 1rem;
    font-style: italic;
  }
  .insight-text {
    font-size: 1rem;
    line-height: 1.8;
    color: rgba(242,237,228,0.8);
    margin-bottom: 1.5rem;
  }
  .paths-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.58rem;
    letter-spacing: 0.25em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 1rem;
  }
  .path-cards {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1rem;
    margin-bottom: 1.5rem;
  }
  .path-card {
    border: 1px solid var(--border);
    padding: 1.5rem;
    transition: all 0.3s;
  }
  .path-card:hover { border-color: var(--gold); background: rgba(201,168,76,0.04); }
  .path-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.52rem;
    letter-spacing: 0.2em;
    color: var(--gold-dim);
    text-transform: uppercase;
    margin-bottom: 0.4rem;
  }
  .path-title {
    font-family: 'DM Serif Display', serif;
    font-size: 1.1rem;
    color: var(--white);
    margin-bottom: 0.3rem;
  }
  .path-income {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    color: var(--gold);
    margin-bottom: 0.5rem;
  }
  .path-meta {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.52rem;
    letter-spacing: 0.12em;
    color: var(--gold-dim);
    text-transform: uppercase;
    margin-bottom: 0.3rem;
  }
  .path-step {
    font-size: 0.88rem;
    color: rgba(242,237,228,0.55);
    line-height: 1.5;
  }
  .path-full {
    grid-column: 1 / -1;
  }
  .torah-anchor {
    padding: 1.5rem;
    border-left: 3px solid var(--gold);
    background: rgba(201,168,76,0.05);
    margin-bottom: 1rem;
  }
  .torah-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.52rem;
    letter-spacing: 0.22em;
    color: var(--gold);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
  }
  .torah-text {
    font-size: 0.95rem;
    color: rgba(242,237,228,0.75);
    line-height: 1.7;
    font-style: italic;
  }
  .barrier-reframe {
    padding: 1.2rem;
    background: rgba(26,107,60,0.1);
    border-left: 3px solid var(--green);
    margin-top: 0.5rem;
  }
  .barrier-label {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.52rem;
    letter-spacing: 0.2em;
    color: #2ecc71;
    text-transform: uppercase;
    margin-bottom: 0.4rem;
  }
  .barrier-text {
    font-size: 0.95rem;
    color: rgba(242,237,228,0.7);
    font-style: italic;
    line-height: 1.6;
  }

  /* ── Roadmap ── */
  .phase {
    border-top: 1px solid var(--border);
    padding: 2rem 0;
    display: grid;
    grid-template-columns: 180px 1fr;
    gap: 2rem;
  }
  .phase-num  { font-family:'IBM Plex Mono',monospace;font-size:0.62rem;letter-spacing:0.2em;color:var(--gold);text-transform:uppercase; }
  .phase-time { font-family:'IBM Plex Mono',monospace;font-size:0.62rem;color:rgba(242,237,228,0.4);margin-top:0.25rem; }
  .phase-cost { font-family:'Bebas Neue',sans-serif;font-size:1.4rem;color:var(--gold-dim);margin-top:0.5rem; }
  .phase-title { font-family:'DM Serif Display',serif;font-size:1.3rem;color:var(--white);margin-bottom:0.75rem; }
  .phase-tasks { list-style:none;padding:0;margin:0 0 0.75rem; }
  .phase-tasks li {
    font-size:0.9rem;color:rgba(242,237,228,0.55);line-height:1.6;padding:0.2rem 0;
    padding-left:1rem;position:relative;
  }
  .phase-tasks li::before { content:'—';position:absolute;left:0;color:var(--gold-dim); }
  .phase-outcome { font-family:'IBM Plex Mono',monospace;font-size:0.62rem;color:var(--gold-dim);letter-spacing:0.1em; }

  /* ── Torah grid ── */
  .torah-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 1px;
    background: var(--border);
    margin: 1.5rem 0 3rem;
  }
  .torah-cell { background:var(--black);padding:2rem;transition:background 0.2s; }
  .torah-cell:hover { background:var(--surface); }
  .torah-hebrew { font-size:2rem;color:var(--gold);margin-bottom:0.5rem;direction:rtl; }
  .torah-concept { font-family:'IBM Plex Mono',monospace;font-size:0.62rem;letter-spacing:0.15em;color:var(--gold-dim);text-transform:uppercase;margin-bottom:0.75rem; }
  .torah-app { font-size:0.9rem;color:rgba(242,237,228,0.55);line-height:1.7; }

  /* ── Footer ── */
  .equai-footer {
    border-top: 1px solid var(--border);
    padding: 3rem 0 2rem;
    margin-top: 3rem;
    text-align: center;
  }
  .footer-logo { font-family:'Bebas Neue',sans-serif;font-size:3rem;letter-spacing:0.3em;color:var(--gold); }
  .footer-meta { font-family:'IBM Plex Mono',monospace;font-size:0.58rem;letter-spacing:0.25em;color:var(--gold-dim);text-transform:uppercase;margin-top:0.75rem;line-height:2; }

  /* ── Streamlit button overrides ── */
  div[data-testid="stButton"] > button {
    background: var(--gold) !important;
    border: none !important;
    color: #080808 !important;
    font-family: 'Bebas Neue', sans-serif !important;
    font-size: 1.2rem !important;
    letter-spacing: 0.15em !important;
    padding: 0.9rem 2.5rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s !important;
    border-radius: 0 !important;
  }
  div[data-testid="stButton"] > button:hover {
    background: var(--white) !important;
    transform: translateY(-2px) !important;
  }
  div[data-testid="stButton"] > button:disabled {
    opacity: 0.4 !important;
    cursor: not-allowed !important;
    transform: none !important;
  }

  /* ── Multiselect pill colors ── */
  div[data-baseweb="select"] * { background-color: transparent !important; }
  .stMultiSelect [data-baseweb="tag"] { background-color: rgba(201,168,76,0.2) !important; border: 1px solid var(--gold) !important; }
  .stMultiSelect [data-baseweb="tag"] span { color: var(--gold) !important; }
  .stMultiSelect [data-testid="stMarkdownContainer"] p { color: var(--gold) !important; font-size: 0.62rem !important; font-family:'IBM Plex Mono',monospace !important; letter-spacing:0.15em !important; text-transform:uppercase !important; }

  /* Selectbox / dropdown */
  [data-testid="stSelectbox"] label, [data-testid="stMultiSelect"] label {
    color: var(--gold) !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.6rem !important;
    letter-spacing: 0.25em !important;
    text-transform: uppercase !important;
  }

  /* Spinner */
  [data-testid="stSpinner"] p { color: var(--gold-dim) !important; font-family:'IBM Plex Mono',monospace !important; font-size:0.7rem !important; letter-spacing:0.15em !important; }

  /* Divider */
  hr { border-color: var(--border) !important; }

  /* Big statement */
  .big-statement {
    font-family: 'DM Serif Display', serif;
    font-size: clamp(1.5rem, 3.5vw, 2.4rem);
    line-height: 1.3;
    max-width: 700px;
    margin-bottom: 2.5rem;
  }
  .big-statement em { color: var(--gold); font-style: italic; }

  @media (max-width: 640px) {
    .asym-grid, .path-cards, .torah-grid, .phase { grid-template-columns: 1fr !important; }
    .demo-wrap { padding: 1.5rem; }
    .path-full { grid-column: auto; }
  }
</style>
""", unsafe_allow_html=True)


# ── Helpers ──────────────────────────────────────────────────────────────────
def session_id():
    return "SESSION " + "".join(random.choices(string.ascii_uppercase + string.digits, k=8))


SKILL_LABELS = {
    "Persuasion & Influence":    "Persuasion & Influence",
    "Pattern Recognition":       "Pattern Recognition",
    "Deep Empathy":              "Deep Empathy",
    "Strategic Thinking":        "Strategic Thinking",
    "Storytelling":              "Storytelling",
    "Negotiation":               "Negotiation",
    "Community Leadership":      "Community Leadership",
    "Data & Analysis":           "Data & Analysis",
}

BARRIER_LABELS = {
    "💸 No starting capital":       "No starting capital",
    "🕸️ No professional network":   "No professional network",
    "📄 No formal credentials":     "No formal credentials",
    "🗣️ Language barrier":          "Language barrier",
    "📍 Remote / rural location":   "Remote/rural location",
    "⚖️ Discrimination / bias":     "Discrimination/bias",
    "⏳ Need income this week":     "Need income this week",
    "🪞 Self-doubt":                "Self-doubt",
}


def build_prompt(skills: list[str], barriers: list[str]) -> str:
    skill_str   = ", ".join(skills)  if skills   else "not specified"
    barrier_str = ", ".join(barriers) if barriers else "None specified"
    return f"""You are EQUAI — a behavioral capital exchange that helps people convert their natural abilities into legitimate income, regardless of their background, credentials, or location.

A person has identified these natural abilities: {skill_str}
Their real barriers are: {barrier_str}

Generate a behavioral capital map in JSON format with this exact structure:
{{
  "capital_statement": "One powerful sentence (max 20 words) that names their capital in market language",
  "insight": "One paragraph (3-4 sentences) explaining why their specific combination of skills is valuable and underrecognized in the current market",
  "paths": [
    {{
      "title": "Path name",
      "category": "Category (e.g. Freelance, Consulting, Digital, Community)",
      "monthly_income_eur": "Realistic range e.g. €800–2,500",
      "time_to_first_income": "e.g. 3–7 days",
      "first_step": "The single most concrete first action they can take today, free, no credentials needed"
    }},
    {{
      "title": "Path name",
      "category": "Category",
      "monthly_income_eur": "Range",
      "time_to_first_income": "Timeline",
      "first_step": "Concrete first action"
    }},
    {{
      "title": "Path name",
      "category": "Category",
      "monthly_income_eur": "Range",
      "time_to_first_income": "Timeline",
      "first_step": "Concrete first action"
    }}
  ],
  "torah_anchor": "One Torah principle (with Hebrew term) that applies to this person's situation and why their capital matters beyond income",
  "barrier_reframe": "One sentence that reframes their biggest barrier as a competitive advantage"
}}

Be specific, honest, and practical. No generic advice. Address their actual barriers directly. Respond ONLY with valid JSON, no markdown, no preamble."""


def call_claude(prompt: str) -> dict:
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1100,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text.strip()
    # Strip accidental markdown fences
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw.strip())


def render_result(result: dict):
    sid = session_id()
    st.markdown(f"""
    <div class="result-box">
      <div class="result-header">
        <span>// CAPITAL MAP GENERATED</span>
        <span>// {sid}</span>
      </div>
      <div class="result-body">
        <div class="capital-statement">"{result['capital_statement']}"</div>
        <div class="insight-text">{result['insight']}</div>
        <div class="paths-label">// YOUR THREE INCOME PATHS</div>
        <div class="path-cards">
    """, unsafe_allow_html=True)

    for i, path in enumerate(result["paths"]):
        extra_class = "path-full" if i == 2 else ""
        st.markdown(f"""
          <div class="path-card {extra_class}">
            <div class="path-label">PATH {str(i+1).zfill(2)} · {path['category']}</div>
            <div class="path-title">{path['title']}</div>
            <div class="path-income">{path['monthly_income_eur']}</div>
            <div class="path-meta">FIRST INCOME IN:</div>
            <div class="path-step">{path['time_to_first_income']}</div>
            <div class="path-meta" style="margin-top:0.75rem;">FIRST STEP TODAY:</div>
            <div class="path-step">{path['first_step']}</div>
          </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
        </div>
        <div class="torah-anchor">
          <div class="torah-label">// TORAH ANCHOR</div>
          <div class="torah-text">{result['torah_anchor']}</div>
        </div>
        <div class="barrier-reframe">
          <div class="barrier-label">// BARRIER REFRAMED AS ADVANTAGE</div>
          <div class="barrier-text">{result['barrier_reframe']}</div>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# RENDER
# ═══════════════════════════════════════════════════════════════════════════════

# ── HERO ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="eyebrow">// BEHAVIORAL CAPITAL EXCHANGE · POWERED BY CLAUDE AI</div>
  <div class="hero-title">EQ<span>UAI</span></div>
  <div class="hero-sub">
    The market already values what you do naturally.<br>
    It just never told you what to call it — or what it's worth.
  </div>
  <div class="hero-axiom">
    POVERTY IS NOT A SKILL DEFICIT. IT IS AN INFORMATION ASYMMETRY.
  </div>
</div>
""", unsafe_allow_html=True)


# ── 01 — FOUR ASYMMETRIES ────────────────────────────────────────────────────
st.markdown('<div class="section-label">// 01 — THE FOUR ASYMMETRIES THAT LOCK POVERTY IN PLACE</div>', unsafe_allow_html=True)
st.markdown("""
<div class="asym-grid">
  <div class="asym-cell">
    <div class="asym-num">Asymmetry 01</div>
    <div class="asym-title">INFORMATION</div>
    <div class="asym-desc">The powerful know what opportunities exist. The poor don't know what they don't know. EQUAI maps every legitimate income path to every behavioral profile.</div>
    <div class="asym-bar" style="width:85%"></div>
  </div>
  <div class="asym-cell">
    <div class="asym-num">Asymmetry 02</div>
    <div class="asym-title">ACCESS</div>
    <div class="asym-desc">Premium tools, networks, and platforms require capital to enter. EQUAI costs zero. Zero registration. Zero subscription. Zero friction.</div>
    <div class="asym-bar" style="width:70%"></div>
  </div>
  <div class="asym-cell">
    <div class="asym-num">Asymmetry 03</div>
    <div class="asym-title">NETWORK</div>
    <div class="asym-desc">Who you know determines what you earn. EQUAI builds network capital from behavioral reputation — not from who your father is.</div>
    <div class="asym-bar" style="width:90%"></div>
  </div>
  <div class="asym-cell">
    <div class="asym-num">Asymmetry 04</div>
    <div class="asym-title">TIME</div>
    <div class="asym-desc">The poor cannot wait. They need income this week, not in six months. EQUAI matches skills to income paths with the fastest time-to-first-euro.</div>
    <div class="asym-bar" style="width:75%"></div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── 02 — MECHANISM ───────────────────────────────────────────────────────────
st.markdown('<div class="section-label">// 02 — HOW EQUAI REDISTRIBUTES POWER</div>', unsafe_allow_html=True)
st.markdown("""
<div class="big-statement">
  Every human has <em>behavioral capital</em> — persuasion, pattern recognition, empathy, social intelligence.
  The system never told them it was worth money. <em>We tell them.</em>
</div>
<div class="stage">
  <div class="stage-num">00</div>
  <div>
    <div class="stage-name">Entry</div>
    <div class="stage-title">Anonymous. No judgment. No documents required.</div>
    <div class="stage-desc">No CV. No diploma. No address. No bank account needed to begin. A person in rural Nigeria and a person in suburban Paris enter the same door.</div>
  </div>
</div>
<div class="stage">
  <div class="stage-num">01</div>
  <div>
    <div class="stage-name">Behavioral Mapping</div>
    <div class="stage-title">What can you actually do — in the language of the market?</div>
    <div class="stage-desc">EQUAI translates lived experience into market-readable skills. "I convinced my community to do X" = persuasion architecture. "I tracked patterns in my village" = data intelligence. The vocabulary changes. The human doesn't.</div>
  </div>
</div>
<div class="stage">
  <div class="stage-num">02</div>
  <div>
    <div class="stage-name">Barrier Identification</div>
    <div class="stage-title">What is actually stopping you — not what you think is stopping you.</div>
    <div class="stage-desc">AI distinguishes between real barriers (no internet, safety risk, language) and perceived barriers (imposter syndrome, lack of credentials, geographic assumptions). Different interventions for each.</div>
  </div>
</div>
<div class="stage">
  <div class="stage-num">03</div>
  <div>
    <div class="stage-name">Path Matching</div>
    <div class="stage-title">Three income paths, ranked by time-to-first-income.</div>
    <div class="stage-desc">Not generic career advice. Specific: this platform, this type of client, this first offer, this price, this week. The Matthew Effect in reverse — giving the poor what the rich pay consultants for.</div>
  </div>
</div>
<div class="stage">
  <div class="stage-num">04</div>
  <div>
    <div class="stage-name">Teshuvah — Return &amp; Track</div>
    <div class="stage-title">Did it work? What changed? What's next?</div>
    <div class="stage-desc">7-day follow-up. 30-day check. Not to collect data. To close the loop. Maimonides' highest Tzedakah: making someone self-sufficient. EQUAI measures this — not engagement metrics.</div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ── 03 — LIVE DEMO ───────────────────────────────────────────────────────────
st.markdown('<div class="demo-wrap">', unsafe_allow_html=True)
st.markdown("""
<div class="section-label">// 03 — LIVE DEMO · BEHAVIORAL CAPITAL EXCHANGE</div>
<div class="demo-title">MAP YOUR CAPITAL</div>
<div class="demo-sub">// ANONYMOUS · NO REGISTRATION · POWERED BY CLAUDE AI</div>
""", unsafe_allow_html=True)

# Skill multiselect
selected_skills = st.multiselect(
    "YOUR STRONGEST NATURAL ABILITIES",
    options=list(SKILL_LABELS.keys()),
    placeholder="Select one or more abilities...",
    help="Choose the skills that feel most natural to you — not what you studied, what you ARE.",
)

st.markdown("<br>", unsafe_allow_html=True)

# Barrier multiselect
selected_barriers = st.multiselect(
    "YOUR REAL BARRIERS RIGHT NOW",
    options=list(BARRIER_LABELS.keys()),
    placeholder="Select all that apply (optional)...",
    help="Be honest — EQUAI routes around barriers, not away from them.",
)

st.markdown("<br>", unsafe_allow_html=True)

# Generate button
can_generate = len(selected_skills) > 0
if can_generate:
    if st.button("GENERATE MY CAPITAL MAP", use_container_width=True):
        skills_clean   = [SKILL_LABELS[s]   for s in selected_skills]
        barriers_clean = [BARRIER_LABELS[b] for b in selected_barriers] if selected_barriers else []

        with st.spinner("// EQUAI IS MAPPING YOUR BEHAVIORAL CAPITAL..."):
            try:
                result = call_claude(build_prompt(skills_clean, barriers_clean))
                st.session_state["last_result"] = result
            except Exception as e:
                st.error(f"API error: {e}. Check your ANTHROPIC_API_KEY in secrets.")
                st.session_state["last_result"] = None
else:
    st.button("GENERATE MY CAPITAL MAP", disabled=True, use_container_width=True)
    st.markdown(
        '<p style="font-family:\'IBM Plex Mono\',monospace;font-size:0.6rem;color:var(--gold-dim);letter-spacing:0.1em;margin-top:0.5rem;">'
        '// SELECT AT LEAST ONE ABILITY TO ACTIVATE</p>',
        unsafe_allow_html=True
    )

# Show result if available
if st.session_state.get("last_result"):
    render_result(st.session_state["last_result"])

st.markdown('</div>', unsafe_allow_html=True)


# ── 04 — ROADMAP ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">// 04 — EXECUTION ROADMAP</div>', unsafe_allow_html=True)
st.markdown("""
<div style="font-family:'Bebas Neue',sans-serif;font-size:clamp(2.5rem,8vw,5rem);line-height:0.9;margin-bottom:3rem;">
  FROM<br><span style="color:var(--gold)">ZERO</span><br>TO SCALE
</div>

<div class="phase">
  <div>
    <div class="phase-num">PHASE 01</div>
    <div class="phase-time">Week 1–2</div>
    <div class="phase-cost">€0 BUDGET</div>
  </div>
  <div>
    <div class="phase-title">Ship the MVP</div>
    <ul class="phase-tasks">
      <li>Deploy on Streamlit Community Cloud (free, instant)</li>
      <li>Connect Anthropic API key via Streamlit secrets — secure</li>
      <li>Test with 20 real users from diverse backgrounds</li>
      <li>Collect: skill input → path output → did it match reality?</li>
      <li>Publish on LinkedIn, tag impact investors + French CTOs</li>
    </ul>
    <div class="phase-outcome">// Outcome: 20 real behavioral capital maps generated. First validation data.</div>
  </div>
</div>

<div class="phase">
  <div>
    <div class="phase-num">PHASE 02</div>
    <div class="phase-time">Month 1</div>
    <div class="phase-cost">€0–500</div>
  </div>
  <div>
    <div class="phase-title">Prove the Redistribution</div>
    <ul class="phase-tasks">
      <li>Track: did users earn their first income using EQUAI paths?</li>
      <li>Add Supabase (free tier) for session tracking</li>
      <li>Add 7-day follow-up email via Resend (free tier)</li>
      <li>Partner with 1 NGO or social enterprise for user pipeline</li>
      <li>Apply to BPI France Innovation Grant (up to €30k, no equity)</li>
    </ul>
    <div class="phase-outcome">// Outcome: First users reporting income generated. This is your investor proof point.</div>
  </div>
</div>

<div class="phase">
  <div>
    <div class="phase-num">PHASE 03</div>
    <div class="phase-time">Month 2–3</div>
    <div class="phase-cost">€30,000</div>
  </div>
  <div>
    <div class="phase-title">Build with Your Israeli Expert</div>
    <ul class="phase-tasks">
      <li>Mobile-first PWA (works without app store)</li>
      <li>Offline mode — works with poor connectivity</li>
      <li>Multi-language: French, English, Arabic, Hebrew</li>
      <li>Behavioral reputation score — portable, user-owned</li>
      <li>EU AI Act compliance audit trail (SHAP + logging)</li>
    </ul>
    <div class="phase-outcome">// Outcome: Production-ready platform. Fundable at €500k–€1M seed.</div>
  </div>
</div>

<div class="phase">
  <div>
    <div class="phase-num">PHASE 04</div>
    <div class="phase-time">Month 4–6</div>
    <div class="phase-cost">€500k seed</div>
  </div>
  <div>
    <div class="phase-title">Scale the Redistribution</div>
    <ul class="phase-tasks">
      <li>Target: Omidyar Network, Ashoka, Kima Ventures</li>
      <li>Government contracts: French Ministry of Labour, EU Commission</li>
      <li>B2B: sell behavioral intelligence to HR platforms (€/profile)</li>
      <li>B2G: refugee integration programs (UNHCR partnership)</li>
      <li>Expand to Canada, Israel, Germany, Ireland</li>
    </ul>
    <div class="phase-outcome">// Outcome: 10,000 users. First revenue. Series A ready.</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── 05 — TORAH ARCHITECTURE ──────────────────────────────────────────────────
st.markdown('<br><div class="section-label">// 05 — TORAH ARCHITECTURE · WHY THIS WORKS WHERE OTHERS FAILED</div>', unsafe_allow_html=True)
st.markdown("""
<div class="torah-grid">
  <div class="torah-cell">
    <div class="torah-hebrew">צֶדֶק</div>
    <div class="torah-concept">Tzedek — Justice, not charity</div>
    <div class="torah-app">EQUAI doesn't give fish. It doesn't teach fishing. It reveals that the person already knows how to fish — and connects them to the market that pays for it.</div>
  </div>
  <div class="torah-cell">
    <div class="torah-hebrew">שְׁמִיטָה</div>
    <div class="torah-concept">Shmita — Built-in redistribution</div>
    <div class="torah-app">Every 7 years, Torah commands debt cancellation. EQUAI's architecture resets barriers by design — free access, no lock-in, user-owned data. Shmita as code.</div>
  </div>
  <div class="torah-cell">
    <div class="torah-hebrew">צֶלֶם אֱלֹהִים</div>
    <div class="torah-concept">Tzelem Elohim — Divine image</div>
    <div class="torah-app">Every human carries intelligence by design. EQUAI's premise: the problem is never the person. The problem is always the system that failed to recognize their capital.</div>
  </div>
  <div class="torah-cell">
    <div class="torah-hebrew">תִּקּוּן עוֹלָם</div>
    <div class="torah-concept">Tikkun Olam — Repair by infrastructure</div>
    <div class="torah-app">The internet repaired nothing because it had no redistribution mechanism. EQUAI is Tikkun Olam as technical architecture — repair built into the product, not the marketing.</div>
  </div>
</div>
""", unsafe_allow_html=True)


# ── FOOTER ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="equai-footer">
  <div class="footer-logo">EQUAI</div>
  <div class="footer-meta">
    BEHAVIORAL CAPITAL EXCHANGE<br>
    BUILT BY SAMUEL LOUISSAINT<br>
    TIKKUN OLAM AS INFRASTRUCTURE
  </div>
</div>
""", unsafe_allow_html=True)
