import sys
import os
from sklearn.metrics import classification_report
import re
import pandas as pd
from sqlalchemy import create_engine
import nltk
import pickle
from sklearn.model_selection import GridSearchCV

from nltk.stem import WordNetLemmatizer 
from nltk.tokenize import word_tokenize 
from nltk.corpus import stopwords
import re

nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from sklearn.multioutput import MultiOutputClassifier
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer


def load_data(database_filepath):
    # load data from database
    engine = create_engine('sqlite:///' + database_filepath)
    table_name = os.path.basename(database_filepath).replace(".db","")
    df = pd.read_sql_table(table_name,engine)

    df.dropna(inplace=True)
    X = df["message"].values.ravel()
    y = df[df.columns[4:]]
    return X, y.values, df.columns[4:]


def tokenize(text):
    # normalize case and remove punctuation
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())
    
    # tokenize text
    tokens = word_tokenize(text)
    
    stop_words = stopwords.words("english")
    lemmatizer = WordNetLemmatizer()
    # lemmatize andremove stop words
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]

    return tokens

def build_model():
    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('multi', MultiOutputClassifier(RandomForestClassifier())),
    ])


    parameters = {"multi__estimator__max_depth": [3],
              "multi__estimator__max_features": [1, 3],}


    cv = GridSearchCV(pipeline, param_grid=parameters)
    return cv

def evaluate_model(model, X_test, Y_test, category_names):
    y_pred = model.predict(X_test)
    
    for column in range(0,Y_test.shape[1]):
        score = classification_report(Y_test[:,column],y_pred[:,column])
        print(str(column), score)

def save_model(model, model_filepath):
    pickle.dump(model, open(model_filepath, 'wb'))


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, Y, category_names = load_data(database_filepath)
        X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2)
        
        print('Building model...')
        model = build_model()
        
        print('Training model...')
        model.fit(X_train, Y_train)
        
        print('Evaluating model...')
        evaluate_model(model, X_test, Y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()