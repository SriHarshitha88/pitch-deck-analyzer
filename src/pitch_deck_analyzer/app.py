import streamlit as st
import os
import sys
from datetime import datetime

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, project_root)

from src.pitch_deck_analyzer.crew import PitchDeckCrew

def check_api_keys():
    """Check if required API keys are set."""
    if not os.getenv("OPENAI_API_KEY"):
        st.error("OPENAI_API_KEY environment variable is not set!")
        st.info("Please set your OpenAI API key in the .env file or environment variables.")
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
                        
                        # Create a container for the report
                        report_container = st.container()
                        with report_container:
                            st.markdown("""
                                <style>
                                .report-header {
                                    background-color: #f0f2f6;
                                    padding: 20px;
                                    border-radius: 10px;
                                    margin-bottom: 20px;
                                }
                                .section-header {
                                    color: #1f77b4;
                                    border-bottom: 2px solid #1f77b4;
                                    padding-bottom: 5px;
                                    margin-top: 20px;
                                }
                                .highlight-box {
                                    background-color: #e6f3ff;
                                    padding: 15px;
                                    border-radius: 5px;
                                    margin: 10px 0;
                                }
                                .risk-box {
                                    background-color: #fff3e6;
                                    padding: 15px;
                                    border-radius: 5px;
                                    margin: 10px 0;
                                }
                                .recommendation-box {
                                    background-color: #e6ffe6;
                                    padding: 15px;
                                    border-radius: 5px;
                                    margin: 10px 0;
                                }
                                </style>
                            """, unsafe_allow_html=True)
                            
                            # Report Header
                            st.markdown(f"""
                                <div class="report-header">
                                    <h1 style="text-align: center; color: #1f77b4;">INVESTMENT ANALYSIS REPORT</h1>
                                    <p style="text-align: center;">Generated for: {result.get('company_name', 'N/A')}</p>
                                    <p style="text-align: center;">Date: {result['timestamp']}</p>
                                </div>
                            """, unsafe_allow_html=True)
                            
                            # Executive Summary
                            st.markdown('<h2 class="section-header">EXECUTIVE SUMMARY</h2>', unsafe_allow_html=True)
                            exec_summary = result['content'].split('## COMPANY ANALYSIS')[0]
                            st.markdown(exec_summary)
                            
                            # Company Analysis
                            st.markdown('<h2 class="section-header">COMPANY ANALYSIS</h2>', unsafe_allow_html=True)
                            company_analysis = result['content'].split('## COMPANY ANALYSIS')[1].split('## MARKET ANALYSIS')[0]
                            st.markdown(company_analysis)
                            
                            # Market Analysis
                            st.markdown('<h2 class="section-header">MARKET ANALYSIS</h2>', unsafe_allow_html=True)
                            market_analysis = result['content'].split('## MARKET ANALYSIS')[1].split('## COMPETITIVE LANDSCAPE')[0]
                            st.markdown(market_analysis)
                            
                            # Competitive Landscape
                            st.markdown('<h2 class="section-header">COMPETITIVE LANDSCAPE</h2>', unsafe_allow_html=True)
                            competitive = result['content'].split('## COMPETITIVE LANDSCAPE')[1].split('## FINANCIAL ANALYSIS')[0]
                            st.markdown(competitive)
                            
                            # Financial Analysis
                            st.markdown('<h2 class="section-header">FINANCIAL ANALYSIS</h2>', unsafe_allow_html=True)
                            financial = result['content'].split('## FINANCIAL ANALYSIS')[1].split('## RISK ASSESSMENT')[0]
                            st.markdown(financial)
                            
                            # Risk Assessment
                            st.markdown('<h2 class="section-header">RISK ASSESSMENT</h2>', unsafe_allow_html=True)
                            risk = result['content'].split('## RISK ASSESSMENT')[1].split('## DIGITAL PRESENCE AUDIT')[0]
                            st.markdown(f'<div class="risk-box">{risk}</div>', unsafe_allow_html=True)
                            
                            # Digital Presence Audit
                            st.markdown('<h2 class="section-header">DIGITAL PRESENCE AUDIT</h2>', unsafe_allow_html=True)
                            digital = result['content'].split('## DIGITAL PRESENCE AUDIT')[1].split('## INVESTMENT RECOMMENDATION')[0]
                            st.markdown(digital)
                            
                            # Investment Recommendation
                            st.markdown('<h2 class="section-header">INVESTMENT RECOMMENDATION</h2>', unsafe_allow_html=True)
                            recommendation = result['content'].split('## INVESTMENT RECOMMENDATION')[1].split('## NEXT STEPS')[0]
                            st.markdown(f'<div class="recommendation-box">{recommendation}</div>', unsafe_allow_html=True)
                            
                            # Next Steps
                            st.markdown('<h2 class="section-header">NEXT STEPS</h2>', unsafe_allow_html=True)
                            next_steps = result['content'].split('## NEXT STEPS')[1]
                            st.markdown(next_steps)
                            
                            # Download button
                            st.markdown("---")
                            if 'report_path' in result:
                                with open(result['report_path'], 'r', encoding='utf-8') as f:
                                    report_content = f.read()
                                st.download_button(
                                    label="📥 Download Full Report",
                                    data=report_content,
                                    file_name=f"{result['company_name']}_analysis_{result['timestamp']}.txt",
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