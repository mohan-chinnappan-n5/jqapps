import streamlit as st
import requests
import os
import json
from streamlit_ace import st_ace

# Function to fetch the Excel report from Salesforce
def get_excel_report(access_token, instance_url, report_id):
    try:
        url = f"{instance_url}/services/data/v60.0/analytics/reports/{report_id}"
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
def describe_report(access_token, instance_url, report_id):
    try:
        url = f"{instance_url}/services/data/v60.0/analytics/reports/{report_id}/describe"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}

# Function to get report details (all records)
def get_report_details(access_token, instance_url, report_id):
    try:
        url = f"{instance_url}/services/data/v60.0/analytics/reports/{report_id}?includeDetails=true"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}


# Function to get the list of reports
def list_reports(access_token, instance_url):
    try:
        url = f"{instance_url}/services/data/v60.0/analytics/reports"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}

# Function to get the list of report types
def get_report_types(access_token, instance_url):
    try:
        url = f"{instance_url}/services/data/v60.0/analytics/reportTypes"
        headers = {"Authorization": f"Bearer {access_token}"}

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"Error: {response.status_code} - {response.text}"}
    except Exception as e:
        return {"error": str(e)}
    

# Streamlit UI
st.title("📊 Salesforce Report Utility")
st.markdown("Enter the required details to download or analyze your report.")

# User Inputs
access_token = st.text_input("🔑 Access Token", type="password")
instance_url = st.text_input("🌐 Instance URL", value="https://your-instance.salesforce.com")
report_id = st.text_input("📄 Report ID : 00Oxxxx")

# Options
option = st.radio("Select an action:", ["List of Reports", "Download Excel", "Describe Report", "Get Report Details", "Get List of Report Types"])

if st.button("Execute"):
    if access_token and instance_url :
        if option == "List of Reports":   
            list_of_reports = list_reports(access_token, instance_url)

            # Display JSON with streamlit_ace
            st.subheader("📑 List of Reports(JSON)")
            json_text = json.dumps(list_of_reports, indent=4)
            # Provide JSON download button
            json_filename = "list_of_reports.json"
            st.download_button(
                label="📥 Download JSON",
                data=json_text,
                file_name=json_filename,
                mime="application/json"
            )
            st_ace(value=json_text, language="json", theme="monokai", readonly=True)
    else :
        st.warning("⚠️ Please enter Access Token and Instance URL.")

            

    if access_token and instance_url and report_id and option != "List of Reports":
        if option == "Download Excel":
            file_path, message = get_excel_report(access_token, instance_url, report_id)
            if file_path:
                st.success("✅ Report generated successfully!")
                st.download_button(
                    label="📥 Download Excel Report",
                    data=open(file_path, "rb"),
                    file_name=message,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.error(message)
        
       

        elif option == "Describe Report":
            report_description = describe_report(access_token, instance_url, report_id)

            # Display JSON with streamlit_ace
            st.subheader("📑 Report Description (JSON)")
            json_text = json.dumps(report_description, indent=4)
            # Provide JSON download button
            json_filename = "report_description.json"
            st.download_button(
                label="📥 Download JSON",
                data=json_text,
                file_name=json_filename,
                mime="application/json"
            )
            st_ace(value=json_text, language="json", theme="monokai", readonly=True)

      

        elif option == "Get Report Details":
            report_details = get_report_details(access_token, instance_url, report_id)

            # Display JSON with streamlit_ace
            st.subheader("📊 Report Details (JSON)")
            json_text = json.dumps(report_details, indent=4)
             # Provide JSON download button
            json_filename = "report_details.json"
            st.download_button(
                label="📥 Download JSON",
                data=json_text,
                file_name=json_filename,
                mime="application/json"
            )
            st_ace(value=json_text, language="json", theme="monokai", readonly=True)

           
        elif option == "Get List of Report Types":
            report_types = get_report_types(access_token, instance_url)

            # Display JSON with streamlit_ace
            st.subheader("📄 List of Report Types (JSON)")
            json_text = json.dumps(report_types, indent=4)

            # Provide JSON download button
            json_filename = "report_types.json"
            st.download_button(
                label="📥 Download JSON",
                data=json_text,
                file_name=json_filename,
                mime="application/json"
            )
            st_ace(value=json_text, language="json", theme="monokai", readonly=True)

    else:
        st.warning("⚠️ Please enter all required fields.")