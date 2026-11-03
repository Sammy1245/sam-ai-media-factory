# SAM AI MEDIA FACTORY — Phase 2

A Streamlit content-planning dashboard with free template-based content packs and optional AI-generated scripts using an OpenAI API key.

## Features
- Dashboard and project targets
- Template-based idea angles (not live trend research)
- Script Studio with hook, script, caption, hashtags and scene list
- Optional OpenAI API script generation
- Downloadable content packs and library backups
- Production planner, publishing checklist and analytics placeholders

## Deploy
Upload `app.py`, `requirements.txt`, and `README.md` to the root of your existing GitHub repository, replacing the previous files. Streamlit Community Cloud automatically redeploys changes to the selected branch.

## API mode
OpenAI API billing is separate from ChatGPT Plus. For a persistent key, set `OPENAI_API_KEY` in Streamlit Community Cloud app settings → Secrets (do not put keys in GitHub). Example:

```toml
OPENAI_API_KEY = "your-key-here"
```

Alternatively enter a key temporarily in the password field. Do not share keys or commit them.

## Limitations
This app does not generate finished videos, auto-post to social networks, or pull real-time trend/analytics data. Cloud-local JSON storage can reset; export backups. Templates are not AI generation and must be reviewed and fact-checked.
