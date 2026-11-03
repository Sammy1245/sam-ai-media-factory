import json
import random
from datetime import datetime
from pathlib import Path

import streamlit as st

st.set_page_config(page_title="SAM AI MEDIA FACTORY", page_icon="🎬", layout="wide")
st.title("🎬 SAM AI MEDIA FACTORY")
st.caption("Phase 2 — ideas, scripts, and production briefs")

STORE = Path("content.json")

def read_items():
    try:
        data = json.loads(STORE.read_text(encoding="utf-8"))
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []

def save_items(data):
    try:
        STORE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
        return True
    except OSError:
        return False

def clean_hashtags(topic):
    terms = ["".join(c for c in word if c.isalnum()) for word in topic.split()]
    terms = [x for x in terms if x][:3]
    return " ".join("#" + x for x in terms) + " #Shorts #LearnOnTikTok #ContentCreator"

def template_content(topic, audience, tone, duration, platform):
    topic = topic.strip()
    audience = audience.strip() or "curious viewers"
    return {
        "title": f"What you should know about {topic}",
        "hook": f"If you're interested in {topic}, here's a simple way to start.",
        "script": (
            f"[0–5 seconds] If you're interested in {topic}, this is for you.\n\n"
            f"[Main section] For {audience}, a useful first step is to define exactly what you want to learn about {topic}. "
            "Break it into three questions: What is it? Why does it matter? What can I do next? "
            "Research each answer using reliable sources, then illustrate the most useful example.\n\n"
            f"[Closing] Save this guide and tell us what part of {topic} you want covered next."
        ),
        "caption": f"A beginner-friendly introduction to {topic}. What would you add?",
        "hashtags": clean_hashtags(topic),
        "scenes": [
            "Scene 1: Bold on-screen hook and an illustrative visual",
            "Scene 2: Show the main concept with a simple example",
            "Scene 3: Display the three research questions as text overlays",
            "Scene 4: Closing CTA and branded end card",
        ],
        "platform": platform,
        "duration": duration,
        "tone": tone,
        "method": "Free template (not AI-generated)",
    }

def ai_content(topic, audience, tone, duration, platform, key, model):
    import requests
    instructions = (
        "You are a professional short-form content strategist. Return ONLY a JSON object with keys "
        "title, hook, script, caption, hashtags, scenes. scenes must be an array of 4-7 concise scene directions. "
        "Write an original engaging script with factual caution; do not invent statistics, citations or news. "
        "If a factual claim needs verification, explicitly mark it for fact-checking. "
        "No markdown fences."
    )
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": instructions},
            {"role": "user", "content": f"Topic: {topic}\nAudience: {audience}\nTone: {tone}\nDuration: {duration}\nPlatform: {platform}"},
        ],
        "temperature": 0.7,
    }
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        json=payload,
        timeout=45,
    )
    if response.status_code != 200:
        raise RuntimeError(f"AI request failed (HTTP {response.status_code}). Check the API key, model, and API billing/quota.")
    raw = response.json()["choices"][0]["message"]["content"].strip()
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
    result = json.loads(raw)
    for field in ["title", "hook", "script", "caption", "hashtags", "scenes"]:
        if field not in result:
            raise ValueError("The AI response was missing a required field. Please try again.")
    if not isinstance(result["scenes"], list):
        raise ValueError("The AI response had an invalid scene list. Please try again.")
    result.update({"platform": platform, "duration": duration, "tone": tone, "method": f"AI ({model})"})
    return result

items = read_items()
page = st.sidebar.radio("Modules", ["Dashboard", "Research & Ideas", "Script Studio", "Production Planner", "Publishing", "Analytics"])
st.sidebar.divider()
st.sidebar.caption("Free template mode works without API keys. AI mode needs a separately billed API key.")

if page == "Dashboard":
    st.subheader("Factory overview")
    a, b, c = st.columns(3)
    a.metric("Saved projects", len(items))
    b.metric("Daily target", "50 videos")
    c.metric("Account target", "90")
    st.info("Targets are goals, not live production figures. Video rendering and social publishing are not connected.")
    st.write("Research → Script → Production → Review → Publishing → Analytics")
    st.markdown("**New in Phase 2:** Generate structured script packs, review scene plans, and download content for safekeeping.")

elif page == "Research & Ideas":
    st.subheader("Research & Ideas")
    niche = st.text_input("Your niche", placeholder="e.g. personal finance, travel, technology")
    audience = st.text_input("Target audience", placeholder="e.g. first-time entrepreneurs")
    if st.button("Suggest idea angles"):
        if niche.strip():
            st.markdown("### Suggested content angles")
            for angle in [
                f"3 beginner mistakes to avoid with {niche}",
                f"A step-by-step introduction to {niche}",
                f"Common myths about {niche} worth fact-checking",
                f"Questions {audience or 'beginners'} ask about {niche}",
                f"How to compare different approaches to {niche}",
            ]:
                st.write("•", angle)
            st.caption("These are template-based ideas, not live trending-topic research.")
        else:
            st.warning("Enter a niche first.")

