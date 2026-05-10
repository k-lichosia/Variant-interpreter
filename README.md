# Variant Interpreter

**Variant Interpreter** is a Python-based tool that integrates Large Language Models (LLMs) with genomic data analysis. The system automates the process of genetic variant interpretation by translating bioinformatic data into clinical-grade reports.

## Features

- **Automated Interpretation:** Generates professional descriptions of a mutation's impact on proteins using the Llama 3.1 model via the Groq API.
- **Scalable Data Sources:** Supports variants from external JSON files, allowing for easy integration with existing bioinformatic pipelines.
- **Future-Proof Configuration:** Manages model versions and AI parameters through environmental variables (`.env`), preventing downtime when older models are deprecated.
- **Privacy-First Security:** Architecture that separates application logic from access keys and sensitive data (utilizing `.gitignore` i `python-dotenv`).

## Project Structure

- `main.py`: Core application logic, LLM request handling, and data processing.
- `variants.json`: External input file containing the list of variants for analysis.
- `.env`: Configuration file (API keys, model names) – **not published in the repository**.

## Installation and Setup

1. **Install dependencies**
   ```bash
   pip install python-dotenv openai

2. **Environment Configuration**
    Create a .env file in the root directory and fill in the details:  
    GROQ_API_KEY=twoj_klucz_api    
    AI_MODEL=twoj_model_ai (np. llama-3.1-8b-instant)

3. **Run the analysis**
   ```bash
   python main.py
