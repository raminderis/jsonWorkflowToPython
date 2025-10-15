import requests

class RESULTSManager:
    def __init__(self):
        # self.reservation_url = "http://us-tram:3040/api/v1/results"
        self.reservation_url = "http://localhost:8080/api/v1/results"

    def get_tram_results(self, testId):
        # Placeholder for getting TRAM results
        print(f"Getting TRAM results for Test ID: {testId}")
        return {"testId": testId, "results": "sample_results"}
        # Implement actual logic as needed
    
    def store_tram_results(self, testId, results):
        # Placeholder for storing TRAM results
        print(f"Storing TRAM results for Test ID: {testId} with results: {results}")
        return True
        # Implement actual logic as needed

    def delete_tram_results(self, testId):
        # Placeholder for deleting TRAM results
        print(f"Deleting TRAM results for Test ID: {testId}")
        return True
        # Implement actual logic as needed

    def update_tram_results(self, testId, results):
        # Placeholder for updating TRAM results
        print(f"Updating TRAM results for Test ID: {testId} with results: {results}")
        return True
        # Implement actual logic as needed