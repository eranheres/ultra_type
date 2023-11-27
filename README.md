Let's start by defining the core classes, functions, and methods that will be necessary for this application:

1. `main.py`: This will be the entry point of the application. It will initialize the application with a default user and language, and handle the user's input.

2. `controller.py`: This will contain the Controller class, which will handle the logic of the application. It will interact with the model and the view. It now includes methods to change the user and select the language.

3. `model.py`: This will contain the Model class, which will handle the data of the application. It will interact with the database and provide methods to retrieve and store data. It now includes methods to set the user and the language.

4. `view.py`: This will contain the View class, which will handle the user interface of the application. It will display the data to the user and get the user's input.

5. `database.py`: This will contain the Database class, which will handle the interaction with the database. It will provide methods to create, read, update, and delete data in the database.

6. `language.py`: This will contain the Language class, which will handle the language-specific logic of the application. It will provide methods to get the words for the chosen language and the direction of the language.

7. `statistics.py`: This will contain the Statistics class, which will handle the statistics of the user's progress. It will provide methods to calculate the typing speed and success rate.
8. `test_controller.py`, `test_model.py`, `test_view.py`, `test_database.py`, `test_language.py`, `test_statistics.py`, `test_user.py`: These will contain the unit tests for the corresponding classes.

Now, let's start with the `main.py` file:

main.py
The main menu of the application now includes the following options:

1. Change User: This option allows you to change the current user. The default user is "default".

2. Select Language: This option allows you to select the language for practice. The default language is "English".

3. Practice: This option allows you to enter a practice mode where you can practice typing words in the selected language.

4. Show Statistics: This option displays your typing statistics.

5. Exit: This option allows you to exit the application.

You can select an option by entering its corresponding number.
