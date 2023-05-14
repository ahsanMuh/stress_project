import streamlit as st
import requests

API_URL = "http://localhost:8000"

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
        #response = requests.post(f"{API_URL}/admin/login", json={"username": username, "password": password})

        if  True:#response.status_code == 200:
            # Save the token and user ID in the session
            token = 'aaaa' # response.json()["token"]
            user_id = 123  # response.json()["id"]
            st.session_state.token = token
            st.session_state.user_id = user_id
            # Go to the second page - File Upload
            file_upload()
        else:
            st.error("Invalid username or password")


# Second page - File Upload
def file_upload():
    st.title("File Upload")
    st.write("Please upload an EEG file and select the employee ID")

    # Get the list of employee IDs associated with the current admin
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    # response = requests.get(f"{API_URL}/admin/{st.session_state.user_id}/employees", headers=headers)
    if False:  # response.status_code != 200:
        st.error("Failed to fetch employee IDs")
        return
    employee_ids = [10001, 10002, 10003] #[employee["id"] for employee in response.json()]

    # File upload and employee ID selection
    eeg_file = st.file_uploader("Upload an EEG file", type="eeg")
    employee_id = st.selectbox("Select employee ID", employee_ids)

    # Submit button
    if st.button("Submit"):
        if not eeg_file:
            st.error("Please upload an EEG file")
            return

        # Call API to submit the file and employee ID
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        files = {"file": eeg_file.read()}
        data = {"employee_id": employee_id}
        # response = requests.post(f"{API_URL}/admin/{st.session_state.user_id}/upload", files=files, data=data, headers=headers)

        if True:  # response.status_code == 200:
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
