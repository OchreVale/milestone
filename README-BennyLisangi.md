The environment for this program requires that a few python libraries must be installed to run. In addition to the os in-built python library, the program requires dotenv, flask, flask_sqlalchemy, flask_login, werkzeug and requests libraries. Flask and requests can be installed in the terminal using the commands "pip install libray_name", all in lowercase. Dotenv is installed using "pip install python-dotenv". In addition to all those libraries, you must also install heroku in your terminal.


You must create an .env file in the current directory. The .env file contains important information without which your app won't be running. In the env. for this project, you must create a TMDB_KEY variable and associate it with your TMDB API key, create DATABASE_URL variable and associated with a postgresql database link, and finally you must create a session_key variable and associate it with any random string that you can use as your key. Reminder that all these variables are string variables so they must be enclosed in quotation marks.

Now to run the code locally, modify main.py by removing the first and the second parameters in the last line of code. At this stage, navigate to the same to directory as the main.py in your terminal. Then type "python main.py", and hit enter. The command should generate an IP address that you can view in your browser. You've successfully run the program!

Click on the link below the image to see the movie's wikipedia page, and click the poster image to navigate to the review page where you can leave a comment and a rating for the movie you clicked on. It is to note that all the comment and running submitted by the same user after their first comment will only replace that user's first comment. So, with one account, you can't leave two comments for the same movie. These comments will be replacing themselves.

https://ochremeter.herokuapp.com/

My final submission isn't different from what I wanted to do from the beginning. I wanted an app that allowed users to comment and rate every movie that can be pulled from TMDB. In the end, I think I successfully managed to accomplish just that.

Although I had clear ideas about what I wanted to, the road hadn't been quite easy. A major problem was designing a database that met my desires for my app. In the beginning, I set the movie_id to be a primary, but that does not work because every movie will be commented only once, trying to comment a movie that's already been commented leads to a database error. So, I had to decide that the primary to the review table in my datable will be an ID; that ID is automatically assignment when a comment or review is registered.

Then routing was also a problem. I needed to route my app so that I'd be passing parameters in the link that leads to a particular route. I've through StackOverflow and YT videos to implement a query; that is to add parameters after a route's name as "thisroute?name=moviename&id=movieid".