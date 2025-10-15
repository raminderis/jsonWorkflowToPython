import requests

class TESTManager:
    def __init__(self):
        # self.reservation_url = "http://us-mobility:3210/api/v1/test-sessions"
        self.reservation_url = "http://localhost:8080/api/v1/test-sessions"

    def create_testSession(self, testname, tas, testServers, testLibrary=0):
        # Placeholder for creating a test session
        print(f"Creating test session for Test Name: {testname}, TAS: {tas}, Test Servers: {testServers}, Test Library: {testLibrary}")
        payload = {
            "test": testname,
            "tas": tas,
            "testServers": testServers,
            "libraryId": testLibrary
        }
        method = "POST"
        headers = {
            'Content-Type': 'application/json'
        }
        print(f"Creating test session with payload: {payload}")
        response = requests.request(method, self.reservation_url, headers=headers, json=payload)


        # response = requests.post(self.reservation_url, json={"testId": testId})
        if response.status_code == 201:
            print("Test session created successfully.")
            print("Response:", response.json())
            return response.json()
        else:
            print(f"Failed to create test session: {response.status_code} - {response.text}")
            return None
        # Implement actual logic as needed
    
    def delete_testSession(self, testId):
        # Placeholder for deleting a test session
        print(f"Deleting test session for Test ID: {testId}")
        response = requests.delete(f"{self.reservation_url}/{testId}")
        if response.status_code == 204:
            print("Test session deleted successfully.")
            return True
        else:
            print(f"Failed to delete test session: {response.status_code} - {response.text}")
            return False
        # Implement actual logic as needed

    def get_session(self, test_session_id):
        # Placeholder for getting a test session
        print(f"Getting test session for Test ID: {test_session_id}")
        method = "GET"
        headers = {
            'Content-Type': 'application/json'
        }   
        session_state_url = f"{self.reservation_url}/{test_session_id}"
        response = requests.request(method, session_state_url, headers=headers)
        if response.status_code == 200:
            return {"testId": test_session_id, "status": response.json().get("status", "unknown")}
        else:
            print(f"Failed to get session state: {response.status_code} - {response.text}")
            return {"testId": test_session_id, "status": "error"}

    def run_test(self, testSessionId, parameters):
        # Placeholder for running a test
        print(f"Running test for Test Session ID: {testSessionId} with parameters: {parameters}")
        payload = parameters
        method = "POST"
        headers = {
            'Content-Type': 'application/json'
        }
        print(f"Executing test session: {testSessionId}")
        execution_url = f"{self.reservation_url}/{testSessionId}/execution"
        response = requests.request(method, execution_url, headers=headers, json=payload)
        if response.status_code == 200:
            print("Test execution started successfully.")
            return True
        else:
            print(f"Failed to start test execution: {response.status_code} - {response.text}")
            return False
        # Implement actual logic as needed
    
    def stop_test(self, testId):
        # Placeholder for stopping a test
        print(f"Stopping test for Test ID: {testId}")
        return True
        # Implement actual logic as needed

    def pause_test(self, testId):
        # Placeholder for pausing a test
        print(f"Pausing test for Test ID: {testId}")
        return True
        # Implement actual logic as needed

    def resume_test(self, testId):
        # Placeholder for resuming a test
        print(f"Resuming test for Test ID: {testId}")
        return True
        # Implement actual logic as needed