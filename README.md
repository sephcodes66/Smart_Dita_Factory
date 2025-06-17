# Smart DITA Factory 
## Automate DITA content generation and validation with the power of AI and the DITA Open Toolkit

This project provides a complete workflow for automatically generating DITA concept and reference topics from structured product data. It leverages the Google Gemini API for intelligent content creation and uses the official DITA Open Toolkit (DITA-OT) for robust validation. The results are displayed in a rich, interactive dashboard that makes it easy to assess content quality instantly.

## Output Visualizations

![Dashboard Screenshot](https://github.com/sephcodes66/Smart_Dita_Factory/raw/main/assets/dashboard_ss1.png)
![Dashboard Screenshot](https://github.com/sephcodes66/Smart_Dita_Factory/raw/main/assets/dashboard_ss2.png)

## Key Features
- Automated DITA Generation: Creates DITA <concept> and <reference> topics from a simple product_specs.csv file.
- AI-Powered Content: Integrates with the Google Gemini API to generate descriptive, human-friendly content for concept topics.
- Robust Validation: Uses the industry-standard DITA Open Toolkit (DITA-OT) for accurate and reliable validation against official DITA standards.
- Quality Reporting: Generates a quality_report.csv file with detailed validation status (PASS/FAIL) and error messages for each generated topic.
- Advanced Interactive Dashboard: Includes a Streamlit-based web app (visualize_output_improved.py) with interactive filters, KPI metrics, and Plotly charts to visually analyze the quality report.


## Table of Contents
1. Prerequisites
2. Installation and Setup
3. How It Works
4. References

### 1. Prerequisites
- Python 3.8+
- DITA Open Toolkit: This project requires a local installation of the DITA-OT.
    - Download the DITA Open Toolkit (the script is configured for version 4.3.2, but you can adjust the path).
    - Unzip the folder and place it in the project's root directory.
- Google Gemini API Key: The script uses the Gemini API for content generation.
    - Get a Gemini API key.


### 2. Installation and Setup
1. Clone the Repository

    ```bash
    git clone https://github.com/your-username/smart-dita-factory.git
    cd smart-dita-factory
    ```

2. Create a Virtual Environment (Recommended)
    * **macOS/Linux**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    * **Windows**
        ```bash
        python -m venv venv
        venv\Scripts\activate
        ```
3. Install Python Dependencies

    ```bash
    pip install -r requirements.txt
    ```

4. Set Up Your API Key
    - Set your Google Gemini API key as an environment variable.
        - Windows
        ```bash
        set GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```

        - macOS/Linux
        ```bash
        export GEMINI_API_KEY="YOUR_API_KEY_HERE"
        ```

5. Verify DITA-OT Path
    - Open smart_dita_factory.py and ensure the DITA_OT_DIR variable matches the name of your DITA Open Toolkit folder.

6. Run the Factory Script
    ```bash
    python smart_dita_factory.py
    ```

7. Run the Visualization App
    ```bash
    streamlit run visualize_output.py
    ```
    - This will open a new tab in your web browser with the interactive quality report.

### 3. How It Works
- Data Ingestion: The smart_dita_factory.py script starts by reading the product_specs.csv into a Pandas DataFrame.
- DITA Generation: For each row in the DataFrame, it generates two DITA files:
    - A <concept> topic using the product Description.
    - A <reference> topic with a <properties> table built from the other product features.
    - The lxml library is used to construct the XML structure programmatically.
- Validation: The script calls the DITA-OT command-line tool using a Python subprocess. This provides a highly accurate validation against the official DITA standard.
- Reporting & Visualization: The results are compiled into quality_report.csv. The visualize_output.py script then uses Streamlit to create a web-based dashboard from this report. You can see an example screenshot at assets/dashboard_screenshot.png.

### 4. References
- [DITA (Darwin Information Typing Architecture): OASIS DITA Standard](https://www.oasis-open.org/committees/tc_home.php?wg_abbrev=dita)
- [DITA Open Toolkit](dita-ot.org)(https://www.dita-ot.org)
- [Google Gemini API: Google AI for Developers](https://ai.google.dev)
- [Python: python.org](https://www.python.org)
- [Streamlit: streamlit.io](https://streamlit.io)
- [Pandas: pandas.pydata.org](https://pandas.pydata.org)
- [lxml: lxml.de (Homepage link from PyPI)](https://lxml.de)