
1. `main.py`: This will be the entry point of the application. It will initialize the application and handle the user's input.

2. `controller.py`: This will contain the Controller class, which will handle the logic of the application. It will interact with the model and the view.

3. `model.py`: This will contain the Model class, which will handle the data of the application. It will interact with the database and provide methods to retrieve and store data.

4. `view.py`: This will contain the View class, which will handle the user interface of the application. It will display the data to the user and get the user's input.

5. `database.py`: This will contain the Database class, which will handle the interaction with the database. It will provide methods to create, read, update, and delete data in the database.

6. `language.py`: This will contain the Language class, which will handle the language-specific logic of the application. It will provide methods to get the words for the chosen language and the direction of the language.

7. `statistics.py`: This will contain the Statistics class, which will handle the statistics of the user's progress. It will provide methods to calculate the typing speed and success rate.

8. `test_controller.py`, `test_model.py`, `test_view.py`, `test_database.py`, `test_language.py`, `test_statistics.py`: These will contain the unit tests for the corresponding classes.

## To Do

- [x] Enable right to left option for languages that are written from right to left.
- [x] Enable the user to choose the lessons they want to practice.
- [x] Support multiple lines
- [x] Save user settings
- [x] Move view functions from controller to view.
- [x] Move view functions from model to view.
- [x] Display statistics based on users language
- [x] Show WPM and accuracy in real time
- [x] Save the practice id in the database
- [x] Show practices stats
- [x] Fix screen overlap crash
- [ ] Support practice that user brings his own text
- [ ] Support weak words practices
- [ ] Show settings in the view
- [ ] Center the text and the practice in the view
- [ ] Show screen rectangle in the view