import requests
import getpass

session = requests.Session()
global_url=""

def login(url):

    global session, global_url
    global_url = url

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
    global session, global_url

    if global_url == "":
        print("You have not logged in.")
        return

    params = {
       # 'story_id': '*',
        'story_cat': '*',
        'story_region': '*',
        'story_date': '*'
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    for arg in switches:
       # if arg.startswith("-id="):
        #    params['story_id'] = arg[len("-id="):]
        if arg.startswith("-cat="):
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
        
    response = session.get(f"{global_url}api/stories", headers=headers, params=params)

    if response.status_code == 200:
        print("News fetched successfully.")
        news_items = response.json()
        for news in news_items:
            print(f"ID: {news['key']}, Headline: {news['headline']}, Category: {news['story_cat']}, Region: {news['story_region']}, Date: {news['story_date']}, Author: {news['author']}, Details: {news['story_details']}")
    else:
        print("Failed to fetch news.")
        print(response.reason)


def list_services():
    global session, global_url

    print("Listing services...")

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
