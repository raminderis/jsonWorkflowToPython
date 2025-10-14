import requests

class SUTManager:
    def __init__(self):
        self.reservation_url = "http://us-policy:3200/api/v1/reservations"
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
        if response.status_code == 200:
            sutId = response.json().get("body", {}).get("id")
            self.sut_list_reserved[sutName] = sutId
            print(f"Reserved SUT ID: {sutId}")
            return sutId
        else:
            response.raise_for_status()

    def remove_sut(self, sutId):
        headers = {
            'Content-Type': 'application/json'
        }
        delete_url = f"{self.reservation_url}/{sutId}"
        response = requests.request("DELETE", delete_url, headers=headers)
        if response.status_code == 200:
            sutId_to_remove = self.sut_list_reserved.pop(sutId, None)
            if sutId_to_remove:
                print(f"Removed SUT ID: {sutId_to_remove}")
                return True
            else:
                print(f"SUT ID {sutId} not found in reserved list.")
                return False
        else:
            response.raise_for_status()

    def get_all_suts_reserved(self):
        return self.sut_list_reserved