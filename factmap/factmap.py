import streamlit as st
import requests
import json
import pandas as pd
from streamlit_ace import st_ace

# Function to fetch report data from Salesforce
def get_report_data(access_token, instance_url, report_id, api_version="60.0"):
    url = f"{instance_url}/services/data/v{api_version}/analytics/reports/{report_id}?includeDetails=true"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else {"error": response.text}

# Function to parse Fact Map and structure it as a DataFrame
def parse_fact_map(fact_map, detail_columns, report_format):
    data_rows = []

    if report_format == "TABULAR":
        for key, section in fact_map.items():
            for row in section.get("rows", []):
                row_data = {detail_columns[i]: cell.get("value", "-") for i, cell in enumerate(row["dataCells"])}
                data_rows.append(row_data)

    elif report_format in ["SUMMARY", "MATRIX"]:
        for key, section in fact_map.items():
            if key.endswith("!T"):  # Summary Data
                row_data = {"Grouping": key.replace("!T", ""), "Aggregates": section["aggregates"]}
                data_rows.append(row_data)

    return pd.DataFrame(data_rows) if data_rows else None

# Streamlit UI
st.title("📊 Salesforce Report Viewer")
st.markdown("Enter your credentials to fetch and visualize reports.")

# User Inputs
access_token = st.text_input("🔑 Access Token", type="password")
instance_url = st.text_input("🌐 Instance URL", "https://your-instance.salesforce.com")
report_id = st.text_input("📄 Report ID", "")

if st.button("Fetch Report Data"):
    if access_token and instance_url and report_id:
        data = get_report_data(access_token, instance_url, report_id)

        if "error" in data:
            st.error(f"⚠️ Error: {data['error']}")
        else:
            st.success("✅ Report data fetched successfully!")

            # Display JSON data
            json_text = json.dumps(data, indent=4)
            st_ace(value=json_text, language="json", theme="monokai", readonly=True)

            # Extract Fact Map Data
            fact_map = data.get("factMap", {})
            detail_columns = data.get("reportMetadata", {}).get("detailColumns", [])
            report_format = data.get("reportMetadata", {}).get("reportFormat", "UNKNOWN")

            st.subheader(f"🔹 Report Type: {report_format}")

            # Parse Fact Map into DataFrame
            df = parse_fact_map(fact_map, detail_columns, report_format)

            if df is not None:
                st.dataframe(df)  # Render as a table
            else:
                st.warning("⚠️ No report data available for rendering.")
    else:
        st.warning("⚠️ Please enter all required fields.")