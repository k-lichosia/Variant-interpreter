# Variant Interpreter

**Variant Interpreter** to narzędzie oparte na Pythonie, które integruje zaawansowane modele językowe (LLM) z analizą danych genomicznych. System automatyzuje proces interpretacji wariantów genetycznych, tłumacząc dane bioinformatyczne na raporty kliniczne.

## Funkcjonalności

- **Automatyczna Interpretacja:** Generowanie profesjonalnych opisów wpływu mutacji na białko przy użyciu modelu Llama 3.1 przez API Groq.
- **Skalowalne Źródła Danych:** Obsługa wariantów z zewnętrznych plików JSON, co pozwala na łatwą integrację z istniejącymi rurociągami (pipelines) bioinformatycznymi.
- **Konfiguracja Future-Proof:** Zarządzanie wersjami modeli i parametrami AI za pomocą zmiennych środowiskowych (`.env`), co zapobiega przestojom w przypadku wycofania starszych modeli.
- **Bezpieczeństwo (Privacy-First):** Architektura oddzielająca logikę aplikacji od kluczy dostępowych i danych wrażliwych (wykorzystanie `.gitignore` i `python-dotenv`).

## Struktura Projektu

- `main.py`: Główna logika aplikacji, obsługa zapytań do LLM i przetwarzanie danych.
- `variants.json`: Zewnętrzny plik wejściowy z listą wariantów do analizy.
- `.env`: Plik konfiguracyjny (klucze API, nazwy modeli) – **niepublikowany w repozytorium**.
- `.gitignore`: Definicja plików wykluczonych z kontroli wersji.

## Instalacja i Uruchomienie

1. **Instalacja zależności**
   ```bash
   pip install python-dotenv openai

2. **Konfiguracja środowiska**
    Stwórz plik .env w katalogu głównym i uzupełnij go:
    GROQ_API_KEY=twoj_klucz_api
    AI_MODEL=twoj_model_ai

3. **Uruchomienie analizy**
   ```bash
   python main.py
