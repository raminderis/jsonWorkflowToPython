import requests

class SUTManager:
    def __init__(self):
        # self.reservation_url = "http://us-policy:3200/api/v1/reservations"
        self.reservation_url = "http://localhost:8080/api/v1/reservations"
        self.sut_list_reserved = {}

    def reserve_sut(self, sutName, workflowId, userName):
        payload = {
            "criteria": {
                "sut": sutName
            },
            "properties": {
                "workflowId": workflowId
            },
            "userName": userName
        }
        method = "POST"
        headers = {
            'Content-Type': 'application/json'
        }
        print(f"Reserving SUT with payload: {payload}")
        response = requests.request(method, self.reservation_url, headers=headers, json=payload)
        # print(f"Response: {response.status_code} - {response.json()}")
        if response.status_code == 201:
            sutId = response.json().get("id")
            self.sut_list_reserved[sutName] = sutId
            print(f"Reserved SUT ID : {sutId}")
            return {
                "id": sutId,
                "status": "OK"
            }

        elif response.status_code == 400:
            print("SUT Reservation request REJECTED")
            return {
                "id": None,
                "status": "SUT_BUSY"
            }
        elif response.status_code > 400 or response.status_code is None:
            print("SUT Reservation request FAILED")
            return {
                "id": None,
                "status": "SUT_BUSY"
            }
        else:
            response.raise_for_status()

    def remove_sut(self, sutId):
        headers = {
            'Content-Type': 'application/json'
        }
        delete_url = f"{self.reservation_url}/{sutId}"
        response = requests.request("DELETE", delete_url, headers=headers)
        print(f"Response: {response.status_code} - {response.text}")
        if response.status_code == 204:
            print("SUT removed successfully.", self.sut_list_reserved)
            key_to_remove = next((key for key, value in self.sut_list_reserved.items() if value == sutId), None)
            if key_to_remove:
                self.sut_list_reserved.pop(key_to_remove)
                return True
            else:
                print(f"SUT ID {sutId} not found in reserved list.")
                return False
        else:
            response.raise_for_status()

    def get_all_suts_reserved(self):
        return self.sut_list_reserved