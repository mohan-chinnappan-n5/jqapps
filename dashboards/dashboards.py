import streamlit as st
import requests
import json
from streamlit_ace import st_ace

# Function to list dashboards
def list_dashboards(access_token, instance_url):
    url = f"{instance_url}/services/data/v60.0/analytics/dashboards"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else {"error": response.text}

# Function to get dashboard results
def get_dashboard_results(access_token, instance_url, dashboard_id):
    url = f"{instance_url}/services/data/v60.0/analytics/dashboards/{dashboard_id}"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else {"error": response.text}

# Function to get dashboard metadata
def get_dashboard_metadata(access_token, instance_url, dashboard_id):
    url = f"{instance_url}/services/data/v60.0/analytics/dashboards/{dashboard_id}/describe"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json() if response.status_code == 200 else {"error": response.text}

# Function to download dashboard as PNG
def download_dashboard_png(access_token, instance_url, dashboard_id):
    url = f"{instance_url}/analytics/download/lightning-dashboard/{dashboard_id}.png"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers, stream=True)

    if response.status_code == 200:
        return response.content  # Binary content for PNG
    else:
        return {"error": f"Error: {response.status_code} - {response.text}"}

# Streamlit UI
st.title("📊 Salesforce Dashboard Utility")
st.markdown("Manage Salesforce Dashboards: List, Get Results, Metadata, and Download as PNG.")

# User Inputs
access_token = st.text_input("🔑 Access Token", type="password")
instance_url = st.text_input("🌐 Instance URL", value="https://your-instance.salesforce.com")

# Options
option = st.radio("Select an action:", [
    "List All Dashboards",
    "Get Dashboard Results",
    "Get Dashboard Metadata"
])

if option != "List All Dashboards":
    dashboard_id = st.text_input("📊 Dashboard ID", "")

if st.button("Execute"):
    if access_token and instance_url:
        if option == "List All Dashboards":
            dashboards = list_dashboards(access_token, instance_url)

            # Display JSON
            st.subheader("📋 List of Dashboards (JSON)")
            json_text = json.dumps(dashboards, indent=4)
             # JSON Download
            st.download_button(
                label="📥 Download JSON",
                data=json_text,
                file_name="list_of_dashboards.json",
                mime="application/json"
            )
            st_ace(value=json_text, language="json", theme="monokai", readonly=True)

           

        elif dashboard_id:
            if option == "Get Dashboard Results":
                results = get_dashboard_results(access_token, instance_url, dashboard_id)

                # Display JSON
                st.subheader("📊 Dashboard Results (JSON)")
                json_text = json.dumps(results, indent=4)

                # JSON Download
                st.download_button(
                    label="📥 Download JSON",
                    data=json_text,
                    file_name="dashboard_results.json",
                    mime="application/json"
                )
                st_ace(value=json_text, language="json", theme="monokai", readonly=True)


            elif option == "Get Dashboard Metadata":
                metadata = get_dashboard_metadata(access_token, instance_url, dashboard_id)

                # Display JSON
                st.subheader("📑 Dashboard Metadata (JSON)")
                json_text = json.dumps(metadata, indent=4)

                # JSON Download
                st.download_button(
                    label="📥 Download JSON",
                    data=json_text,
                    file_name="dashboard_metadata.json",
                    mime="application/json"
                )
                st_ace(value=json_text, language="json", theme="monokai", readonly=True)


            elif option == "Download Dashboard as PNG":
                png_data = download_dashboard_png(access_token, instance_url, dashboard_id)

                if isinstance(png_data, dict) and "error" in png_data:
                    st.error(png_data["error"])
                else:
                    st.subheader("📸 Dashboard PNG Preview")
                    st.image(png_data, caption="Downloaded Dashboard")

                    # PNG Download
                    st.download_button(
                        label="📥 Download PNG",
                        data=png_data,
                        file_name=f"dashboard_{dashboard_id}.png",
                        mime="image/png"
                    )
        else:
            st.warning("⚠️ Please enter a valid Dashboard ID.")
    else:
        st.warning("⚠️ Please enter Access Token and Instance URL.")