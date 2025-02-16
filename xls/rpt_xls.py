import streamlit as st
import requests
import os

# Function to fetch the Excel report from Salesforce
def get_excel_report(access_token, instance_url, report_id):
    try:
        # API endpoint
        url = f"{instance_url}/services/data/v60.0/analytics/reports/{report_id}"

        # Headers for the request
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        }

        # Make the GET request
        response = requests.get(url, headers=headers)

        # Check response status
        if response.status_code == 200:
            # Get the filename from the Content-Disposition header
            content_disposition = response.headers.get("Content-Disposition", "")
            filename = "Salesforce_Report.xlsx"  # Default filename
            if "filename=" in content_disposition:
                filename = content_disposition.split("filename=")[-1].strip('"')

            # Save the file locally
            file_path = os.path.join("downloads", filename)
            os.makedirs("downloads", exist_ok=True)
            with open(file_path, "wb") as file:
                file.write(response.content)

            return file_path, filename
        else:
            return None, f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return None, f"Exception: {str(e)}"

# Streamlit UI
st.title("📊 Salesforce Report Downloader")
st.markdown("Enter the required details to download the report as an Excel file.")

# User Inputs
access_token = st.text_input("🔑 Access Token", type="password")
instance_url = st.text_input("🌐 Instance URL", value="https://your-instance.salesforce.com")
report_id = st.text_input("📄 Report ID")

# Download Button
if st.button("Download Report"):
    if access_token and instance_url and report_id:
        file_path, message = get_excel_report(access_token, instance_url, report_id)
        if file_path:
            st.success("✅ Report generated successfully!")
            st.download_button(label="📥 Download Excel Report", data=open(file_path, "rb"), file_name=message, mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.error(message)
    else:
        st.warning("⚠️ Please enter all required fields.")