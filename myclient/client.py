import requests
import getpass
from tabulate import tabulate

# Create a global session and url 
session = requests.Session()
global_url=""

# Handles logging in
def login(url):

    # Required to access/modify globals
    global session, global_url
    # User just has to put xyz.pythonanywhere.com
    global_url = "https://" + url

    username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    payload = {
        'username': username,
        'password': password
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Make login post request with given details
    response = session.post(f"{global_url}/api/login", data=payload, headers=headers)

    # Print error code and reason if unsuccessful
    if response.status_code == 200:
        print("Logged in successfully.")
    else:
        print(f"Failed to log in. Status Code: {response.status_code}\n")
        print(response.reason)

# Handles logging out
def logout():
    global session, global_url

    # Check to see if the user has logged in before by checking if the global url has been assigned
    # Also prevents client making more logout requests as global_url is set to "" at the end
    if global_url == "":
        print("You have not logged in.")
        return
    
    response = session.post(f"{global_url}/api/logout")

    if response.status_code == 200:
        print("Logged out successfully.")
        print(response.reason)
        # Set global to zero as a saftey measure
        global_url = ""

    else:
        print(f"Logout failed. Status Code: {response.status_code}\n")
        print(response.reason)

# Handles news posting
def post_news():
    global session, global_url

    # Sanity check
    if global_url == "":
        print("You have not logged in.")
        return

    headline = input("Enter headline: ")
    category = input("Enter category: ")
    region = input("Enter region: ")
    details = input("Enter details: ")

    payload = {
        'headline': headline,
        'category': category,
        'region': region,
        'details': details
    }

    # Post request as required
    response = session.post(f"{global_url}/api/stories", json=payload)

    if response.status_code == 200:
        print("News posted successfully.")
        print(response.reason)
    else:
        print(f"Failed to post news. Status Code: {response.status_code}\n")
        print(response.reason)

# Handles news aggregation
def get_news(switches):

    params = {
        'story_cat': '*',
        'story_region': '*',
        'story_date': '*'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    # Determines which news service to gather news from
    newsservice = ""

    # Applies relevant filters based on the clients switches
    for arg in switches:
        if arg.startswith("-id="):
            newsservice = arg[len("-id="):]
        elif arg.startswith("-cat="):
            params['story_cat'] = arg[len("-cat="):] # Everything after -cat=
        elif arg.startswith("-reg="):
            params['story_region'] = arg[len("-reg="):] # Everything after -reg=
        elif arg.startswith("-date="):
            date_value = arg[len("-date="):] # Everything after -date=
            day, month, year = date_value.split('/')
            params['story_date'] = f"{year}-{month}-{day}"
        else:
            print("Usage: news [-id=] [-cat=] [-reg=] [-date=]")
            return
        
    # Gets a list of all news services available
    url = "https://newssites.pythonanywhere.com"    
    directory_response = requests.get(f"{url}/api/directory/")
    directory_data = directory_response.json()

    # Truncation function for if news output is too long
    def truncate_string(s, max_length):
        if len(s) > max_length:
            # Cuts off the string after the length and puts a "..."
            return s[:max_length - 3] + "..."
        else:
            return s

    # If all of them ("*")
    if newsservice == "":
        # Go through all agencies
        for agency in directory_data:
             # Some people don't undertsand the difference between localhost and the actual internet...
            if (agency['url'] == "http://127.0.0.1:8000/") or (agency['url'] == "https://127.0.0.1:8000/"):
                print(f"The creator of {agency['agency_name']} is very silly and doesn't know how computers work")
            else:
             
             # Print status message
             print(f"Fetching news from: {agency['url']}\n")
             try:
                 # Make request to this agency
                 response = session.get(f"{agency['url']}/api/stories", headers=headers, params=params)
             except (ConnectionError, ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError):
                 print(f"Failed to fetch news. Response code: {response.status_code}\n")
                 print(f"Reason: {response.reason}\n")

             # If successful 
             if response.status_code == 200:
                    # News should be in Json format
                    news_items = response.json()
                    try:
                        # Truncate all items for niceness
                        truncated_items = [
                            [
                                truncate_string(str(item['key']), 8),
                                truncate_string(item['headline'], 64),
                                truncate_string(item['story_cat'], 16),
                                truncate_string(item['story_region'], 16),
                                truncate_string(item['story_date'], 16),
                                truncate_string(item['author'], 32),
                                truncate_string(item['story_details'], 128)
                            ] for item in news_items['stories']
                        ]
                    except (KeyError, TypeError):
                        print(f"Failed to fetch news. Response code: 404\n")
                        print(f"Reason: Not Found\n")

                    tab_headers = ["ID", "Headline", "Category", "Region", "Date", "Author", "Details"]
                    try:
                        print(tabulate(truncated_items, headers=tab_headers, tablefmt='grid'))
                    except (KeyError, TypeError):
                        print(f"Failed to fetch news. Response code: 404\n")
                        print(f"Reason: Not Found\n")

             # If not successful
             else:
                 print(f"Failed to fetch news. Response code: {response.status_code}\n")
                 print(f"Reason: {response.reason}\n")
    # If not all of them (-id=<something>)
    else:
        # Allows me to check if a user with this ID has been found
        matched = 0
        # Go through all agencies
        for agency in directory_data:
            # If found, set matched=1
            if agency['agency_code'] == newsservice:
                matched = 1

                # Some people don't undertsand the difference between localhost and the actual internet...
                if (agency['url'] == "http://127.0.0.1:8000/") or (agency['url'] == "https://127.0.0.1:8000/"):
                    print(f"The creator of {agency['agency_name']} is very silly and doesn't know how computers work")
                else:
                    # Keep updated
                    print(f"Fetching news from: {agency['url']}\n")
                    try:
                        # Make request to agency
                        response = session.get(f"{agency['url']}/api/stories", headers=headers, params=params)
                    except (ConnectionError, ConnectionRefusedError, ConnectionAbortedError, ConnectionResetError):
                        print(f"Failed to fetch news. Response code: {response.status_code}\n")
                        print(f"Reason: {response.reason}\n")
                    if response.status_code == 200:
                        news_items = response.json()

                        # If there is no news for this agency + filter combination
                        if (news_items['stories'] is None) or (news_items['stories'] == {}) or (news_items['stories'] == []):
                            print(f"Failed to fetch news. Response code: 404\n")
                            print(f"Reason: Not Found\n")
                            return

                        try:
                            tab_headers = ["ID", "Headline", "Category", "Region", "Date", "Author", "Details"]
             
                             # Truncate all items for niceness
                            truncated_items = [
                                [
                                    truncate_string(str(item['key']), 8),
                                    truncate_string(item['headline'], 64),
                                    truncate_string(item['story_cat'], 16),
                                    truncate_string(item['story_region'], 16),
                                    truncate_string(item['story_date'], 16),
                                    truncate_string(item['author'], 32),
                                    truncate_string(item['story_details'], 128)
                                ] for item in news_items['stories']
                            ]

                            # Tabulate for niceness
                            print(tabulate(truncated_items, headers=tab_headers, tablefmt='grid'))

                        except (KeyError, TypeError):
                            print(f"Failed to fetch news. Response code: 404\n")
                            print(f"Reason: Not Found\n")
                    else:
                        print(f"Failed to fetch news. Response code: {response.status_code}\n")
                        print(f"Reason: {response.reason}\n")
        if matched == 0:
            print("No agency found with that code.")

# HList all news agencies
def list_services():
    # Hardcode the URL as needed
    url = "https://newssites.pythonanywhere.com"

    # Make directory call
    response = requests.get(f"{url}/api/directory/")

    if response.status_code == 200:
        print("Success.")
        data = response.json()
        for agency in data:
            print(f"Agency Name: {agency['agency_name']}, URL: {agency['url']}, Code: {agency['agency_code']}")
    else:
        print(f"Failure. Status Code: {response.status_code}\n")
        print(response.content)

# Delete news based off primary key
def delete_news(key):
    global session, global_url

    if global_url == "":
        print("You have not logged in.")
        return
    
    response = session.delete(f"{global_url}/api/stories/{key}")

    if response.status_code == 200:
        print("News deleted successfully.")
    else:
        print("Failed to delete news.")
        print(response.reason)


# Determines which command the client has selected
def process_command(command):
    global global_url, session

    if command.startswith("login"):
        try:
            _, url = command.split()
        except ValueError:
            print("Usage: login <url>")
            return
        global_url=str(url)
        login(url)
    elif command == "logout":
        logout()
    elif command == "post":
        post_news()
    elif command.startswith("news"):
        args = command.split()[1:]  # Get arguments after news
        get_news(args)
    elif command == "list":
        list_services()
    elif command.startswith("delete"):
         try:
            _, key = command.split()
         except ValueError:
            print("Usage: delete <key>")
            return
         delete_news(key)
    else:
        print("Unknown command.")

# Simulates a terminal with ">"
def main():
    print("Welcome to the News Service CLI. Type 'exit' to quit.")
    while True:
        command = input("> ")
        if command == "exit":
            break
        process_command(command)

if __name__ == "__main__":
    main()
