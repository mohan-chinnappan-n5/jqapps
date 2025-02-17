import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

def load_json(file):
    """Load JSON data from the uploaded file."""
    return json.load(file)

def parse_factmap(fact_map, column_names, aggregate_names):
    """Extract report details from the factMap."""
    grouped_data = {}
    
    for key, section in fact_map.items():
        group_name = key.replace("!T", "")  # Extract grouping key
        aggregates = {aggregate_names[i]: agg.get("value", 0) for i, agg in enumerate(section.get("aggregates", []))}
        
        rows = []
        for row in section.get("rows", []):
            row_data = [cell.get("label", "-") for cell in row["dataCells"]]
            rows.append(row_data)
        
        grouped_data[group_name] = {
            "aggregates": aggregates,
            "rows": rows,
            "columns": column_names
        }
    
    return grouped_data

def display_grouped_data(grouped_data):
    """Render each report group as a table."""
    for group, data in grouped_data.items():
        st.subheader(f"Group: {group}")
        
        if data["rows"]:
            df = pd.DataFrame(data["rows"], columns=data["columns"])
            st.dataframe(df)
        
        st.write("### Aggregates")
        st.json(data["aggregates"])

def plot_chart(grouped_data):
    """Generate a bar chart from aggregates."""
    for group, data in grouped_data.items():
        fig, ax = plt.subplots()
        ax.bar(data["aggregates"].keys(), data["aggregates"].values(), color='skyblue')
        ax.set_xlabel("Aggregate Metrics")
        ax.set_ylabel("Values")
        ax.set_title(f"Summary Report Chart - Group: {group}")
        ax.set_xticklabels(data["aggregates"].keys(), rotation=30, ha='right')
        ax.grid(True, linestyle='--', alpha=0.7)
        st.pyplot(fig)

# Streamlit UI
st.title("📊 Salesforce Summary Report Viewer")

uploaded_file = st.file_uploader("Upload JSON Report File", type=["json"])

if uploaded_file:
    data = load_json(uploaded_file)
    fact_map = data.get("factMap", {})
    column_names = data.get("reportMetadata", {}).get("detailColumns", [])
    aggregate_names = data.get("reportMetadata", {}).get("aggregates", [])
    
    if fact_map:
        grouped_data = parse_factmap(fact_map, column_names, aggregate_names)
        display_grouped_data(grouped_data)
        plot_chart(grouped_data)
    else:
        st.error("Invalid report format. No factMap found.")
