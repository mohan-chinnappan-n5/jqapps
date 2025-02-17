import streamlit as st
import json
import pandas as pd
import matplotlib.pyplot as plt

def load_json(file):
    """Load JSON data from the uploaded file."""
    return json.load(file)

def parse_factmap(fact_map, column_names):
    """Extract report details from the factMap."""
    grouped_data = {}
    
    for key, section in fact_map.items():
        group_name = key.replace("!T", "")  # Extract grouping key
        aggregates = [agg.get("value", 0) for agg in section.get("aggregates", [])]
        
        rows = []
        for row in section.get("rows", []):
            row_data = [cell.get("value", "-") for cell in row["dataCells"]]
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
        st.write(data["aggregates"])

def plot_chart(grouped_data):
    """Generate a bar chart from aggregates."""
    group_labels = list(grouped_data.keys())
    aggregate_values = [sum(data["aggregates"]) for data in grouped_data.values()]
    
    fig, ax = plt.subplots()
    ax.bar(group_labels, aggregate_values, color='skyblue')
    ax.set_xlabel("Groups")
    ax.set_ylabel("Aggregate Values")
    ax.set_title("Summary Report Chart")
    st.pyplot(fig)

# Streamlit UI
st.title("📊 Salesforce Summary Report Viewer")

uploaded_file = st.file_uploader("Upload JSON Report File", type=["json"])

if uploaded_file:
    data = load_json(uploaded_file)
    fact_map = data.get("factMap", {})
    column_names = data.get("reportMetadata", {}).get("detailColumns", [])
    
    if fact_map:
        grouped_data = parse_factmap(fact_map, column_names)
        display_grouped_data(grouped_data)
        plot_chart(grouped_data)
    else:
        st.error("Invalid report format. No factMap found.")
