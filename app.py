import streamlit as st
import asyncio
import os
import logging
import nest_asyncio
import base64
from dotenv import load_dotenv
from job_agents import run_analysis
from mcp_server import wait_for_initialization, get_mcp_server

nest_asyncio.apply()
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Set page config
st.set_page_config(
    page_title="LinkedIn Profile Analyzer",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'analysis_result' not in st.session_state:
    st.session_state.analysis_result = ""
if 'is_analyzing' not in st.session_state:
    st.session_state.is_analyzing = False

async def analyze_profile(linkedin_url: str, api_key: str):
    try:
        if not await wait_for_initialization():
            st.error("Failed to initialize MCP server")
            return

        result = await run_analysis(get_mcp_server(), linkedin_url, api_key)
        st.session_state.analysis_result = result
    except Exception as e:
        logger.error(f"Error analyzing LinkedIn profile: {str(e)}")
        st.error(f"Error analyzing LinkedIn profile: {str(e)}")
    finally:
        st.session_state.is_analyzing = False

def main():
    st.title("🚀 Zero-Cost AI Job Searcher")
    st.markdown("---")

    # Sidebar
    with st.sidebar:
        api_key = st.text_input("Enter your API key", type="password")
        st.divider()

        st.subheader("Enter LinkedIn Profile URL")
        linkedin_url = st.text_input("LinkedIn URL", placeholder="https://www.linkedin.com/in/username/")

        if st.button("Analyze Profile", type="primary", disabled=st.session_state.is_analyzing):
            if not linkedin_url:
                st.error("Please enter a LinkedIn profile URL")
                return
            if not api_key:
                st.error("Please enter your API key")
                return

            st.session_state.is_analyzing = True
            st.session_state.analysis_result = ""

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                loop.run_until_complete(analyze_profile(linkedin_url, api_key))
            finally:
                loop.close()

    # Results section
    if st.session_state.analysis_result:
        st.subheader("Analysis Results")
        st.markdown(st.session_state.analysis_result)

    # Loading state
    if st.session_state.is_analyzing:
        st.markdown("---")
        with st.spinner("Analyzing profile... This may take a few minutes."):
            st.empty()

if __name__ == "__main__":
    main()