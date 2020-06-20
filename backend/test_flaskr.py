import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = f'postgres://postgres:postgres1@localhost:5432/{self.database_name}'
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_getQuestions(self):
        res = self.client().get('/questions')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(res_data["questions"])
        self.assertTrue(res_data["total_questions"])

    def test_getQuestions_404_error(self):
        res = self.client().get('/questions?page=1000')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(res_data["message"], "Resource Not Found")

    def test_searchQuestion(self):
        res = self.client().post('/questions', json={"searchTerm": "heaviest"})
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["total_questions"], 1)

    def test_searchQuestion_notFound(self):
        res = self.client().post('/questions', json={"searchTerm": "zzzzz"})
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["total_questions"], 0)

    def test_deleteQuestion(self):
        req_1 = self.client().post(
            '/questions',
            json={
                'question': 'q1',
                'answer': 'a1',
                'difficulty': '1',
                'category': '1'})
        res_data_1 = json.loads(req_1.data)
        id = res_data_1["id"]
        res = self.client().delete(f'/questions/{id}')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_deleteQuestion_422_error(self):
        res = self.client().delete('/questions/2000')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(res_data["message"], "Unprocessable")

    def test_addQuestion(self):
        res = self.client().post(
            '/questions',
            json={
                'question': 'q1',
                'answer': 'a1',
                'difficulty': '1',
                'category': '1'})
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(res_data["success"], True)

    def test_addQuestion_400_error(self):
        res = self.client().post(
            '/questions',
            json={
                "answer": "a1",
                "difficulty": 1,
                "category": 1})
        res_data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(res_data["message"], "Bad Request")

    def test_get_question_by_category(self):
        id = 1
        res = self.client().get(f'/categories/{id}/questions')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(str(res_data["current_category"]), "1")

    def test_get_question_by_category_404_error(self):
        id = 1000
        res = self.client().get(f'/categories/{id}/questions')
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_play_quiz(self):
        res = self.client().post(
            '/quizzes',
            json={
                'quiz_category': {
                    'type': 'Science',
                    'id': '1'},
                'previous_questions': []})
        res_data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_play_quiz_400_error(self):
        res = self.client().post(
            '/quizzes',
            json={
                'quiz_category': {
                    'type': 'Science'
                }
            })

        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
