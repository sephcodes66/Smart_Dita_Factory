import streamlit as st
import pandas as pd
import plotly.express as px

def create_improved_dashboard():
    st.set_page_config(page_title="DITA Quality Dashboard", layout="wide")

    try:
        df = pd.read_csv('report/quality_report.csv')
    except FileNotFoundError:
        st.error("The 'quality_report.csv' file was not found. Please run the main factory script first.")
        return

    st.title("Interactive DITA Quality Dashboard")
    st.markdown("Analyze the results of the DITA generation and validation process.")

    # --- Sidebar Filters ---
    st.sidebar.header("Filter Options")
    
    # --- Filter by Validation Status ---
    selected_status = st.sidebar.multiselect(
        "Validation Status",
        options=df['ValidationStatus'].unique(),
        default=df['ValidationStatus'].unique()
    )

    # --- Filter by DITA Type ---
    selected_type = st.sidebar.multiselect(
        "DITA Type",
        options=df['DITAType'].unique(),
        default=df['DITAType'].unique()
    )

    # --- Filter by Product ID ---
    selected_product_id = st.sidebar.multiselect(
        "Product ID",
        options=df['ProductID'].unique(),
        default=df['ProductID'].unique()
    )
    
    # --- Apply filters to the dataframe ---
    filtered_df = df[
        (df['ValidationStatus'].isin(selected_status)) &
        (df['DITAType'].isin(selected_type)) &
        (df['ProductID'].isin(selected_product_id))
    ]

    # --- High-Level KPI Metrics ---
    st.header("Overall Quality Metrics")
    total_files = len(df)
    passed_files = len(df[df['ValidationStatus'] == 'PASS'])
    failed_files = total_files - passed_files
    pass_rate = (passed_files / total_files * 100) if total_files > 0 else 0

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Files Generated", f"{total_files}")
    col2.metric("Pass Rate", f"{pass_rate:.2f}%")
    col3.metric("Passed Files", f"{passed_files}")
    col4.metric("Failed Files", f"{failed_files}")
    st.divider()

    # --- Charts and Visuals ---
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # --- Pie chart for Pass/Fail distribution ---
        status_counts = df['ValidationStatus'].value_counts().reset_index()
        status_counts.columns = ['Status', 'Count']
        fig_pie = px.pie(
            status_counts, 
            names='Status', 
            values='Count', 
            title='Overall Validation Status',
            color='Status',
            color_discrete_map={'PASS': 'green', 'FAIL': 'red'}
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with chart_col2:
        # --- Bar chart for failures by DITA type ---
        failures_by_type = df[df['ValidationStatus'] == 'FAIL']['DITAType'].value_counts().reset_index()
        failures_by_type.columns = ['DITAType', 'Count']
        fig_bar = px.bar(
            failures_by_type,
            x='DITAType',
            y='Count',
            title='Failures by DITA Type',
            labels={'Count': 'Number of Failed Files'},
            color='DITAType'
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    st.divider()

    # --- Data View & Error Analysis ---
    st.info(f"Showing {len(filtered_df)} of {len(df)} total files based on filters.")
    st.dataframe(filtered_df)

    # --- Section for analyzing failures ---        
    failed_data = filtered_df[filtered_df['ValidationStatus'] == 'FAIL']
    if not failed_data.empty:
        st.subheader("Failure Analysis")
        for index, row in failed_data.iterrows():
            with st.expander(f"**FAIL:** {row['FilePath']}"):
                st.write(f"**Product ID:** {row['ProductID']}")
                st.write(f"**DITA Type:** {row['DITAType']}")
                st.write("**Error Message:**")
                st.error(row['ErrorMessage'] or "No error message captured.")

if __name__ == "__main__":
    create_improved_dashboard()