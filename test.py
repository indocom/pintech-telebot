import requests 

url = "https://api.notion.com/v1/databases/ce1357c2d9e64bee8067d53b2eb7309e"
token = "secret_FF6WUjuKEa91I1s4GycsF6OgDxqsZhjBJcWy5SuUMBe"

headers = {
    "Accept": "application/json",
    "Notion-Version": "2021-08-16",
    "Authorization": "Bearer secret_FF6WUjuKEa91I1s4GycsF6OgDxqsZhjBJcWy5SuUMBe"
}

response = requests.request("GET", url, headers=headers)

# print(response.text)

url = "https://api.notion.com/v1/databases/ce1357c2d9e64bee8067d53b2eb7309e/query"

payload = {"page_size": 100}
headers = {
    "Accept": "application/json",
    "Notion-Version": "2021-08-16",
    "Content-Type": "application/json",
    "Authorization": "Bearer secret_FF6WUjuKEa91I1s4GycsF6OgDxqsZhjBJcWy5SuUMBe"
}

response = requests.request("POST", url, json=payload, headers=headers)

print(response.text)
