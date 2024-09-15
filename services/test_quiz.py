import unittest
from unittest.mock import patch, MagicMock
from services.quiz import (
    get_all_questions,
    create_question,
    publish_question,
    disable_question,
    create_answer,
    publish_answer,
    disable_answer,
    create_restriction,
    remove_restriction_by_id,
    get_product_restrictions
)

class TestQuizServices(unittest.TestCase):

    @patch('services.quiz.mysql.connector.connect')
    def test_get_all_questinos(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            {
                'question_id': 1, 'question_text': 'Question 1', 'question_status': 'published',
                'answer_id': 1, 'answer_text': 'Answer 1', 'answer_status': 'published'
            },
            {
                'question_id': 1, 'question_text': 'Question 1', 'question_status': 'published',
                'answer_id': 2, 'answer_text': 'Answer 2', 'answer_status': 'draft'
            }
        ]

        result = get_all_questions()

        self.assertEqual(len(result), 1)  # One question
        self.assertEqual(len(result[0]['answers']), 2)  # Two answers under the same question

    @patch('services.quiz.mysql.connector.connect')
    def test_create_question(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        create_question("New Question")

        mock_cursor.execute.assert_called_with("INSERT INTO questions (text, status) VALUES (%s, 'draft')", ("New Question",))
        mock_connection.commit.assert_called_once()

    @patch('services.quiz.mysql.connector.connect')
    def test_publish_question(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = ('draft',)

        publish_question(1)

        mock_cursor.execute.assert_called_with("UPDATE questions SET status = 'published' WHERE id = %s", (1,))
        mock_connection.commit.assert_called_once()

    @patch('services.quiz.mysql.connector.connect')
    def test_disable_question(self, mock_connect):
        # Mock connection behavior
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = ('published',)

        disable_question(1)

        mock_cursor.execute.assert_called_with("UPDATE questions SET status = 'disabled' WHERE id = %s", (1,))
        mock_connection.commit.assert_called_once()

    @patch('services.quiz.mysql.connector.connect')
    def test_create_answer(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        create_answer("New Answer", 1)

        mock_cursor.execute.assert_called_with("INSERT INTO answers (text, question_id, status) VALUES (%s, %s, 'draft')", ("New Answer", 1))
        mock_connection.commit.assert_called_once()

    @patch('services.quiz.mysql.connector.connect')
    def test_publish_answer(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = ('draft',)

        publish_answer(1)

        mock_cursor.execute.assert_called_with("UPDATE answers SET status = 'published' WHERE id = %s", (1,))
        mock_connection.commit.assert_called_once()

    @patch('services.quiz.mysql.connector.connect')
    def test_disable_answer(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchone.return_value = ('published',)

        disable_answer(1)

        mock_cursor.execute.assert_called_with("UPDATE answers SET status = 'disabled' WHERE id = %s", (1,))
        mock_connection.commit.assert_called_once()


    @patch('services.quiz.mysql.connector.connect')
    def test_remove_restriction_by_id(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        remove_restriction_by_id(1)

        mock_cursor.execute.assert_called_with("DELETE FROM product_restrictions WHERE id = %s", (1,))
        mock_connection.commit.assert_called_once()

    @patch('services.quiz.mysql.connector.connect')
    def test_get_product_restrictions(self, mock_connect):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            {"id": 1, "product_id": 1, "answer_id": 1, "action": "allow"}
        ]

        result = get_product_restrictions(1)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['action'], "allow")

