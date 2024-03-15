from django.test import TestCase

import requests

url = "http://localhost:8080/tasks/1"
headers = {"Content-Type": "application/json"}
data = {"title": "First Task", "status": "Not Done"}

response = requests.delete(url, headers=headers)

print(response.text)
