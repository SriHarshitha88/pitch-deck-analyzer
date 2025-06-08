# AI-Driven Pitch Deck Analysis Platform

This platform uses CrewAI to analyze pitch decks and generate structured reports using AI. The application provides a simple Streamlit interface for uploading and analyzing pitch decks.

## Features

- Upload and analyze pitch decks (PDF/PPT)
- Generate AI-powered analysis reports
- Compare different versions of pitch decks
- Export reports in various formats
- Knowledge base integration for context-aware analysis

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   SERPER_API_KEY=your_serper_api_key_here  # Optional, for search functionality
   ```
4. Run the application:
   ```bash
   streamlit run src/pitch_deck_analyzer/app.py
   ```

## Project Structure

```
.
├── src/
│   └── pitch_deck_analyzer/
│       ├── __init__.py
│       ├── app.py              # Streamlit interface
│       ├── crew.py             # CrewAI orchestration
│       ├── config/             # Configuration files
│       │   ├── agents.yaml
│       │   └── tasks.yaml
│       └── tools/              # Custom tools
│           ├── __init__.py
│           ├── file_processor.py
│           └── website_audit.py
├── requirements.txt           # Project dependencies
└── README.md                 # This file
```

## Usage

1. Launch the application using `streamlit run src/pitch_deck_analyzer/app.py`
2. Upload your pitch deck (PDF or PPT)
3. Enter company name and optional website URL
4. Generate and view the analysis report
5. Download the report in text format

## License

MIT License 