import requests

url = "http://localhost:8000/admin/get_link/"
headers = {
    "Authorization": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzA2ODc5ODY5LCJpYXQiOjE3MDY3OTM0NjksImp0aSI6ImE3N2Q1ZWM5ZWY4ZjQ0MTViZTQwMmJlMjA3NDU3YmUwIiwidXNlcl9pZCI6NX0.PXPTH1JivXOvPxyNSxqRXHrbGozoQtRojyGK8G4xLLc",
    "Content-Type": "application/json",
    "X-CSRFToken": "M5wArjYv6Ggdh7hgfEg89FPo46wJvcTd",
}
payload_data = {
    "link": "www.youtube.com"
}

response = requests.post(url, headers=headers, json=payload_data)

print(response.status_code)
print(response.json())
