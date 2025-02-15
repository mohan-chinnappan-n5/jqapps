import streamlit as st
import json
import pandas as pd
from streamlit_ace import st_ace

# Page Configuration           
st.set_page_config(page_title="Salesforce Report Viewer", layout="wide")

st.title("🔍 Salesforce Report Viewer")

# File Upload
uploaded_file = st.sidebar.file_uploader("Upload Salesforce Report JSON", type=["json"])

if uploaded_file:
    # Load JSON Data
    data = json.load(uploaded_file)

    # Extract Report Name
    report_name = data.get("attributes", {}).get("reportName", "Unknown Report")
    st.subheader(f"📑 Report: {report_name}")

    # Extract Column Headers
    detail_columns = data.get("reportMetadata", {}).get("detailColumns", [])

    # Display JSON Data in Ace Editor
    json_text = json.dumps(data, indent=2)
    st_ace(value=json_text, language="json", theme="monokai", height=400, readonly=True)

    if not detail_columns:
        st.error("No column headers found in reportMetadata.")
    else:
        # Extract factMap data
        fact_map = data.get("factMap", {})

        # Process Data for Table
        table_data = []
        aggregate_data = []
        aggregate_headers = set()  # Track aggregate column headers

        for key, section in fact_map.items():
            # Extract row data
            rows = section.get("rows", [])
            for row in rows:
                row_data = [cell.get("label", "-") for cell in row["dataCells"]]
                table_data.append(row_data)

            # Extract aggregate data if available
            aggregates = section.get("aggregates", [])
            if aggregates:
                agg_row = {"Section": key}  # Start with section key
                for idx, agg in enumerate(aggregates):
                    column_name = f"Aggregate {idx+1}"  # Dynamic column names
                    agg_row[column_name] = agg.get("label", "N/A")
                    aggregate_headers.add(column_name)  # Store column names
                aggregate_data.append(agg_row)

        # Display Row-Level Data
        if table_data:
            df = pd.DataFrame(table_data, columns=detail_columns)
            st.subheader("📊 Report Data")
            st.dataframe(df)
        else:
            st.warning("No row-level data found in the report.")

        # Display Aggregates Data
        if aggregate_data:
            st.subheader("📈 Aggregate Data")
            agg_columns = ["Section"] + sorted(list(aggregate_headers))  # Ensure consistent column order
            agg_df = pd.DataFrame(aggregate_data).fillna("N/A")[agg_columns]  # Fill missing values
            st.dataframe(agg_df)
        else:
            st.info("No aggregate data found.")