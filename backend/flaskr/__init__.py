import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
    return response

  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  def paginate_questions(request, questions):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    formatted_questions = [question.format() for question in questions]
    return formatted_questions[start:end] 

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route('/questions')
  def get_books():
    questions = Question.query.all()
    current_questions = paginate_questions(request, questions)
    categories_values = Category.query.all()
    categories = [category.type for category in categories_values]
    
    if len(current_questions) == 0 or current_questions is None:
      abort(404)
      return
    else:  

      return jsonify({
        "questions" :  current_questions,
        "total_questions" : len(questions),
        "categories" : categories,
        "current_category" : None
      })
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:
      question = Question.query.filter(Question.id==question_id).one_or_none()
      if question is None:
        abort(422)
      else:
        question.delete()
        return jsonify({
          "success" : True,
          "questions_id" : question_id
        })

    except:
      abort(422)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/categories')
  def getCategories():
    categories = Category.query.all()
    formatted_categories = [category.type for category in categories]

    return jsonify({
      "categories" : formatted_categories
    })

  @app.route('/questions', methods=['POST'])
  # Since we use the same end point to add a new question, and also search for a question, both operations are handled in this route
  def add_question_or_search():
    try:
      question_json = request.get_json()
      search_term = question_json.get("searchTerm", None)

      # If a search term is submitted, then we perform a search operation
      if search_term:
        search_questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        current_questions = paginate_questions(request, search_questions)
        if len(current_questions):
          current_category = current_questions[-1]["category"]
        else:
          current_category = None
        return jsonify({
          "questions" : current_questions,
          "total_questions" : len(search_questions),
          "current_category" : current_category
        })
      #If there is no search term in the json, then we add a new question
      else:
        print(question_json)
        question = question_json["question"]
        answer = question_json["answer"]
        category = question_json["category"]
        difficulty = question_json["difficulty"]
        question_add = Question(question=question, answer=answer, category=category, difficulty=difficulty)

        question_add.insert()
        return jsonify({
          "success" : True,
        })

    except:
      abort(400)

  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
    category_id = str(category_id)
    questions_in_category = Question.query.filter(Question.category == category_id).all()
    current_questions = paginate_questions(request, questions_in_category)
    if len(current_questions):
      current_category = current_questions[0]["category"]
    else:
      current_category = None

    return jsonify({
      "questions" : current_questions,
      "total_questions" : len(questions_in_category),
      "current_category" : current_category
    })

    
    

  @app.errorhandler(404)
  def notFound(error):
    return jsonify({
      "success" : False,
      "error" : 404,
      "message" : "Resource Not Found"

    }), 404
  
  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success" : False,
      "error" : 422,
      "message" : "Unprocessable"

    }), 422

  @app.errorhandler(400)
  def badRequest(error):
    return jsonify({
      "success" : False,
      "error" : 400,
      "message" : "Bad Request"

    }), 400

  
  return app
  

  

  

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  

    