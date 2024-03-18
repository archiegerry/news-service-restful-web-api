import requests
import getpass

session = requests.Session()
global_url=""

def login(url):

    global session, global_url
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

    # Add logic to authenticate with the service
    response = session.post(f"{url}api/login", data=payload, headers=headers)

    if response.status_code == 200:
        print("Logged in successfully.")
        print(response.reason)
    else:
        print("Failed to log in.")
        print(response.reason)


def logout():
    global session, global_url

    if global_url == "":
        print("You have not logged in.")
        return
    
    response = session.post(f"{global_url}api/logout")

    if response.status_code == 200:
        print("Logged out successfully.")
        print(response.reason)
        global_url = ""

    else:
        print("Logout failed")
        print(response.reason)

def post_news():
    global session, global_url

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

    response = session.post(f"{global_url}api/stories", json=payload)

    if response.status_code == 200:
        print("News posted successfully.")
        print(response.reason)
    else:
        print("Failed to post news.")
        print(response.reason)

def get_news(switches):

    params = {
        'story_cat': '*',
        'story_region': '*',
        'story_date': '*'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    newsservice = ""

    for arg in switches:
        if arg.startswith("-id="):
            newsservice = arg[len("-id="):]
        elif arg.startswith("-cat="):
            params['story_cat'] = arg[len("-cat="):]
        elif arg.startswith("-reg="):
            params['story_region'] = arg[len("-reg="):]
        elif arg.startswith("-date="):
            date_value = arg[len("-date="):]
            day, month, year = date_value.split('/')
            params['story_date'] = f"{year}-{month}-{day}"
        else:
            print("Usage: news [-id=] [-cat=] [-reg=] [-date=]")
            return
        
    url = "https://newssites.pythonanywhere.com"    
    directory_response = requests.get(f"{url}/api/directory/")
    directory_data = directory_response.json()

    if newsservice == "":
        print(f"{'ID':<10} {'Headline':<30} {'Category':<15} {'Region':<15} {'Date':<10} {'Author':<20} {'Details':<30}")
        for agency in directory_data:
            response = session.get(f"{agency['url']}/api/stories", headers=headers, params=params)
            if response.status_code == 200:
                    news_items = response.json()
                    try:
                        for news in news_items['stories']:
                            try:
                                print(f"{news['key']:<10} {news['headline'][:28]:<30} {news['story_cat']:<15} {news['story_region']:<15} {news['story_date']:<10} {news['author'][:18]:<20} {news['story_details'][:28]:<128}")
                            except (KeyError, TypeError):
                                print("Server error.")
                    except (KeyError, TypeError):
                        print("Server error.")

            else:
                    print("Failed to fetch news.")
                    print(response.reason)
    else:
        matched = 0
        for agency in directory_data:
            if agency['agency_code'] == newsservice:
                matched = 1
                response = session.get(f"{agency['url']}/api/stories", headers=headers, params=params)
                if response.status_code == 200:
                    print(f"{'ID':<10} {'Headline':<30} {'Category':<15} {'Region':<15} {'Date':<10} {'Author':<20} {'Details':<30}")
                    news_items = response.json()
                    try:
                        for news in news_items['stories']:
                            try:
                                print(f"{news['key']:<10} {news['headline'][:28]:<30} {news['story_cat']:<15} {news['story_region']:<15} {news['story_date']:<10} {news['author'][:18]:<20} {news['story_details'][:28]:<128}")
                            except (KeyError, TypeError):
                                print("Server error.")
                    except (KeyError, TypeError):
                        print("Server error.")
                else:
                    print("Failed to fetch news.")
                    print(response.reason)
        if matched == 0:
            print("No agency found with that code.")


def list_services():
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

def delete_news(key):
    global session, global_url

    if global_url == "":
        print("You have not logged in.")
        return
    
    response = session.delete(f"{global_url}api/stories/{key}")

    if response.status_code == 200:
        print("News deleted successfully.")
    else:
        print("Failed to delete news.")
        print(response.reason)


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
        args = command.split()[1:]  # Get arguments after "news"
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

def main():
    print("Welcome to the News Service CLI. Type 'exit' to quit.")
    while True:
        command = input("> ")
        if command == "exit":
            break
        process_command(command)

if __name__ == "__main__":
    main()
