# Pitch Deck Analyzer

An AI-powered platform that analyzes pitch decks and provides comprehensive investment analysis reports. Built with Streamlit and powered by OpenAI's GPT-4, this tool helps investors and entrepreneurs evaluate pitch decks efficiently.

## 🎥 Demo Video

[![Pitch Deck Analyzer Demo](https://via.placeholder.com/800x450?text=Pitch+Deck+Analyzer+Demo)](<!-- Uploading "WhatsApp Video 2025-06-17 at 1.52.45 PM.mp4"... -->)

*Click the image above to watch the demo video*

## ✨ Features

- **AI-Powered Analysis**: Utilizes OpenAI's GPT-4 for intelligent pitch deck analysis
- **Comprehensive Reports**: Generates detailed investment analysis reports including:
  - Executive Summary
  - Company Analysis
  - Market Analysis
  - Competitive Landscape
  - Financial Analysis
  - Risk Assessment
  - Digital Presence Audit
  - Investment Recommendations
  - Next Steps
- **Multiple File Formats**: Supports PDF, PowerPoint (PPT/PPTX), and Word (DOCX) files
- **Beautiful UI**: Clean and professional interface built with Streamlit
- **Export Capabilities**: Download analysis reports in text format
- **History Tracking**: Maintains a history of previous analyses

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- OpenAI API key
- Serper API key (for web search capabilities)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pitch-deck-analyzer.git
cd pitch-deck-analyzer
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -e .
```

4. Create a `.env` file in the project root and add your API keys:
```
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
```

### Running the Application

1. Start the Streamlit app:
```bash
streamlit run src/pitch_deck_analyzer/app.py
```

2. Open your browser and navigate to the URL shown in the terminal (typically http://localhost:8501)

## 📝 Usage

1. **Upload Pitch Deck**:
   - Click the "Upload" button
   - Select your pitch deck file (PDF, PPT, PPTX, or DOCX)

2. **Enter Company Information**:
   - Provide the company name
   - Optionally add the company website URL

3. **Start Analysis**:
   - Click "Start Analysis"
   - Wait for the AI to process your pitch deck

4. **View Results**:
   - Review the comprehensive analysis report
   - Download the report if needed
   - View analysis history in the sidebar

## 🛠️ Technical Details

- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-4
- **File Processing**: Python-PPTX, PyPDF2, python-docx
- **Web Search**: Serper API
- **Project Structure**:
  ```
  pitch-deck-analyzer/
  ├── src/
  │   └── pitch_deck_analyzer/
  │       ├── app.py
  │       ├── crew.py
  │       ├── run.py
  │       └── tools/
  ├── uploads/
  ├── pyproject.toml
  └── requirements.txt
  ```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT-4 API
- Streamlit for the web framework
- CrewAI for the AI agent framework

