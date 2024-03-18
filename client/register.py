import requests, json

url = "https://newssites.pythonanywhere.com"

payload = {
    'agency_name':"Archie Gerry News Agency",
    'url':"https://sc21ag.pythonanywhere.com",
    'agency_code':"AG01"
}

response = requests.post(f"{url}/api/directory/", json=payload)

if response.status_code == 201:
    print("Success")
    print(response.reason)
else:
    print("Failure")
    print(response.content)