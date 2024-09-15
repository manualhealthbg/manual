import unittest
from unittest.mock import patch, MagicMock
from services.quiz_filler import get_quiz_current_question, answer_current_question
from domain.quiz_filler import QuizFiller


class TestQuizFiller(unittest.TestCase):

    def setUp(self):
        self.quiz_snapshot = {
            "questions": [
                {"id": 1, "text": "am I old?", "status": "published", "answers": [
                    {"id": 1, "text": "yes", "status": "published"},
                    {"id": 2, "text": "no", "status": "published"}
                ]},
                {"id": 2, "text": "am I pretty?", "status": "published", "answers": [
                    {"id": 3, "text": "yes", "status": "published"},
                    {"id": 4, "text": "maybe", "status": "published"},
                    {"id": 5, "text": "no", "status": "published"}
                ]}
            ],
            "products": [
                {"id": 1, "name": "Product A", "description": "Desc A", "status": "draft"},
                {"id": 2, "name": "Product B", "description": "Desc B", "status": "draft"}
            ],
            "product_restrictions": [],
            "question_transitions": [
                {"id": 1, "answer_id": 1, "next_question_id": 2, "product_id": None},
                {"id": 2, "answer_id": 2, "next_question_id": 2, "product_id": None},
                {"id": 3, "answer_id": 3, "next_question_id": None, "product_id": 1},
                {"id": 4, "answer_id": 4, "next_question_id": None, "product_id": 2}
            ]
        }

    @patch('services.quiz_filler.quiz_collection')
    def test_answer_current_question_invalid_answer(self, mock_quiz_collection):
        mock_quiz = QuizFiller(5, self.quiz_snapshot, progress={"answers_given": [], "current_question_id": 1})
        mock_quiz_collection.find_one.return_value = {"quiz_snapshot": self.quiz_snapshot, "progress": mock_quiz.progress}

        with self.assertRaises(ValueError):
            answer_current_question(5, 99)


    @patch('services.quiz_filler.quiz_collection')
    def test_get_quiz_recommended_products(self, mock_quiz_collection):
        mock_quiz = QuizFiller(5, self.quiz_snapshot, progress={"answers_given": [
            {"question_id": 1, "answer_id": 1}
        ], "recommended_products": [{"id": 1, "name": "Product A", "description": "Desc A", "status": "draft"}], "current_question_id": None})

        mock_quiz_collection.find_one.return_value = {"quiz_snapshot": self.quiz_snapshot, "progress": mock_quiz.progress}

        result = get_quiz_current_question(5)

        self.assertIn("recommended_products", result)
        self.assertEqual(len(result["recommended_products"]), 1)
        self.assertEqual(result["recommended_products"][0]["name"], "Product A")
