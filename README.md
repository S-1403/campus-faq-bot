# 🎓 Campus FAQ Assistant

An AI-powered conversational chatbot that answers prospective and current students'
questions about university admissions, courses, fees, and campus life. Built as a
multi-turn, context-aware assistant with a clean Streamlit front-end and support for
both OpenAI and Anthropic (Claude) APIs.

**Live demo:** _add your deployed URL here after following the deployment steps below_

---

## Problem Statement

Build a conversational chatbot that can answer questions on a specific topic — in this
case, university admissions and campus FAQs — using an LLM API, with a simple front-end
interface that demonstrates multi-turn contextual conversation, not just single-shot Q&A.

## Core Features

- 💬 **Multi-turn conversation** — the bot remembers earlier turns in the session and
  responds with that context (e.g., it won't ask which program you're applying to twice).
- 🎯 **Topic-focused system prompt** — scoped strictly to admissions, courses, fees,
  scholarships, and campus life, with polite redirection for off-topic asks.
- 🗂️ **Conversation history management** — history is stored in session state and
  automatically trimmed to the last N turns to keep API calls efficient.
- 🗑️ **Clear / Reset functionality** — clear just the chat, or fully reset the session
  (including the API key).
- ⌨️ **Typing indicator** — a streaming-style "typing..." reveal while the model
  generates its response.
- 🔌 **Dual-provider support** — switch between OpenAI and Anthropic models from the
  sidebar without touching code.

## Tools & Technologies

| Layer        | Choice                              |
|--------------|--------------------------------------|
| Language     | Python 3.10+                        |
| Front-end    | Streamlit                           |
| LLM APIs     | OpenAI API, Anthropic (Claude) API  |
| State        | Streamlit `session_state` (in-memory)|

## Project Structure

```
campus-faq-bot/
├── app.py                  # Streamlit UI + chat orchestration
├── llm_client.py           # Provider-agnostic LLM calling logic (OpenAI / Anthropic)
├── system_prompt.py        # Topic-focused system prompt + reference FAQ data
├── requirements.txt        # Python dependencies
├── .streamlit/config.toml  # Theme & server config
└── README.md
```

> ⚠️ **Before deploying for real use:** open `system_prompt.py` and replace every
> bracketed placeholder (`[University Name]`, fee figures, dates, contact info, etc.)
> with your actual institution's real data. The bot is instructed to only answer from
> what's written there, so accuracy depends entirely on filling this in correctly.

---

## Run Locally

```bash
git clone <your-repo-url>
cd campus-faq-bot
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints (usually `http://localhost:8501`), pick a
provider in the sidebar, paste in your API key, and start chatting.

> **Note:** Bring your own API key — get one from
> [console.anthropic.com](https://console.anthropic.com) (Claude) or
> [platform.openai.com](https://platform.openai.com) (OpenAI). The key is only kept in
> your browser session and is never logged or stored server-side.

---

## Deploy for Free (Streamlit Community Cloud)

This gets you a public, shareable URL in a few minutes.

1. **Push this project to a public GitHub repo.**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Campus FAQ Assistant"
   git branch -M main
   git remote add origin https://github.com/<your-username>/campus-faq-bot.git
   git push -u origin main
   ```

2. **Go to [share.streamlit.io](https://share.streamlit.io)** and sign in with GitHub.

3. Click **"New app"**, select your repo, branch (`main`), and set the main file path
   to `app.py`.

4. Click **Deploy**. In a minute or two you'll get a public URL like:
   `https://your-app-name.streamlit.app`

5. Share that link — anyone can open it, paste in their own API key, and chat with the
   bot. No server secrets needed since each user supplies their own key client-side.

### Optional: Pre-fill a key via Streamlit Secrets (for your own demo only)

If you want the deployed app to work without visitors entering a key (e.g., for a demo
video or recruiter walkthrough), you can store **your own** key as a Streamlit secret
instead of exposing it in the repo:

1. In the Streamlit Cloud dashboard, go to your app → **Settings → Secrets**.
2. Add:
   ```toml
   ANTHROPIC_API_KEY = "sk-ant-..."
   ```
3. Modify `app.py` to fall back to `st.secrets` if no key is typed in (see comment in
   `app.py` near the API key input for where to add this).

⚠️ Never commit real API keys to GitHub — `.streamlit/secrets.toml` is already in
`.gitignore` for this reason.

---

## How This Demonstrates Multi-Turn Contextual Conversation

Try this sequence after deploying:

1. "I'm interested in applying for B.Tech Computer Science. What's the eligibility?"
2. "What documents do I need to submit?"
3. "And what about the fees for that program?"

Notice the bot never re-asks which program you're asking about — it carries that
context across turns, which is the core technical demonstration this project is built
to showcase.

---

## Possible Extensions

- Fill in `system_prompt.py` with your actual university's real admissions data
- Swap `system_prompt.py` to retarget the bot entirely (e.g., placement prep, product support)
- Add persistent storage (e.g., a database) so history survives page reloads
- Add streaming token-by-token responses using each provider's streaming API
- Add a feedback/rating widget per response for evaluation data
- Connect to a real FAQ database or PDF (admissions brochure) instead of inline text
