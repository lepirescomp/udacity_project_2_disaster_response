# Disaster Response Pipeline Project
## Disaster Response ETL, ML pipelines and Web application.


### Code and data

-  process_data.py: This code process messages.csv (containing message data) and categories.csv (classes of messages) and creates an SQLite database.

-  train_classifier.py: This code takes the SQLite as input and uses the data  to build/tunne a ML model for categorizing messages. The output is a pickle file with the model fit. 

-  disaster_messages.csv, disaster_categories.csv contain sample messages (real messages that were sent during disaster events) and categories datasets in csv format.
-  templates folder: This folder contains all of the files necessary to run and render the web app.

## Setup:
- pyenv shell 3.7
- python -m venv venv
- python install -r requirements.txt

### Instructions:
1. Run the following commands in the project's root directory to set up your database and model.

    - To run ETL pipeline that cleans data and stores in database
        `python data/process_data.py data/disaster_messages.csv data/disaster_categories.csv data/DisasterResponse.db`
    - To run ML pipeline that trains classifier and saves
        `python models/train_classifier.py data/DisasterResponse.db models/classifier.pkl`

2. Run the following command in the app's directory to run your web app.
    `python run.py`

3. Go to http://0.0.0.0:3001/
