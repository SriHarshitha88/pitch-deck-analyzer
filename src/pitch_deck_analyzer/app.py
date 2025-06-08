import streamlit as st
import os
import sys
from datetime import datetime


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.pitch_deck_analyzer.crew import PitchDeckCrew

def check_api_keys():
    """Check if required API keys are set."""
    if not os.getenv("GROQ_API_KEY"):
        st.error("GROQ_API_KEY environment variable is not set!")
        st.info("Please set your Groq API key in the .env file or environment variables.")
        return False
    return True

def initialize_crew():
    """Initialize the PitchDeckCrew"""
    if not check_api_keys():
        st.stop()
    return PitchDeckCrew()

def main():
    st.set_page_config(
        page_title="Pitch Deck Analyzer",
        page_icon="📊",
        layout="wide"
    )

    st.title("AI-Driven Pitch Deck Analysis Platform")
    st.write("Analyze your pitch deck with our advanced AI-powered tools")

    
    if 'crew' not in st.session_state:
        try:
            st.session_state.crew = initialize_crew()
        except Exception as e:
            st.error(f"Error initializing crew: {str(e)}")
            st.stop()
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []

    
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Choose a feature:",
        ["Analyze Pitch Deck", "View History"]
    )

    if page == "Analyze Pitch Deck":
        st.header("Analyze New Pitch Deck")
        
       
        company_name = st.text_input("Company Name", help="Enter the company name for analysis")
        
      
        uploaded_file = st.file_uploader("Upload your pitch deck (PDF/PPT)", type=['pdf', 'ppt', 'pptx'])
        
        website_url = st.text_input("Company Website URL (optional)")
        
        if uploaded_file and company_name and st.button("Start Analysis"):
            os.makedirs("uploads", exist_ok=True)
            file_path = os.path.join("uploads", uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            with st.spinner("Analyzing pitch deck..."):
                try:
                    result = st.session_state.crew.analyze_pitch_deck(
                        pitch_deck_path=file_path,
                        company_name=company_name,
                        website_url=website_url if website_url else ""
                    )
                    
                    
                    if result['status'] == 'success':
                        st.session_state.analysis_history.append({
                            'analysis_id': f"analysis_{len(st.session_state.analysis_history) + 1}",
                            'timestamp': result['timestamp'],
                            'company_name': company_name,
                            'pitch_deck_path': file_path,
                            'result': result
                        })
                        
                       
                        st.success("Analysis completed!")
                        st.subheader("Analysis Results")
                        
                        st.text_area("Analysis Report", str(result['content']), height=400)
                        
                       
                        st.write(f"**Generated at:** {result['timestamp']}")
                        st.write(f"**Company:** {result.get('company_name', 'N/A')}")
                        st.write(f"**Analysis Type:** {result.get('analysis_type', 'comprehensive')}")
                        st.write(f"**Duration:** {result.get('duration_seconds', 0):.2f} seconds")
                        
                       
                        if 'report_path' in result:
                            st.write(f"**Report saved to:** {result['report_path']}")
                            
                            
                            if os.path.exists(result['report_path']):
                                with open(result['report_path'], 'r', encoding='utf-8') as f:
                                    report_content = f.read()
                                st.download_button(
                                    label="Download Report",
                                    data=report_content,
                                    file_name=os.path.basename(result['report_path']),
                                    mime="text/plain"
                                )
                    else:
                        st.error("Analysis failed!")
                        st.error(f"Error: {result.get('message', 'Unknown error')}")
                        st.write(f"**Error Type:** {result.get('error_type', 'Unknown')}")
                        
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    st.write("Please check your configuration files and API keys.")

    elif page == "View History":
        st.header("Analysis History")
        
        if not st.session_state.analysis_history:
            st.info("No analysis history available")
        else:
            for analysis in st.session_state.analysis_history:
                with st.expander(f"Analysis {analysis['analysis_id']} - {analysis['company_name']}"):
                    st.write(f"**Date:** {analysis['timestamp']}")
                    st.write(f"**Company:** {analysis['company_name']}")
                    st.write(f"**Pitch Deck:** {analysis['pitch_deck_path']}")
                    
                    if st.button(f"View Details", key=analysis['analysis_id']):
                        analysis_content = analysis['result'].get('content', 'No content available')
                        st.text_area("Analysis Details", str(analysis_content), height=300)

if __name__ == "__main__":
    main()