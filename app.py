import streamlit as st
import json
from datetime import datetime
from pathlib import Path
st.set_page_config(page_title='SAM AI MEDIA FACTORY',page_icon='🎬',layout='wide')
st.title('🎬 SAM AI MEDIA FACTORY')
st.caption('Phase 1 — content planning dashboard')
p=Path('scripts.json')
try: items=json.loads(p.read_text()) if p.exists() else []
except (ValueError,OSError): items=[]
page=st.sidebar.radio('Modules',['Dashboard','Research','Script Studio','Production Planner','Publishing','Analytics'])
if page=='Dashboard':
 st.subheader('Factory overview')
 a,b,c=st.columns(3);a.metric('Saved scripts',len(items));b.metric('Daily goal','50 videos');c.metric('Account goal','90')
 st.info('Goals are targets, not current production. This prototype does not generate videos or publish automatically.')
 st.write('Research → Scripts → Production → Review → Publishing → Analytics')
elif page=='Research':
 st.subheader('Research brief')
 topic=st.text_input('Topic or niche');audience=st.text_input('Audience');angle=st.selectbox('Angle',['Educational','Entertaining','Inspirational','Product'])
 if st.button('Create brief'):
  if topic.strip(): st.session_state.brief=f'Topic: {topic}\nAudience: {audience}\nAngle: {angle}\nNext: find reliable sources and draft a strong hook.'
  else: st.warning('Enter a topic.')
 if 'brief' in st.session_state: st.text_area('Brief',st.session_state.brief,height=130)
 st.caption('Live trends and external research are not connected yet.')
elif page=='Script Studio':
 st.subheader('Script Studio')
 title=st.text_input('Video title');hook=st.text_area('Hook');script=st.text_area('Narration',height=180);cta=st.text_input('Call to action')
 platforms=st.multiselect('Platforms',['YouTube','TikTok','Instagram','Facebook'])
 if st.button('Save script',type='primary'):
  if title.strip() and script.strip():
   items.append({'title':title,'hook':hook,'script':script,'cta':cta,'platforms':platforms,'created':datetime.now().isoformat(timespec='minutes')})
   try: p.write_text(json.dumps(items,indent=2));st.success('Saved. Export a copy for safekeeping.')
   except OSError: st.error('Storage unavailable. Export your work.')
  else: st.warning('Enter title and narration.')
 if items: st.download_button('Export all scripts',json.dumps(items,indent=2),'sam_scripts.json','application/json')
elif page=='Production Planner':
 st.subheader('Production Planner')
 if not items: st.info('Save a script first.')
 else:
  i=st.selectbox('Script',range(len(items)),format_func=lambda n:items[n]['title']);st.write(items[i]['script'])
  st.text_area('Scene plan','1. Hook visual\n2. Explain the idea\n3. Closing and call to action',height=140)
  st.selectbox('Aspect ratio',['9:16 Vertical','16:9 Landscape','1:1 Square'])
 st.warning('Video generation, voiceovers and editing are not connected yet.')
elif page=='Publishing':
 st.subheader('Publishing Planner');st.warning('No social accounts are connected. Nothing is automatically published.')
 for i,item in enumerate(items):
  with st.expander(item['title']):
   st.write('Platforms:',', '.join(item['platforms']) or 'None');st.checkbox('Reviewed',key=f'review_{i}')
else:
 st.subheader('Analytics');st.metric('Connected accounts',0);st.metric('Published videos tracked',0)
 st.info('Analytics integrations are planned for later phases.')
st.divider();st.caption('Starter prototype • Local data may be lost when cloud hosting restarts. Export your scripts regularly.')
