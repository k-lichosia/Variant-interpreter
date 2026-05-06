import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("AI_MODEL")

if not api_key:
    print("ERROR: Nie znaleziono klucza API. Upewnij się, że plik .env istnieje.")
    exit()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

def interpretuj_mutacje(gene, variant, effect):
    prompt = f"""
    Jesteś ekspertem bioinformatyki klinicznej. 
    Zinterpretuj krótko poniższy wariant:
    Gen: {gene}
    Wariant: {variant}
    Typ zmiany: {effect}
    
    Napisz 3-4 zdania wyjaśniające wpływ tej mutacji na białko i jej znaczenie medyczne.
    Używaj fachowego słownictwa.
    """
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5 
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"{e}"

def load_variants(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    print("--- START ANALIZATORA AI ---\n")

    try:
        sample_variants = load_variants("variants.json")
    except FileNotFoundError:
        print("ERROR: Nie znaleziono pliku variants.json")
        sample_variants = []
    
    for mutation in sample_variants:
        print(f"Analizuję: {mutation['gene']} {mutation['variant']}...")
        wynik = interpretuj_mutacje(mutation['gene'], mutation['variant'], mutation['effect'])
        print(f"RAPORT AI:\n{wynik}\n")
        print("-" * 40)