from mysql.connector import connect, Error
from services.db_config import DB_CONFIG

def get_db_connection():
    return connect(**DB_CONFIG)


def get_question_transitions():
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM question_transitions"
        cursor.execute(query)
        transitions = cursor.fetchall()
        return transitions
    except Error as e:
        print(f"Error fetching question transitions: {e}")
        return []
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def get_question_transition_by_id(transition_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM question_transitions WHERE id = %s"
        cursor.execute(query, (transition_id,))
        transition = cursor.fetchone()
        return transition
    except Error as e:
        print(f"Error fetching question transition: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def create_question_transition(answer_id, next_question_id=None, product_id=None):
    """
    Inserts a new question transition into the database.
    """
    if not (next_question_id or product_id):
        raise ValueError("Either next_question_id or product_id must be provided.")
    if next_question_id and product_id:
        raise ValueError("Only one of next_question_id or product_id can be provided, not both.")

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO question_transitions (answer_id, next_question_id, product_id)
        VALUES (%s, %s, %s)
        """
        cursor.execute(query, (answer_id, next_question_id or None, product_id or None))
        connection.commit()

        return cursor.rowcount
    except Error as err:
        print(f"Error: {err}")
        raise
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def update_question_transition(transition_id, answer_id, next_question_id=None, product_id=None):
    """
    Updates an existing question transition in the database.

    :param transition_id: The ID of the transition to update.
    :param answer_id: The ID of the answer.
    :param next_question_id: (Optional) The ID of the next question.
    :param product_id: (Optional) The ID of the product. Only one of next_question_id or product_id should be provided.
    :return: Number of rows affected or None in case of an error.
    """
    if not (next_question_id or product_id):
        raise ValueError("Either next_question_id or product_id must be provided.")
    if next_question_id and product_id:
        raise ValueError("Only one of next_question_id or product_id can be provided, not both.")

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        query = """
        UPDATE question_transitions
        SET answer_id = %s, next_question_id = %s, product_id = %s
        WHERE id = %s
        """
        cursor.execute(query, (answer_id, next_question_id or None, product_id or None, transition_id))
        connection.commit()

        return cursor.rowcount
    except Error as e:
        print(f"Error updating question transition: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def delete_question_transition(transition_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "DELETE FROM question_transitions WHERE id = %s"
        cursor.execute(query, (transition_id,))
        connection.commit()
        return cursor.rowcount
    except Error as e:
        print(f"Error deleting question transition: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
