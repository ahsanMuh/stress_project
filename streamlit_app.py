import requests
import config
import json

import streamlit as st

API_URL = config.API_ROOT_ADR

# First page - Login
def login():
    st.title("Operator’s Stress Detection Project")
    st.write("Please login to continue")

    # Input fields for username and password
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    # Login button
    if st.button("Login"):
        # Call API to authenticate user
        response = requests.post(f"{API_URL}/admin/login", json={"username": username, "password": password})

        if  response.status_code == 200:
            # Save the token and user ID in the session
            response_json = json.loads(response.text)

            # Save the token and user ID in the session
            st.session_state.token = response_json["token"]
            st.session_state.user_id = response_json["id"]
            file_upload()
        else:
            st.error("Invalid username or password")


# Second page - File Upload
def file_upload():
    st.title("File Upload")
    st.write("Please upload an EDF file and select the employee ID")

    # Get the list of employee IDs associated with the current admin
    response = requests.get(
        f"{API_URL}/employee/list?_id={st.session_state.user_id}")

    if False:  # response.status_code != 200:
        st.error("Failed to fetch employee IDs")
        return
    response_json = json.loads(response.text)
    # stress_list = response_json['stress_list']
    employee_ids = response_json['employee_ids']

    # File upload and employee ID selection
    edf_file = st.file_uploader("Upload an edf file", type="edf")
    employee_id = st.selectbox("Select employee ID", employee_ids)

    # Submit button
    if st.button("Submit"):
        if not edf_file:
            st.error("Please upload an EDF file")
            return

        # Call API to submit the file and employee ID
        # headers = {"Authorization": f"Bearer {st.session_state.token}"}
        files = {"file": edf_file.read()}
        data = {"employee_id": employee_id}
        response = requests.post(f"{API_URL}/stress/add", files=files, data=data)

        if response.status_code == 200:
            st.success('Success!')  # response.json()["message"])
        else:
            st.error(response.json()["message"])

    # Logout button
    if st.button("Logout"):
        # Clear the session state and go back to the login page
        st.session_state.token = None
        st.session_state.user_id = None
        st.session_state.file_uploaded = False
        st.experimental_rerun()  # Rerun the app to display the login page
        return

# Main function - app entry point
def main():
    if not hasattr(st.session_state, "token"):
        st.session_state.token = None
    st.set_page_config(page_title="Stress Project", page_icon=":brain:")
    if not st.session_state.token:
        login()
    else:
        file_upload()


if __name__ == "__main__":
    main()
