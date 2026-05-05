import streamlit as st
from youtube_fetch import get_transcript, extract_video_id
from analyzer import analyze_transcript, generate_script
import pandas as pd

st.set_page_config(page_title="Viral Content Engine", page_icon="🚀", layout="wide")

st.title("🚀 Viral Content Engine")
st.caption("Turn competitor videos into your content strategy")

tab1, tab2, tab3 = st.tabs(["📊 Analyze Video", "✍️ Script Generator", "📈 History"])

with tab1:
    col1, col2 = st.columns([3, 1])
    with col1:
        video_input = st.text_input("YouTube URL or Video ID", placeholder="https://youtube.com/watch?v=... or dQw4w9WgXcQ")
    
    if st.button("🔍 Analyze", type="primary"):
        if video_input:
            with st.spinner("Fetching transcript..."):
                video_id = extract_video_id(video_input)
                text = get_transcript(video_id)
                
                if "Error" in text:
                    st.error(text)
                else:
                    with st.spinner("AI analyzing viral patterns..."):
                        insights = analyze_transcript(text)
                        
                        if "error" in insights:
                            st.error(f"Analysis failed: {insights['error']}")
                        else:
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.subheader("🔥 Top Hooks")
                                for hook in insights.get('hooks', [])[:5]:
                                    st.info(hook)
                                
                                st.subheader("💡 Video Ideas")
                                for idea in insights.get('video_ideas', [])[:5]:
                                    st.success(idea)
                            
                            with col2:
                                st.subheader("🎯 Viral Patterns")
                                for pattern in insights.get('viral_patterns', []):
                                    st.write(f"• {pattern}")
                                
                                st.subheader("🔑 Keywords")
                                st.write(", ".join(insights.get('keywords', [])[:10]))
        else:
            st.warning("Enter a video URL or ID")

with tab2:
    hook = st.text_input("Viral Hook", placeholder="Stop doing this if you want white teeth...")
    topic = st.text_input("Topic", placeholder="dental hygiene mistakes")
    
    if st.button("✨ Generate Script"):
        if hook and topic:
            script = generate_script(hook, topic)
            st.text_area("Your Script", script, height=200)
        else:
            st.warning("Both fields required")

with tab3:
    st.info("Analysis history will appear here for saved sessions")
