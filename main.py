import os
import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("AI_MODEL") 

if not api_key or not model_name:
    print("ERROR: Nie znaleziono klucza API lub nazwy modelu. Upewnij się, że plik .env istnieje i jest poprawnie wypełniony.")
    exit()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

def interpretuj_mutacje(gene, variant, effect):
    prompt = f"""
    You are a clinical bioinformatics expert. 
    Interpret the following genetic variant and return the response EXCLUSIVELY in JSON format.

    Input data:
    Gene: {gene}
    Variant: {variant}
    Effect type: {effect}

    Expected JSON structure:
    {{
        "gene": "{gene}",
        "variant": "{variant}",
        "effect": "{effect}",
        "clinical_significance": " Pathogenic, Benign, Uncertain significance",
        "protein_effect": "1-2 sentences describing the structural or functional change in the protein",
        "medical_significance": "1-2 sentences regarding clinical consequences",
        "recommendations": "short suggestions for further steps (e.g., ClinVar verification)"
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            response_format={"type": "json_object"} 
        )

        surowy_json = response.choices[0].message.content
        sparsowany_json = json.loads(surowy_json)

        return sparsowany_json
    
    except Exception as e:
        return {"ERROR": str(e)}

def load_variants(filepath):
    with open(filepath, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    print("--- START OF VARIANT INTERPRETATION ---\n")

    try:
        sample_variants = load_variants("variants.json")
    except FileNotFoundError:
        print("ERROR: Could not find variants.json")
        sample_variants = []

    raport_koncowy = []
    
    for mutation in sample_variants:
        print(f"Analyzing: {mutation['gene']} {mutation['variant']}...")
        wynik = interpretuj_mutacje(mutation['gene'], mutation['variant'], mutation['effect'])

        raport_koncowy.append(wynik)

        if "ERROR" not in wynik:
            print(f"Pathogenicity: {wynik.get('clinical_significance', 'No data')}")
            print(f"Protein Effect: {wynik.get('protein_effect', 'No data')}")
            print("\n---\n")

    plik_wynikowy = "variant_report.json"
    try:
        with open(plik_wynikowy, 'w', encoding='utf-8') as f:
            json.dump(raport_koncowy, f, indent=4, ensure_ascii=False)
        print(f"Final report saved to {plik_wynikowy}")
    except Exception as e:
        print(f"ERROR: Could not save report - {str(e)}")
