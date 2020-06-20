# Full Stack Trivia API Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

## Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

## Running the server

From within the `backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `flaskr` directs flask to use the `flaskr` directory and the `__init__.py` file to find the application. 


## API Reference

### Getting Started

- Base URL : This project is currently not hosted on a public domain, and can only be run locally. The default port used by the API is 5000, and the base URL is > http://localhost:5000/

- Authentication : At present, no authentication or API keys are required for this API.

### Error Handling

Errors are formatted in the JSON format, and an example of an error returned is show below:

    {
      "success" : False,
      "error" : 422,
      "message" : "Unprocessable"

    }
The following errors are handled by the API:

> - 400 : Bad Request
> - 404 : Resource Not Found
> - 405 : Method Not Allowed
> - 422 : Unprocessable

### Endpoints

#### GET /questions

##### **Functionality provided**

> - Returns a list of all the questions from the database, which contains questions, answers, the category they belong to and the difficulty.
> - The results are paginated, with 10 results per page.
> - A list of all categories is also returned, to provide the user with a category list to choose from.

##### **Sample** 
A sample request to get all the questions using curl is shown below
>> curl http://localhost:5000/questions

    Response:
    {
        "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
      ],
      "current_category": null,
      "questions": [
        {
          "answer": "Alexander Fleming",
          "category": 0,
          "difficulty": 3,
          "id": 21,
          "question": "Who discovered penicillin?"
        },
        {
          "answer": "Blood",
          "category": 0,
          "difficulty": 4,
          "id": 22,
          "question": "Hematology is a branch of medicine involving the study of what?"
        },
        {
          "answer": "Escher",
          "category": 1,
          "difficulty": 1,
          "id": 16,
          "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
        {
          "answer": "Mona Lisa",
          "category": 1,
          "difficulty": 3,
          "id": 17,
          "question": "La Giaconda is better known as what?"
        },
        {
          "answer": "One",
          "category": 1,
          "difficulty": 4,
          "id": 18,
          "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
          "answer": "Jackson Pollock",
          "category": 1,
          "difficulty": 2,
          "id": 19,
          "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
          "answer": "Lake Victoria",
          "category": 2,
          "difficulty": 2,
          "id": 13,
          "question": "What is the largest lake in Africa?"
        },
        {
          "answer": "The Palace of Versailles",
          "category": 2,
          "difficulty": 3,
          "id": 14,
          "question": "In which royal palace would you find the Hall of Mirrors?"
        },
        {
          "answer": "Agra",
          "category": 2,
          "difficulty": 2,
          "id": 15,
          "question": "The Taj Mahal is located in which Indian city?"
        },
        {
          "answer": "Maya Angelou",
          "category": 3,
          "difficulty": 2,
          "id": 5,
          "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
      ],
      "total_questions": 30
    }

#### GET /categories

##### **Functionality provided**

> - Returns a list of all the categories from the database.

##### **Sample** 
A sample request to get categories using curl is shown below
>> curl http://localhost:5000/categories

    Response:
    {
        "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
      ]
    }
    
#### GET /<category_id>/categories/questions

##### **Functionality provided**

> - Returns a list of all question from the category which is provided in the url.

##### **Sample** 
A sample request to get questions of a paricular category using curl is shown below
>> curl http://localhost:5000/categories/1/questions

    Response :
    {
        "current_category": 1,
      "questions": [
        {
          "answer": "Escher",
          "category": 1,
          "difficulty": 1,
          "id": 16,
          "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
        },
        {
          "answer": "Mona Lisa",
          "category": 1,
          "difficulty": 3,
          "id": 17,
          "question": "La Giaconda is better known as what?"
        },
        {
          "answer": "One",
          "category": 1,
          "difficulty": 4,
          "id": 18,
          "question": "How many paintings did Van Gogh sell in his lifetime?"
        },
        {
          "answer": "Jackson Pollock",
          "category": 1,
          "difficulty": 2,
          "id": 19,
          "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
        },
        {
          "answer": "Nitrogen",
          "category": 1,
          "difficulty": 1,
          "id": 29,
          "question": "What is the most abundant gas in the Earth\u2019s atmosphere?"
        },
        {
          "answer": "asd",
          "category": 1,
          "difficulty": 1,
          "id": 35,
          "question": "asd"
        }
      ],
      "total_questions": 6
    }

#### POST /questions

##### **Functionality provided**

> - Add a new question or search for a particular question.

##### **Sample** 
A sample request to add a question using curl is shown below
>> curl http://localhost:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "What is an area surrounded by 3 sides with water called?", "answer": "Peninsula", "difficulty":"1", "category": "3" }'

    Response:
    {
      "success": true
    }

A sample request to search for a question using curl is shown below
>> curl http://localhost:5000/questions -X POST -H  "Content-Type: application/json" -d '{ "searchTerm" : "Cassius"}'

    Response:
    {
        "current_category": 3,
      "questions": [
        {
          "answer": "Muhammad Ali",
          "category": 3,
          "difficulty": 1,
          "id": 9,
          "question": "What boxer's original name is Cassius Clay?"
        }
      ],
      "total_questions": 1
    }
    
#### POST /quizzes

##### **Functionality provided**

> - Processes a post request, and returns a random question, based on the previous questions and the category selected.

##### **Sample** 
A sample request to get the next question of the quiz
>> curl http://localhost:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Science", "id": "0"}}"

    Response:
    {
        "question": {
        "answer": "Alexander Fleming",
        "category": 0,
        "difficulty": 3,
        "id": 21,
        "question": "Who discovered penicillin?"
      }
    }

#### DELETE /questions/<question_id>

##### **Functionality provided**

> - Deletes the selected question from the database.

##### **Sample** 
A sample request to delete a question from the quiz
>>  curl -X DELETE http://localhost:5000/questions/35

    Response:
    {
        "questions_id": 35,
        "success": true
    }


## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```