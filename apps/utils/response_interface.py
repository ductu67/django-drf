# - status: True/False
# - messageCode: "ABC001"
# - messageParams: {"username": "as"}
# - data: {}


class Response:
    def __init__(self, status, data, message="success"):
        self.status = status
        self.data = data
        self.message = message
    
    def generate_response(self):
        response = dict()
        response["status"] = self.status
        response["message"] = self.message
        response["data"] = self.data
        return response
