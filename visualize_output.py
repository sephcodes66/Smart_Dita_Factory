import streamlit as st
import pandas as pd

def visualize_output():
    df = pd.read_csv('report/quality_report.csv')
    st.title("DITA Quality Report")
    st.dataframe(df)

    pass_df = df[df['ValidationStatus'] == 'PASS']
    st.subheader("Passes")
    st.dataframe(pass_df)

    st.bar_chart(df['ValidationStatus'].value_counts())

if __name__ == "__main__":
    visualize_output() 
    print("Visualization complete")