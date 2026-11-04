# SAM AI MEDIA FACTORY — Phase 3 foundation

This release adds a cinematic scene prompt planner and working MP4 clip assembly to your Streamlit dashboard.

## Included
- Cinematic scene prompts for three moving scenes
- Upload up to five existing MP4 clips (25 MB each)
- Normalize and join the clips with FFmpeg
- Preview and download assembled MP4
- Basic script/research outlines, production checklist, publishing/analytics placeholders

## Not included yet
True AI text-to-video generation, audio narration, subtitles, automatic publishing, and analytics require further integrations. The app does not generate AI video from prompts by itself. A GPU or video inference API is required for that.

## Upgrade warning
This app.py **replaces the Phase 2 app**, and Phase 2 content library functions are not retained. Download any saved content packs **before** uploading this version. Streamlit Community Cloud local files are not durable.

## Deploy
Upload app.py, requirements.txt, README.md, and .gitignore to your existing GitHub repository root. The existing Streamlit site should redeploy.
