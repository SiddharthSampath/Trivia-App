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
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    def paginate_questions(request, questions):
        page = request.args.get("page", 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        formatted_questions = [question.format() for question in questions]
        return formatted_questions[start:end]

    @app.route('/questions')
    def get_questions():
        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)
        categories_values = Category.query.all()
        categories = [category.type for category in categories_values]

        if len(current_questions) == 0 or current_questions is None:
            abort(404)
            return
        else:

            return jsonify({
                "questions": current_questions,
                "total_questions": len(questions),
                "categories": categories,
                "current_category": None
            })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(422)
            else:
                question.delete()
                return jsonify({
                    "success": True,
                    "questions_id": question_id
                })

        except BaseException:
            abort(422)

    @app.route('/categories')
    def getCategories():
        categories = Category.query.all()
        formatted_categories = [category.type for category in categories]

        return jsonify({
            "categories": formatted_categories
        })

    @app.route('/questions', methods=['POST'])
    # Since we use the same end point to add a new question, and also search
    # for a question, both operations are handled in this route
    def add_question_or_search():
        try:
            question_json = request.get_json()
            search_term = question_json.get("searchTerm", None)

            # If a search term is submitted, then we perform a search operation
            if search_term:
                search_questions = Question.query.filter(
                    Question.question.ilike(f'%{search_term}%')).all()
                current_questions = paginate_questions(
                    request, search_questions)
                if len(current_questions):
                    current_category = current_questions[-1]["category"]
                else:
                    current_category = None
                return jsonify({
                    "questions": current_questions,
                    "total_questions": len(search_questions),
                    "current_category": current_category
                })
            # If there is no search term in the json, then we add a new
            # question
            else:
                # print(question_json)
                question = question_json["question"]
                answer = question_json["answer"]
                category = question_json["category"]
                difficulty = question_json["difficulty"]
                question_add = Question(
                    question=question,
                    answer=answer,
                    category=category,
                    difficulty=difficulty)

                question_add.insert()
                return jsonify({
                    "success": True,
                    "id": question_add.id
                })

        except BaseException:
            abort(400)

    @app.route('/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        category_id = str(category_id)
        questions_in_category = Question.query.filter(
            Question.category == category_id).all()
        current_questions = paginate_questions(request, questions_in_category)
        if len(current_questions):
            current_category = current_questions[0]["category"]
        else:
            abort(404)

        return jsonify({
            "questions": current_questions,
            "total_questions": len(questions_in_category),
            "current_category": current_category
        })

    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            # Get the category and previous questions from the request sent
            question_data = request.get_json()
            category = question_data["quiz_category"]["id"]
            category_type = question_data["quiz_category"]["type"]
            previous_questions = question_data["previous_questions"]
            # The next question should not be in the previous question. So, we can remove all the previous questions from the category_questions.
            # To do this optimally, we can store all previous questions in a
            # hash table/ dictionary so that we can check if a question is a
            # previous question in constant time.
            previous_questions_dictionary = {}
            for question in previous_questions:
                previous_questions_dictionary[question] = True

            if category_type == "click":
                category_questions = Question.query.all()
            else:
                category_questions = Question.query.filter(
                    Question.category == category).all()
            new_questions = []
            for question in category_questions:
                # This checks whether the question is a previous question or
                # not, in constant time.
                if question.id not in previous_questions_dictionary:
                    new_questions.append(question)

            if len(new_questions) == 0:
                random_next_question = None
            else:

                random_next_question = random.choice(new_questions)
                random_next_question = random_next_question.format()
                print(random_next_question)
            return jsonify({
                "question": random_next_question

            })
        except BaseException:
            abort(400)

    @app.errorhandler(404)
    def notFound(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"

        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"

        }), 422

    @app.errorhandler(400)
    def badRequest(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "Bad Request"

        }), 400

    @app.errorhandler(405)
    def methodNotAllowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": "Method Not Allowed"

        }), 405

    return app