elif page == "Script Studio":
    st.subheader("Script Studio")
    topic = st.text_input("Video topic", placeholder="e.g. 5 ways to improve your study routine")
    audience = st.text_input("Audience", value="Beginners")
    x, y, z = st.columns(3)
    tone = x.selectbox("Tone", ["Friendly", "Professional", "Energetic", "Storytelling", "Educational"])
    duration = y.selectbox("Target duration", ["30 seconds", "60 seconds", "90 seconds"])
    platform = z.selectbox("Platform", ["TikTok", "YouTube Shorts", "Instagram Reels", "Facebook", "YouTube"])
    method = st.radio("Generation method", ["Free template", "AI-powered (optional API key)"], horizontal=True)
    api_key = ""
    model = "gpt-4.1-mini"
    if method.startswith("AI-powered"):
        try:
            api_key = st.secrets.get("OPENAI_API_KEY", "")
        except Exception:
            pass
        if not api_key:
            api_key = st.text_input("OpenAI API key (not your ChatGPT password)", type="password", help="Use Streamlit app secrets for persistent deployment. This field is temporary and should never be committed to GitHub.")
        model = st.text_input("API model", value="gpt-4.1-mini")
        st.caption("OpenAI API usage may cost money and is billed separately from ChatGPT Plus.")
    if st.button("Generate content pack", type="primary"):
        if not topic.strip():
            st.warning("Enter a video topic.")
        elif method.startswith("AI-powered") and not api_key:
            st.error("Provide an API key, or switch to Free template mode.")
        else:
            try:
                if method.startswith("AI-powered"):
                    result = ai_content(topic, audience, tone, duration, platform, api_key, model)
                else:
                    result = template_content(topic, audience, tone, duration, platform)
                result["created"] = datetime.now().isoformat(timespec="seconds")
                st.session_state["draft"] = result
            except Exception as exc:
                st.error(str(exc))
    if "draft" in st.session_state:
        result = st.session_state["draft"]
        st.success("Content pack prepared. Review and edit before publishing.")
        st.write("**Method:**", result["method"])
        st.write("**Title:**", result["title"])
        st.write("**Hook:**", result["hook"])
        st.text_area("Script", value=result["script"], height=230, key="draft_script_display")
        st.write("**Caption:**", result["caption"])
        st.write("**Hashtags:**", result["hashtags"])
        st.markdown("**Scenes:**")
        for scene in result["scenes"]:
            st.write("•", scene)
        st.download_button("Download this content pack", json.dumps(result, indent=2, ensure_ascii=False), file_name="sam_content_pack.json", mime="application/json")
        if st.button("Save to library"):
            items.append(result)
            if save_items(items):
                st.success("Saved locally. Download a backup because cloud storage may reset.")
            else:
                st.error("Could not save on this host. Download the content pack instead.")

elif page == "Production Planner":
    st.subheader("Production Planner")
    if not items:
        st.info("Save a content pack in Script Studio first.")
    else:
        chosen = st.selectbox("Saved content", range(len(items)), format_func=lambda i: items[i].get("title", "Untitled"))
        item = items[chosen]
        st.write("**Hook:**", item.get("hook", ""))
        st.text_area("Script", value=item.get("script", ""), height=180)
        for scene in item.get("scenes", []):
            st.write("•", scene)
        st.selectbox("Target aspect ratio", ["9:16 Vertical", "16:9 Landscape", "1:1 Square"])
        st.warning("This page prepares a scene plan. It does not render video or synthesize audio yet.")

elif page == "Publishing":
    st.subheader("Publishing planner")
    st.warning("No social accounts are connected and this app does not publish posts.")
    for i, item in enumerate(items):
        with st.expander(item.get("title", "Untitled")):
            st.write("Platform:", item.get("platform", ", ".join(item.get("platforms", []))))
            st.checkbox("Reviewed and ready for manual upload", key=f"review_{i}")

elif page == "Analytics":
    st.subheader("Analytics")
    st.metric("Connected accounts", 0)
    st.metric("Published videos tracked", 0)
    st.info("Official platform API integrations are required for live analytics.")

if items:
    st.sidebar.download_button("Export saved library", json.dumps(items, indent=2, ensure_ascii=False), file_name="sam_library_backup.json", mime="application/json")
st.divider()
st.caption("SAM AI MEDIA FACTORY • Phase 2 • Verify facts and rights before publishing. Cloud-local storage is temporary; export backups.")
