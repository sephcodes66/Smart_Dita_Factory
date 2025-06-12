Smart DITA Factory 🏭
Automate DITA content generation and validation with the power of AI and the DITA Open Toolkit.

This project provides a complete workflow for automatically generating DITA concept and reference topics from structured product data. It leverages the Google Gemini API for intelligent content creation and uses the official DITA Open Toolkit (DITA-OT) for robust validation, ensuring your content is compliant and high-quality. A built-in visualization dashboard helps you instantly assess the results.

✨ Key Features
Automated DITA Generation: Creates DITA concept and reference topics from a simple product_specs.csv file (contains synthetic data).
AI-Powered Content: Integrates with the Google Gemini API to generate descriptive content.
Robust Validation: Uses the industry-standard DITA Open Toolkit (DITA-OT) for accurate and reliable validation.
Quality Reporting: Generates a quality_report.csv file with detailed validation status and error messages for each generated topic.
Interactive Dashboard: Includes a Streamlit-based web app to visualize the quality report, making it easy to see passes, failures, and overall trends.
📂 Project Structure
Here is the recommended directory structure for the project to function correctly:

.
├── assets/
│   └── dashboard_screenshot.png  # Your dashboard image
├── dita-ot-4.3.2/              # DITA Open Toolkit directory
├── dtds/                         # DITA DTD files for reference
├── dita_output/                  # Generated DITA files will appear here
├── report/                       # The quality report CSV will be saved here
├── .gitignore                    # Standard Python gitignore
├── product_specs.csv             # Your input data file
├── smart_dita_factory.py         # Main script for generation and validation
├── visualize_output.py           # Script to launch the visualization dashboard
└── requirements.txt              # Python package dependencies
🚀 Getting Started
Follow these steps to set up and run the project on your local machine.

1. Prerequisites
Python 3.8+
DITA Open Toolkit: This project requires a local installation of the DITA-OT.
Download the DITA Open Toolkit (the script is configured for version 4.3.2, but you can adjust the path).
Unzip the folder and place it in the project's root directory.
Google Gemini API Key: The script uses the Gemini API for content generation.
Get a Gemini API key.
2. Installation & Setup
Step 1: Clone the Repository

Bash

git clone https://github.com/your-username/smart-dita-factory.git
cd smart-dita-factory
Step 2: Create a Virtual Environment (Recommended)

Bash

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

# For Windows
python -m venv venv
venv\Scripts\activate
Step 3: Install Python Dependencies
Create a requirements.txt file with the following content:

Plaintext

pandas
google-generativeai
lxml
streamlit
Then, install the packages:

Bash

pip install -r requirements.txt
Step 4: Set Up Your API Key
Set your Google Gemini API key as an environment variable. This is a secure way to handle your credentials.

Bash

# For macOS/Linux
export GEMINI_API_KEY="YOUR_API_KEY_HERE"

# For Windows
set GEMINI_API_KEY="YOUR_API_KEY_HERE"
Alternatively, you can hardcode the key in smart_dita_factory.py, but this is not recommended for security reasons.

Step 5: Verify DITA-OT Path
Open smart_dita_factory.py and ensure the DITA_OT_DIR variable matches the name of your DITA Open Toolkit folder.

Python

# In smart_dita_factory.py
DITA_OT_DIR = "dita-ot-4.3.2" # Update this to your DITA-OT path
⚙️ How to Run
1. Prepare Your Input Data
Create or modify the product_specs.csv file in the root directory. It should contain the product data you want to convert into DITA topics. The script expects the following columns:

ProductID	ProductName	Description	FeatureA	FeatureB
101	Quantum Drive	An ultra-fast solid-state drive...	1TB Storage	5-Year-Warranty
102	Photon Processor	A next-generation CPU with AI cores...	16 Cores	Low Power
103	LogicBoard X	A versatile motherboard for creators...	ATX Form-Factor	RGB Lighting

Export to Sheets
2. Generate and Validate DITA Files
Run the main script from your terminal. It will read the CSV, generate all DITA files, validate them, and create the quality report.

Bash

python smart_dita_factory.py
3. Visualize the Results
After the main script finishes, launch the Streamlit dashboard to see the results.

Bash

streamlit run visualize_output.py
This will open a new tab in your web browser with the interactive quality report.

📊 Understanding the Output
dita_output/: This folder will contain the generated DITA files, such as con_101.dita and ref_101.dita.
report/quality_report.csv: A CSV log detailing the validation status (PASS/FAIL), file path, and any error messages for each generated file.
Streamlit Dashboard: The web dashboard provides:
A full report table.
A filtered table showing only the passed topics.
A bar chart summarizing the number of passes and failures.
🔧 How It Works
Data Ingestion: The smart_dita_factory.py script starts by reading the product_specs.csv into a Pandas DataFrame.
DITA Generation: For each row in the DataFrame, it generates two DITA files:
A <concept> topic using the product Description.
A <reference> topic with a <properties> table built from the other product features.
The lxml library is used to construct the XML structure programmatically.
Validation: The script calls the DITA-OT command-line tool using a Python subprocess. This provides a highly accurate validation against the official DITA standard, which is more robust than DTD validation alone.
Reporting & Visualization: The results are compiled into quality_report.csv. The visualize_output.py script then uses Streamlit to create a simple but effective web-based dashboard from this report.

📜 License
No License.