import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("AI_MODEL") 

if not api_key or not model_name:
    print("ERROR: Count not find API key or model name in environment variables. Please check your .env file.")
    exit()

client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key=api_key
)

def pobieranie_danych_medycznych(gene, variant):
    print(f"Fetching additional medical data for {gene} {variant} in MyVariant.info database...")

    zapytanie = f"{gene} AND {variant}"
    url = f"https://myvariant.info/v1/query?q={zapytanie}&fields=clinvar.rcv.clinical_significance,clinvar.rcv.conditions&size=1"

    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            dane = response.json()
            if dane.get('total', 0) > 0:
                hit = dane['hits'][0]
                return json.dumps(hit)
    except Exception as e:
        print(f"Failed to fetch data from MyVariant.info: {e}")
    
    return "No additional data found in external databases."            

def interpretuj_mutacje(gene, variant, effect, kontekst_medyczny):
    prompt = f"""
    You are a clinical bioinformatics expert. 
    Interpret the following genetic variant and return the response EXCLUSIVELY in JSON format.

    CRITICAL INSTRUCTIONS:
    1. You must base your 'medical_significance' and 'clinical_significance' STRICTLY on the 'External Database Context' provided below.
    2. If the External Context states 'No additional data found in external databases.' or is empty, DO NOT guess, DO NOT hallucinate, and DO NOT use your internal training data.
    3. If no data is provided in the context, explicitly output: "No clinical data available in external databases" for the medical fields.

    Input data:
    Gene: {gene}
    Variant: {variant}
    Effect type: {effect}

    External Database Context:
    {kontekst_medyczny}

    Expected JSON structure:
    {{
        "gene": "{gene}",
        "variant": "{variant}",
        "effect": "{effect}",
        "clinical_significance": "Extract exactly from context, or return 'Unknown' if missing",
        "protein_effect": "1-2 sentences describing the structural or functional change in the protein",
        "medical_significance": "Summarize the clinical consequences ONLY based on the External Context.",
        "recommendations": "short suggestions for further steps"
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
        kontekst_medyczny = pobieranie_danych_medycznych(mutation['gene'], mutation['variant'])
        wynik= interpretuj_mutacje(mutation['gene'], mutation['variant'], mutation['effect'], kontekst_medyczny)
        
        raport_koncowy.append(wynik)

        if "ERROR" not in wynik:
            print(f"Successfully interpreted {mutation['gene']} {mutation['variant']}\n")
        else:
            print(f"Failed to interpret {mutation['gene']} {mutation['variant']}: {wynik['ERROR']}\n")

    plik_json = "variant_report.json"
    try:
        with open(plik_json, 'w', encoding='utf-8') as f:
            json.dump(raport_koncowy, f, indent=4, ensure_ascii=False)
        print(f"Final report saved to {plik_json}")
    except Exception as e:
        print(f"ERROR: Could not save report - {str(e)}")
    
    try:
        df = pd.DataFrame(raport_koncowy)
        plik_csv = "variant_report.csv"
        df.to_csv(plik_csv, index=False, encoding='utf-8')
        print(f"Final report also saved to {plik_csv}")
    except Exception as e:
        print(f"ERROR: Could not save CSV report - {str(e)}")
    