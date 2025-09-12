"""
HTML File Processor for Koteria App

Processes HTML files and extracts structured data.
Following Streamlit best practices for modular code organization.
"""

import re
import pandas as pd
from bs4 import BeautifulSoup
import csv

def clean_multiline(text_list):
    joined = " ".join(text_list)
    # Replace all kinds of line breaks, tabs, and excess whitespace with single space
    return re.sub(r"[\n\r\t]+", " ", joined).strip()

def read_html(file_path, file_name):
    # Step 1: Read HTML file
    with open(file_path, encoding="iso-8859-2") as f:
        html = f.read()

    # Step 2: Split by visits using the <B>DATE: Wizyta<BR></B> or Badanie marker
    visit_sections = re.split(r"<B>\s*\d{2}/\d{2}/\d{4} \d{2}:\d{2}: (?:Wizyta|Badanie)<BR>\s*</B>", html)

    # Step 3: Extract date-time info to match with split sections
    visit_headers = re.findall(r"<B>\s*(\d{2}/\d{2}/\d{4} \d{2}:\d{2}): (Wizyta|Badanie)<BR>\s*</B>", html)

    # Step 4: Parse each visit section into structured data
    data = []

    for i, section in enumerate(visit_sections[1:]):  # skip the first chunk (header)
        soup = BeautifulSoup(section, "html.parser")
        text = soup.get_text(separator="\n")

        # Clean and prepare lines
        lines = [line.strip() for line in text.split("\n") if line.strip()]

        animal_line = next((l for l in lines if l.startswith("Zwierz")), None)
        if animal_line:
            match = re.search(r"Zwierz.*?:\s*(\S+)\s+Nr:\s*(\S+)", animal_line)
            animal_name = match.group(1) if match else None
            animal_id = match.group(2) if match else None
        else:
            animal_name = None
            animal_id = None

        # Extract zalecenia
        recommendations = []
        if "Zalecenia:" in lines:
            start_idx = lines.index("Zalecenia:") + 1
            while start_idx < len(lines) and not re.match(r"^\d{2}/\d{2}/\d{4} \d{2}:\d{2}:", lines[start_idx]):
                recommendations.append(lines[start_idx])
                start_idx += 1

        # Extract treatments and medications
        treatments = [l.strip() for l in lines if l.startswith("__") or l.startswith("_")]
        medications = [l.strip() for l in lines if re.match(r"^[A-Z].*\d{1,2}[.,]?\s?ml", l)]

        entry = {
            "data": visit_headers[i][0],
            "typ": visit_headers[i][1],
            "wlasciciel": next((l.split(":")[1].strip() for l in lines if "Właściciel" in l), None),
            "telefon": next((l.split(":")[1].strip() for l in lines if l.startswith("Tel.:")), None),
            "email": next((l.split(":")[1].strip() for l in lines if l.startswith("E-mail:")), None),
            "nazwa_zwierzecia": animal_name,
            "id_zwierzecia": animal_id,
            "gatunek": next((l.split(":")[1].strip() for l in lines if l.startswith("Gatunek")), None),
            "rasa": next((l.split(":")[1].strip() for l in lines if l.startswith("Rasa")), None),
            "plec": next((l.split(":")[1].strip() for l in lines if "Płeć" in l), None),
            "wiek": next((l.split(":")[1].strip() for l in lines if l.startswith("Wiek")), None),
            "microchip": next((l.split(":")[1].strip() for l in lines if l.startswith("Mikrochip")), None),
            "zabiegi": clean_multiline(treatments),
            "leki": clean_multiline(medications),
            "zalecenia": clean_multiline(recommendations)
        }

        data.append(entry)

    # Step 5: Create DataFrame
    df = pd.DataFrame(data)
    return df
    # Step 6: Write to csv
    # df.to_csv(f"/Users/danielsz/PycharmProjects/CleverDoc/{file_name}.csv", index=False, encoding="utf-8", quoting=csv.QUOTE_ALL)
