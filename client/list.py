import requests, json

url = "https://newssites.pythonanywhere.com"

response = requests.get(f"{url}/api/directory/")

if response.status_code == 200:
    print("Success")
    data = response.json()
    for agency in data:
        print(f"Agency Name: {agency['agency_name']}, URL: {agency['url']}, Code: {agency['agency_code']}")
else:
    print("Failure")
    print(response.content)
    