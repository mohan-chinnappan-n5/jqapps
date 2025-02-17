import streamlit as st
import requests
import os
import json
from streamlit_ace import st_ace

# Function to load credentials from access.json
def load_credentials():
    try:
        with open("access.json", "r") as file:
            credentials = json.load(file)
            return credentials.get("access_token"), credentials.get("instance_url")
    except Exception as e:
        st.error(f"Error loading access.json: {str(e)}")
        return None, None

# Function to construct API URLs dynamically
def get_api_url(instance_url, api_version, endpoint):
    return f"{instance_url}/services/data/v{api_version}/{endpoint}"

# Function to fetch the Excel report from Salesforce
def get_excel_report(access_token, instance_url, api_version, report_id):
    try:
        url = get_api_url(instance_url, api_version, f"analytics/reports/{report_id}")
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            content_disposition = response.headers.get("Content-Disposition", "")
            filename = "Salesforce_Report.xlsx"
            if "filename=" in content_disposition:
                filename = content_disposition.split("filename=")[-1].strip('"')

            file_path = os.path.join("downloads", filename)
            os.makedirs("downloads", exist_ok=True)
            with open(file_path, "wb") as file:
                file.write(response.content)

            return file_path, filename
        else:
            return None, f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"Exception: {str(e)}"

# Function to describe the report structure
def describe_report(access_token, instance_url, api_version, report_id):
    try:
        url = get_api_url(instance_url, api_version, f"analytics/reports/{report_id}/describe")
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}

# Function to get report details
def get_report_details(access_token, instance_url, api_version, report_id):
    try:
        url = get_api_url(instance_url, api_version, f"analytics/reports/{report_id}?includeDetails=true")
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}

# Function to get the list of reports
def list_reports(access_token, instance_url, api_version):
    try:
        url = get_api_url(instance_url, api_version, "analytics/reports")
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}

# Function to get the list of report types
def get_report_types(access_token, instance_url, api_version):
    try:
        url = get_api_url(instance_url, api_version, "analytics/reportTypes")
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}

# Load credentials from access.json
access_token, instance_url = load_credentials()

# Streamlit UI
st.title("📊 Salesforce Report Utility")
st.markdown("Select an option to download or analyze your Salesforce report.")

# User Inputs
api_version = st.text_input("🔄 Salesforce API Version", "60.0")
report_id = st.text_input("📄 Report ID (Required for specific operations)", "")

# Options
option = st.radio("Select an action:", [
    "List of Reports", "Download Excel", "Describe Report", 
    "Get Report Details", "Get List of Report Types"
])

if st.button("Execute"):
    if not access_token or not instance_url:
        st.warning("⚠️ Unable to read `access.json`. Ensure it contains valid credentials.")
    else:
        if option == "List of Reports":   
            reports = list_reports(access_token, instance_url, api_version)
            json_text = json.dumps(reports, indent=4)
            st.subheader("📑 List of Reports (JSON)")
            st.download_button("📥 Download JSON", json_text, "list_of_reports.json", "application/json")
            st_ace(value=json_text, language="json", theme="monokai", readonly=True)

        elif report_id:
            if option == "Download Excel":
                file_path, message = get_excel_report(access_token, instance_url, api_version, report_id)
                if file_path:
                    st.success("✅ Report generated successfully!")
                    st.download_button(
                        "📥 Download Excel Report", open(file_path, "rb"), 
                        file_name=message, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                else:
                    st.error(message)

            elif option == "Describe Report":
                description = describe_report(access_token, instance_url, api_version, report_id)
                json_text = json.dumps(description, indent=4)
                st.subheader("📑 Report Description (JSON)")
                st.download_button("📥 Download JSON", json_text, "report_description.json", "application/json")
                st_ace(value=json_text, language="json", theme="monokai", readonly=True)

            elif option == "Get Report Details":
                details = get_report_details(access_token, instance_url, api_version, report_id)
                json_text = json.dumps(details, indent=4)
                st.subheader("📊 Report Details (JSON)")
                st.download_button("📥 Download JSON", json_text, "report_details.json", "application/json")
                st_ace(value=json_text, language="json", theme="monokai", readonly=True)

        elif option == "Get List of Report Types":
            report_types = get_report_types(access_token, instance_url, api_version)
            json_text = json.dumps(report_types, indent=4)
            st.subheader("📄 List of Report Types (JSON)")
            st.download_button("📥 Download JSON", json_text, "report_types.json", "application/json")
            st_ace(value=json_text, language="json", theme="monokai", readonly=True)

        else:
            st.warning("⚠️ Report ID is required for this action.")