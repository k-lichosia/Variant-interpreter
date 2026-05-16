# Variant Interpreter

**Variant Interpreter** is a Python-based tool that integrates LLMs with genomic data analysis. The system automates the process of genetic variant interpretation by translating bioinformatic data into clinical-grade reports using a Retrieval-Augmented Generation (RAG) architecture.

## Features

- **Retrival-Augmented Generation (RAG):** Integrates with the MyVariant.info API to fetch real-world clinical data and prevents model hallucinations through strict grounding instructions.
- **Automated Clinical Interpretation:** Generates professional descriptions of a mutation's impact on proteins and its medical significance using the Llama 3.1 model via the Groq API.
- **Structured Data Output:** Enforces strict JSON responses from the LLM, ensuring the output is ready for programmatic downstream processing.
- **Data Export & Reporting** Processes batches of variants and automatically generates comprehensive reports in both JSON and CSV formats.
- **Privacy-First Security:** Architecture that separates application logic from access keys and sensitive data (utilizing `.gitignore` i `python-dotenv`).

## Project Structure

- `main.py`: Core application logic, external API integrations, and LLM request handling.
- `variants.json`: External input file containing the list of variants for analysis.
- `variant_report.json` / `variant_report.csv`: Auto-generated output reports containing the AI interpretations. 
- `.env`: Configuration file (API keys, model names) – **not published in the repository**.

## Installation and Setup

1. **Install dependencies**
   ```bash
   pip install python-dotenv openai requests pandas

2. **Environment Configuration**
   Create a .env file in the root directory and fill in the details:  
   ```bash
   GROQ_API_KEY=your_API_key   
   AI_MODEL=llama-3.1-8b-instant

3. **Run the analysis**
   ```bash
   python main.py
