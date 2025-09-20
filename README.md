🤖 AI Agent – Bank Statement PDF Parser

This repository contains an AI-powered agent that automatically generates custom parsers for bank statement PDFs. The agent analyzes sample statements and writes Python code that can extract structured data into CSV format.

🎯 Objective
The goal is to build a self-improving coding agent that, when given a new bank’s sample statement and CSV schema, can:

- Write a parser in custom_parsers/
- Test it automatically against the provided CSV
- Refine itself up to 3 times until a working parser is produced

🏗️ How the Agent Works
The agent operates in a plan → generate → test → refine cycle:
```
┌─────────┐    ┌──────────────┐    ┌─────────────┐    ┌─────────────┐
│ Planner │───▶│ Code Gen    │───▶│ Code Test  │───▶│ Success?   │
│         │    │             │    │             │    │             │
└─────────┘    └──────────────┘    └─────────────┘    └─────────────┘
                                                           │
                                                           ▼
                                                ┌─────────────────┐
                                                │ Self-Correct    │
                                                │ (≤3 attempts)   │
                                                └─────────────────┘
```

Main Components:
- Planner → inspects PDF + CSV to design a parsing approach
- Generator → uses Gemini AI to write parser code
- Tester → runs parser and checks output against expected CSV
- Correction loop → automatically retries on errors (up to 3 attempts)

🚀 Getting Started
1. Install Environment
git clone <your-repo-url>
cd Karbon-AI-agent
pip install -r requirements.txt

Set your Gemini API key (free keys available here):

# Windows
set GEMINI_API_KEY=your_api_key

# Linux/Mac
export GEMINI_API_KEY=your_api_key

2. Run the Agent
# Example: generate a parser for ICICI bank
python agent.py --target icici

The agent will:
- Load data/icici/icici_sample.pdf and icici_sample.csv
- Write custom_parsers/icici_parser.py
- Run tests automatically
- Retry up to 3 times if needed

3. Validate the Parser
python -m pytest tests/test_icici_parser.py -v

📂 Repository Layout
```
Karbon-AI-agent/
├── agent.py                 # Main AI agent implementation
├── custom_parsers/          # Generated parser modules
│   ├── __init__.py
│   └── icici_parser.py     # Example parser for ICICI bank
├── data/                    # Sample data for different banks
│   └── icici/
│       ├── icic_sample.pdf # Sample PDF statement
│       └── icic_sample.csv # Expected CSV output
├── tests/                   # Test files
│   └── test_icici_parser.py
├── requirements.txt         # Python dependencies
└── README.md               # This file
```
🔧 Behind the Scenes
Workflow: Plan → Analyze PDF + schema → Generate code → Test → Retry → Verified parser

Parser Contract:
Each parser must implement:
def parse(pdf_path: str) -> pd.DataFrame:
    '''Return a DataFrame with the expected CSV schema.'''

🧪 Testing Strategy
- Input → Bank’s sample PDF
- Expected → Bank’s sample CSV
- Validation → Uses pd.testing.assert_frame_equal() for correctness

✨ Features
- 🔄 Autonomous: Minimal human input once setup
- 🛠 Self-healing: Up to 3 retries on failure
- 🏦 Bank-independent: Extendable to any statement format
- ✅ Robust: Strict schema + data validation

🔑 Requirements
- Google Gemini API key (for parser generation)
- Python 3.10+ with pandas, pypdf, pytest, and LangGraph

⚠️ Troubleshooting
- Missing API Key → Set environment variable as shown above.
- File Not Found → Place your files in data/{bank}/.
- Test Mismatch → Agent retries automatically (≤3 attempts).

📈 Extending to New Banks
- Add data/{bank}/{bank}_sample.pdf and {bank}_sample.csv
- Run: python agent.py --target {bank}
- Test parser with pytest

🤝 Contributing
- Fork the repo
- Create a feature branch
- Add tests for any new logic
- Open a pull request

📜 License
This project is developed as part of the Karbon AI Challenge.

🙏 Credits
- LangGraph – workflow orchestration
- Google Gemini – AI code generation
- Inspired by mini-swe-agent architecture
