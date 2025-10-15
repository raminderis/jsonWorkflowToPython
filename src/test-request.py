import requests

# url = "http://localhost:8080"
url = "http://localhost:8080/api/v1/test-sessions"

# Send a GET request
response = requests.get(url)

# Check if the response is OK
if response.status_code == 200:
    print(f"Test session: {response.status_code} - {response.json()}")
else:
    print(f"Error {response.status_code}: {response.text}")


response = requests.post(url, json={"testId": "test_456"})
if response.status_code == 200:
    print(f"Test session created successfully. {response.status_code} - {response.text}")
else:
    print(f"Failed to create test session: {response.status_code} - {response.text}")

response = requests.delete(f"{url}/test_456")
if response.status_code == 200:
    print(f"Test session deleted successfully. {response.status_code} - {response.text}")
else:
    print(f"Failed to delete test session: {response.status_code} - {response.text}")