# EQUAI — Behavioral Capital Exchange

> *Poverty is not a skill deficit. It is an information asymmetry.*

EQUAI maps natural human abilities to legitimate income paths — free, anonymous, no credentials required. Powered by Claude AI.

## Stack

| Layer | Tool |
|---|---|
| Frontend + Backend | Streamlit |
| AI | Anthropic Claude (claude-sonnet-4) |
| Secrets | Streamlit secrets (never in code) |
| Hosting | Streamlit Community Cloud (free) |

---

## Run locally

```bash
# 1. Clone
git clone https://github.com/samuerukuchimoto/equai
cd equai

# 2. Install
pip install -r requirements.txt

# 3. Add your API key
mkdir -p .streamlit
echo 'ANTHROPIC_API_KEY = "sk-ant-YOUR_KEY_HERE"' > .streamlit/secrets.toml

# 4. Run
streamlit run app.py
```

---

## Deploy to Streamlit Cloud (free, 5 minutes)

1. Push this repo to GitHub (make sure `.streamlit/secrets.toml` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Select your repo → `app.py`
4. **Settings → Secrets** — paste:
   ```
   ANTHROPIC_API_KEY = "sk-ant-YOUR_KEY_HERE"
   ```
5. Deploy ✓

---

## Architecture

```
User selects skills + barriers
        ↓
Streamlit (Python backend)
        ↓
Anthropic API — claude-sonnet-4
(API key stored securely in Streamlit secrets)
        ↓
JSON: capital_statement, insight, 3 income paths,
      torah_anchor, barrier_reframe
        ↓
Rendered in EQUAI's black/gold design
```

---

## Files

```
equai/
├── app.py                  # The entire app
├── requirements.txt        # streamlit + anthropic only
├── .gitignore              # secrets excluded
├── .streamlit/
│   └── secrets.toml        # YOUR API KEY — not committed
└── README.md
```

---

Built by Samuel Louissaint · Tikkun Olam as Infrastructure
