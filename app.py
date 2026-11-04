import streamlit as st
import json, subprocess, tempfile
from pathlib import Path
import imageio_ffmpeg

st.set_page_config(page_title='SAM AI MEDIA FACTORY', page_icon='🎬', layout='wide')
st.title('🎬 SAM AI MEDIA FACTORY')
st.caption('Phase 3 — cinematic scene planning and MP4 assembly')
page = st.sidebar.radio('Modules', ['Dashboard', 'Research & Ideas', 'Script Studio', 'Cinematic Studio', 'Production Planner', 'Publishing', 'Analytics'])
st.sidebar.caption('AI text-to-video generation requires an external GPU or API and is not connected yet.')

if page == 'Dashboard':
    st.subheader('Factory overview')
    a,b,c=st.columns(3)
    a.metric('Phase', '3')
    b.metric('Daily target', '50 videos')
    c.metric('Account target', '90')
    st.info('Targets are not live production figures. This release creates scene prompts and assembles existing moving MP4 clips.')
elif page == 'Research & Ideas':
    st.subheader('Research brief')
    topic=st.text_input('Topic')
    audience=st.text_input('Audience')
    if st.button('Prepare research brief'):
        if topic.strip():
            st.session_state['brief']=f'Topic: {topic}\nAudience: {audience or "General"}\nVerify three key facts with reliable sources. Identify the strongest visual examples.'
        else: st.warning('Enter a topic first.')
    if 'brief' in st.session_state: st.text_area('Brief',st.session_state['brief'],height=140)
    st.caption('Live trend research is not connected.')
elif page == 'Script Studio':
    st.subheader('Narration script planner')
    topic=st.text_input('Topic')
    if st.button('Create script outline'):
        if topic.strip(): st.session_state['outline']=f'[Hook] Open with a compelling question about {topic}.\n[Body] Explain three specific, verified points.\n[Close] Summarize the takeaway.'
        else: st.warning('Enter a topic.')
    st.text_area('Editable outline',value=st.session_state.get('outline',''),height=200)
    st.caption('Template outline only; language-model generation and narration audio are not connected.')
elif page == 'Cinematic Studio':
    st.subheader('Cinematic Studio')
    st.write('Create scene prompts, then assemble real moving video clips from a video generator or footage you own.')
    topic=st.text_input('Video concept',value='Futuristic city at sunrise')
    style=st.selectbox('Visual style',['Photorealistic cinematic','Dreamlike science fiction','Nature documentary','Luxury commercial'])
    ratio=st.selectbox('Format',['Vertical 9:16','Landscape 16:9'])
    if st.button('Create scene prompts'):
        st.session_state['prompts']=[
            f'Wide cinematic establishing shot of {topic}. {style}. Slow tracking camera, rich light, no logos, {ratio}.',
            f'Medium shot revealing details of {topic}. {style}. Smooth dolly movement, realistic depth, no text, {ratio}.',
            f'Closing cinematic shot of {topic}. {style}. Gentle crane movement, atmospheric ending, no logos, {ratio}.'
        ]
    if 'prompts' in st.session_state:
        for i,prompt in enumerate(st.session_state['prompts'],1): st.text_area(f'Scene {i}',prompt,height=90)
        st.download_button('Download prompts',json.dumps(st.session_state['prompts'],indent=2),file_name='sam_scene_prompts.json',mime='application/json')
    st.divider()
    st.markdown('#### Assemble moving MP4 scenes')
    files=st.file_uploader('Upload MP4 clips in playback order (up to 5 clips, 25 MB each)',type=['mp4'],accept_multiple_files=True)
    if files and st.button('Assemble video',type='primary'):
        if len(files)>5 or any(f.size>25*1024*1024 for f in files):
            st.error('Maximum 5 clips, each 25 MB or less.')
        else:
            try:
                with st.spinner('Assembling video...'):
                    ffmpeg=imageio_ffmpeg.get_ffmpeg_exe()
                    w,h=(720,1280) if ratio.startswith('Vertical') else (1280,720)
                    with tempfile.TemporaryDirectory() as tmp:
                        tmp=Path(tmp)
                        outputs=[]
                        for i,f in enumerate(files):
                            source=tmp/f'source{i}.mp4'; source.write_bytes(f.getvalue())
                            dest=tmp/f'normalized{i}.mp4'
                            command=[ffmpeg,'-y','-i',str(source),'-vf',f'scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps=24','-an','-c:v','libx264','-preset','ultrafast','-pix_fmt','yuv420p',str(dest)]
                            result=subprocess.run(command,capture_output=True,text=True,timeout=150)
                            if result.returncode: raise RuntimeError(result.stderr[-500:])
                            outputs.append(dest)
                        manifest=tmp/'clips.txt'; manifest.write_text(''.join(f"file '{p.as_posix()}'\n" for p in outputs))
                        final=tmp/'final.mp4'
                        result=subprocess.run([ffmpeg,'-y','-f','concat','-safe','0','-i',str(manifest),'-c','copy',str(final)],capture_output=True,text=True,timeout=150)
                        if result.returncode: raise RuntimeError(result.stderr[-500:])
                        st.session_state['video']=final.read_bytes()
                st.success('Video assembled!')
            except Exception as exc: st.error(f'Video processing failed: {exc}')
    if st.session_state.get('video'):
        st.video(st.session_state['video'])
        st.download_button('Download assembled MP4',st.session_state['video'],file_name='sam_cinematic.mp4',mime='video/mp4')
    st.warning('This feature assembles existing moving clips. It does NOT generate AI motion from prompts, voiceovers, or subtitles yet.')
elif page == 'Production Planner':
    st.subheader('Production checklist')
    for item in ['Verify script facts','Approve prompts','Obtain rights to moving clips','Check audio rights','Review final video']:
        st.checkbox(item)
elif page == 'Publishing':
    st.subheader('Publishing')
    st.warning('No accounts connected. No automatic posting. Official platform APIs and authorization are needed.')
else:
    st.subheader('Analytics')
    st.metric('Connected accounts',0)
    st.metric('Published videos tracked',0)
    st.info('Platform analytics integration is not yet connected.')
st.divider()
st.caption('SAM AI MEDIA FACTORY • Phase 3 foundation • Cloud-local files are temporary.')
