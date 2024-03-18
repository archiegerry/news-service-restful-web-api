INSTRUCTONS

    - Run python client.py from within the myclient folder
    - You will be prompted with a >
    - From here you can do the following:

        login <url>: Logs the client in
                     <url> must be in the form xyz.pythonanywhere.com
                     EXAMPLE:
                        login sc21ag.pythonanywhere.com

        
        logout: Logs the client out (must be logged in)

        post: Post news stories (must be logged in)
              You will be prompted to enter all the relevant details

        news [-id=] [-cat=] [-reg=] [-date=]: Aggregates all the news within parameters 
                                              [-id=] [-cat=] [-reg=] [-date=] all represent optional switches
                                              EXAMPLES:
                                                -id=AG01
                                                -cat=trivia
                                                -reg=w
                                                -date=11/03/2024

                                              Don't put a switch if you want everything in that category
                                                i.e -id=* or -cat=*
        
        list: Gathers all the news services in the directory

        delete <key>: Deletes a news story with a given primary key of <key> (must be logged in)
                      EXAMPLE:
                        delete 6

DOMAIN NAME

    sc21ag.pythonanywhere.com

CREDENTIALS

    username = ammar
    password = ammarsalka

OTHER INFORMATION

    You will need to run: 
        pip install tabulate
    If you do not have tabulate installed. This will allow the tables to be drawn.