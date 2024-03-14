from django.test import TestCase

import requests

url = "http://127.0.0.1:8000/api/contract/"

data = {"total": "15000.00", "author": 1, "agent_id": 1, "comment_id": 1}

files = {"file_path": open("backend\\static\\media\\files\\contract_O3dO5f8.pdf", "rb")}

response = requests.post(url, data=data, files=files)

print(response.status_code)
print(response.json())
