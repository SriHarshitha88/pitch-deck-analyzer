from dotenv import load_dotenv
import streamlit as st
from pitch_deck_analyzer import PitchDeckCrew, FileProcessor
import os
from pathlib import Path

def main():
    # Load environment variables
    load_dotenv()

    # Set page config
    st.set_page_config(
        page_title="Pitch Deck Analysis Platform",
        page_icon="📊",
        layout="wide"
    )

    # Check for required API keys
    required_keys = ["GROQ_API_KEY", "SERPER_API_KEY"]
    missing_keys = [key for key in required_keys if not os.getenv(key)]
    
    if missing_keys:
        st.error(f"Missing required API keys: {', '.join(missing_keys)}")
        st.info("Please add the missing API keys to your .env file")
        return

    st.title("📊 Pitch Deck Analysis Platform")
    st.write("Upload your pitch deck and get AI-powered analysis and recommendations.")

    # Initialize the crew
    crew = PitchDeckCrew()

    # Company information
    company_name = st.text_input("Company Name", "")
    website_url = st.text_input("Company Website URL (optional)", "")

    # Analysis options
    analysis_type = st.selectbox(
        "Analysis Type",
        ["comprehensive", "quick", "investor-focused"],
        help="Choose the type of analysis to perform"
    )

    # File upload
    uploaded_file = st.file_uploader(
        "Choose a pitch deck file",
        type=['pdf', 'pptx', 'docx'],
        help="Upload your pitch deck in PDF, PowerPoint, or Word format"
    )

    if uploaded_file and company_name:
        try:
            # Save the uploaded file temporarily
            temp_dir = Path("temp")
            temp_dir.mkdir(exist_ok=True)
            
            file_path = temp_dir / uploaded_file.name
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getvalue())
            
            # Analyze the pitch deck
            with st.spinner("Analyzing pitch deck..."):
                result = crew.analyze_pitch_deck(
                    pitch_deck_path=str(file_path),
                    company_name=company_name,
                    website_url=website_url if website_url else None,
                    analysis_type=analysis_type
                )
                
                if result["status"] == "success":
                    st.success("Analysis completed successfully!")
                    
                    # Display the report
                    st.subheader(f"Analysis Report for {result['company_name']}")
                    st.text(result["content"])
                    
                    # Provide download link
                    with open(result["report_path"], "r", encoding="utf-8") as f:
                        report_content = f.read()
                    st.download_button(
                        label="Download Report",
                        data=report_content,
                        file_name=f"{result['company_name']}_analysis_{result['timestamp']}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error(f"Analysis failed: {result['message']}")
                    
        except Exception as e:
            st.error(f"Error during analysis: {str(e)}")
            st.info("Please check your configuration files and API keys.")
            
        finally:
            # Clean up temporary file
            if file_path.exists():
                file_path.unlink()
    elif uploaded_file and not company_name:
        st.warning("Please enter the company name to proceed with the analysis.")

if __name__ == "__main__":
    main()

 