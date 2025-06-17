import os
import pandas as pd
import google.generativeai as genai
from lxml import etree
import time
import subprocess
import sys

# Note: To get a key, visit https://makersuite.google.com/app/apikey
# Note: add your key to the environment variable GEMINI_API_KEY or edit the script to add your key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# File and Directory Paths
PRODUCT_SPECS_CSV = "product_specs.csv"
OUTPUT_DIR_DITA = "dita_output"
OUTPUT_DIR_REPORT = "report"
QUALITY_REPORT_CSV = os.path.join(OUTPUT_DIR_REPORT, "quality_report.csv")

DTD_PATH = "dtds/dtd/technicalContent/dtd/reference.dtd"
CONCEPT_DTD_PATH = "dtds/dtd/technicalContent/dtd/concept.dtd"

# Note: Download DITA-OT from https://www.dita-ot.org/ and move it into the root directory of the project
DITA_OT_DIR = "dita-ot-4.3.2" # Update this to your DITA-OT path

def configure_gemini_api():
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print("Gemini API configured successfully.")
        return True
    except Exception as e:
        print(f"Error configuring Gemini API: {e}")
        print("Please ensure your GEMINI_API_KEY is set correctly.")
        return False

def dita_ot_validate(dita_file, dita_ot_dir):
    dita_cmd = os.path.join(dita_ot_dir, "bin", "dita")
    if not os.path.exists(dita_cmd):
        return "FAIL", f"DITA-OT executable not found at {dita_cmd}"
    if not os.path.exists(dita_file):
        return "FAIL", f"DITA file not found: {dita_file}"
    try:
        result = subprocess.run(
            [dita_cmd, "validate", "-i", dita_file],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        if result.returncode == 0:
            return "PASS", result.stdout.strip()
        else:
            return "FAIL", result.stderr.strip() or result.stdout.strip()
    except Exception as e:
        return "FAIL", str(e)

# --- PHASE 1: GENERATE REFERENCE DITA ---

def generate_reference_dita(product, output_dir):
    """Generates a DITA <reference> topic from product data."""
    product_id = product['ProductID']
    product_name = product['ProductName']

    root = etree.Element('reference')
    root.set('id', product_id)

    relative_dtd_path = f"../{DTD_PATH.replace(os.path.sep, '/')}"
    doctype = f'<!DOCTYPE reference PUBLIC "-//OASIS//DTD DITA Reference//EN" "{relative_dtd_path}">'

    title = etree.SubElement(root, 'title')
    title.text = f"Technical Specifications for {product_name}"

    refbody = etree.SubElement(root, 'refbody')
    properties = etree.SubElement(refbody, 'properties')

    for key, value in product.items():
        if key not in ['ProductID', 'ProductName']:
            property_elem = etree.SubElement(properties, 'property')
            proptype = etree.SubElement(property_elem, 'proptype')
            proptype.text = str(key)
            propvalue = etree.SubElement(property_elem, 'propvalue')
            propvalue.text = str(value)

    tree = etree.ElementTree(root)
    file_path = os.path.join(output_dir, f"{product_id}_reference.dita")

    with open(file_path, 'wb') as f:
        f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8', doctype=doctype))

    print(f"Generated DITA reference for {product_id}.")
    return file_path


# --- PHASE 2: GENERATE CONCEPT DITA WITH GEMINI API (with intentional errors) ---

def generate_concept_dita(product, output_dir):
    """Generates a DITA <concept> topic, intentionally failing for some products."""
    product_id = product['ProductID']
    product_name = product['ProductName']
    file_path = os.path.join(output_dir, f"{product_id}_concept.dita")
    
    # *** REVISED MODIFICATION: Handle error cases separately ***
    if product_id in ['A-50', 'F-800']:
        print(f"Intentionally generating a broken DITA file for product {product_id}.")
        
        relative_dtd_path = f"../{CONCEPT_DTD_PATH.replace(os.path.sep, '/')}"
        doctype = f'<!DOCTYPE concept PUBLIC "-//OASIS//DTD DITA Concept//EN" "{relative_dtd_path}">'
        
        # Intentionally generate a broken DITA file with an unclosed tag
        raw_dita_content = f'''<?xml version="1.0" encoding="UTF-8"?>
        {doctype}
        <concept id="{product_id}_summary">
        <title>About the {product_name}</title>
        <conbody>
        <p>This is some content with an <b>unclosed tag that will cause a validation failure.
        </p>
        </conbody>
        </concept>'''
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(raw_dita_content)
        
        print(f"Generated intentionally broken AI concept for {product_id}.")
        return file_path
    
    prompt = f"""
    Based on the following technical specifications for the product '{product_name}', please write a user-friendly and engaging summary for a non-technical audience.
    The summary should be enclosed in a single <p> tag.

    Specifications:
    {product.to_string()}

    Example Output:
    <p>Discover the {product_name}, a revolutionary device designed for modern needs. It operates on a standard voltage of {product.get('Voltage', 'N/A')} and reaches an impressive maximum speed of {product.get('MaxSpeed', 'N/A')}, making it both powerful and efficient. Perfect for enthusiasts and professionals alike!</p>
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt)
        ai_content = response.text.strip()

        if not ai_content.startswith('<p>'):
            ai_content = f'<p>{ai_content}</p>'
        
        ai_paragraph_element = etree.fromstring(ai_content)
            
    except Exception as e:
        print(f"Error during generation for {product_id}: {e}")
        ai_paragraph_element = etree.Element('p')
        ai_paragraph_element.text = f"An AI-generated summary for the {product_name} could not be created at this time due to an error."

    root = etree.Element('concept')
    root.set('id', f"{product_id}_summary")

    relative_dtd_path = f"../{CONCEPT_DTD_PATH.replace(os.path.sep, '/')}"
    doctype = f'<!DOCTYPE concept PUBLIC "-//OASIS//DTD DITA Concept//EN" "{relative_dtd_path}">'

    title = etree.SubElement(root, 'title')
    title.text = f"About the {product_name}"

    conbody = etree.SubElement(root, 'conbody')
    conbody.append(ai_paragraph_element)

    tree = etree.ElementTree(root)

    with open(file_path, 'wb') as f:
        f.write(etree.tostring(tree, pretty_print=True, xml_declaration=True, encoding='UTF-8', doctype=doctype))
        
    print(f"Generated AI concept for {product_id}.")
    return file_path


def main():
    print("--- Starting Smart DITA Factory ---")

    if not os.path.exists(OUTPUT_DIR_DITA):
        os.makedirs(OUTPUT_DIR_DITA)
    if not os.path.exists(OUTPUT_DIR_REPORT):
        os.makedirs(OUTPUT_DIR_REPORT)

    if not GEMINI_API_KEY or "YOUR_GEMINI_API_KEY" in GEMINI_API_KEY:
        print("\nERROR: Gemini API Key is not set. Please set the GEMINI_API_KEY environment variable.")
        return

    if not configure_gemini_api():
        return

    try:
        products_df = pd.read_csv(PRODUCT_SPECS_CSV)
    except FileNotFoundError:
        print(f"\nERROR: The file '{PRODUCT_SPECS_CSV}' was not found.")
        print("Please create it in the same directory as the script.")
        return

    audit_results = []
    print(f"\nFound {len(products_df)} products. Starting generation and validation...")

    for index, product in products_df.iterrows():
        product_id = product['ProductID']
        print(f"\n--- Processing Product: {product_id} ---")

        # Generate and validate Reference DITA
        ref_file_path = generate_reference_dita(product, OUTPUT_DIR_DITA)
        status, error = dita_ot_validate(ref_file_path, DITA_OT_DIR)
        audit_results.append({
            'ProductID': product_id,
            'DITAType': 'Reference',
            'FilePath': ref_file_path,
            'ValidationStatus': status,
            'ErrorMessage': error
        })
        print(f"Validation for {os.path.basename(ref_file_path)}: {status}")

        time.sleep(1) 
        
        # Generate and validate Concept DITA
        concept_file_path = generate_concept_dita(product, OUTPUT_DIR_DITA)
        status, error = dita_ot_validate(concept_file_path, DITA_OT_DIR)
        audit_results.append({
            'ProductID': product_id,
            'DITAType': 'Concept',
            'FilePath': concept_file_path,
            'ValidationStatus': status,
            'ErrorMessage': error
        })
        print(f"Validation for {os.path.basename(concept_file_path)}: {status}")

    print("\n--- Generating Quality Report ---")
    report_df = pd.DataFrame(audit_results)
    report_df.to_csv(QUALITY_REPORT_CSV, index=False)
    print(f"Successfully generated quality report: {QUALITY_REPORT_CSV}")

    print("\n--- Smart DITA Factory Finished ---")
    print("The output .csv file is saved to the 'report' folder. Use 'streamlit run visualize_output.py' (or the improved version) to visualize the results.")

if __name__ == "__main__":
    main()