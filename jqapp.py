import streamlit as st
import json
import jq
from streamlit_ace import st_ace

# Page Configuration
st.set_page_config(page_title="JSON Query using JQ", layout="wide")

st.title("🔍 JSON Query with JQ")

# Sample JQ Selectors
sample_selectors = [
    '.factMap."15!T"',
    '.factMap."15!T".rows[].dataCells[0].label',
    '.reportMetadata.detailColumns',
    '.factMap."15!T".aggregates',
]

HEIGHT = 300

# Sidebar - Upload JSON
st.sidebar.header("📂 Upload JSON File")
uploaded_file = st.sidebar.file_uploader("Choose a JSON file", type=["json"])

# Load JSON Data
json_data = {}
if uploaded_file is not None:
    json_data = json.load(uploaded_file)

# Left Panel - JSON Editor
st.subheader("📜 JSON Input")
json_input = st_ace(
    value=json.dumps(json_data, indent=2),
    language="json",
    theme="monokai",
    height=HEIGHT
)

# Dropdown for sample selectors
selected_jq = st.selectbox("📌 Choose a Sample Selector", sample_selectors)

# Manual JQ Input
jq_query = st.text_input("✏️ Or enter JQ manually", value=selected_jq)

# JQ Query Input
#jq_query = st.text_input("Enter jq expression:", '.factMap."15!T".aggregates')  # Default jq filter is `.`
#st.caption("Example: `.skills[]`, `.age`, `{name, age}`")

# Process JSON with jq
try:
    json_obj = json.loads(json_input)  # Convert Editor Text to JSON
    result = jq.compile(jq_query).input(json_obj).all()  # Run JQ Query
    output_json = json.dumps(result, indent=2)
except Exception as e:
    output_json = f"Error: {str(e)}"

# Right Panel - JSON Output
st.subheader("📤 JQ Output")
st_ace(
    value=output_json,
    language="json",
    theme="monokai",
    height=HEIGHT,
    readonly=True

)