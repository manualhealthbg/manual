import unittest
from unittest.mock import patch, MagicMock
from services.question_transitions import (
    get_question_transitions,
    get_question_transition_by_id,
    create_question_transition,
    update_question_transition,
    delete_question_transition
)

class TestQuestionTransitionsServices(unittest.TestCase):

    @patch('services.question_transitions.get_db_connection')
    def test_get_question_transitions(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        mock_cursor.fetchall.return_value = [
            {'id': 1, 'answer_id': 1, 'next_question_id': 2, 'product_id': None},
            {'id': 2, 'answer_id': 2, 'next_question_id': None, 'product_id': 1}
        ]

        transitions = get_question_transitions()

        self.assertEqual(len(transitions), 2)
        self.assertEqual(transitions[0]['next_question_id'], 2)
        self.assertEqual(transitions[1]['product_id'], 1)

    @patch('services.question_transitions.get_db_connection')
    def test_create_question_transition_with_next_question(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1

        rowcount = create_question_transition(1, next_question_id=2, product_id=None)

        self.assertEqual(rowcount, 1)
        mock_cursor.execute.assert_called_with('\n        INSERT INTO question_transitions (answer_id, next_question_id, product_id)\n        VALUES (%s, %s, %s)\n        ', (1, 2, None))
        mock_connection.commit.assert_called_once()

    @patch('services.question_transitions.get_db_connection')
    def test_create_question_transition_with_product_id(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1  # Mock rowcount to return 1

        rowcount = create_question_transition(1, next_question_id=None, product_id=1)

        self.assertEqual(rowcount, 1)
        mock_cursor.execute.assert_called_with('\n        INSERT INTO question_transitions (answer_id, next_question_id, product_id)\n        VALUES (%s, %s, %s)\n        ', (1, None, 1))
        mock_connection.commit.assert_called_once()

    @patch('services.question_transitions.get_db_connection')
    def test_update_question_transition(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1

        rowcount = update_question_transition(1, 1, next_question_id=2, product_id=None)

        self.assertEqual(rowcount, 1)
        mock_cursor.execute.assert_called_with('\n        UPDATE question_transitions\n        SET answer_id = %s, next_question_id = %s, product_id = %s\n        WHERE id = %s\n        ', (1, 2, None, 1))
        mock_connection.commit.assert_called_once()

    @patch('services.question_transitions.get_db_connection')
    def test_delete_question_transition(self, mock_get_db_connection):
        mock_connection = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_cursor.rowcount = 1  # Mock rowcount to return 1

        rowcount = delete_question_transition(1)

        self.assertEqual(rowcount, 1)
        mock_cursor.execute.assert_called_with("DELETE FROM question_transitions WHERE id = %s", (1,))
        mock_connection.commit.assert_called_once()
