import mysql.connector
from mysql.connector import Error
from typing import List, Dict
from services.db_config import DB_CONFIG


def get_all_questions():
    """Fetch all questions along with their answers."""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query = """
        SELECT q.id AS question_id, q.text AS question_text, q.status AS question_status,
               a.id AS answer_id, a.text AS answer_text, a.status AS answer_status
        FROM questions q
        LEFT JOIN answers a ON q.id = a.question_id
        """

        cursor.execute(query)
        rows = cursor.fetchall()

        questions = {}
        for row in rows:
            question_id = row['question_id']
            if question_id not in questions:
                questions[question_id] = {
                    'id': question_id,
                    'text': row['question_text'],
                    'status': row['question_status'],
                    'answers': []
                }
            if row['answer_id']:
                questions[question_id]['answers'].append({
                    'id': row['answer_id'],
                    'text': row['answer_text'],
                    'status': row['answer_status']
                })

        return list(questions.values())

    except Error as e:
        print(f"Error: {e}")
        raise e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def create_question(text: str):
    """
    Inserts a new question into the questions table.

    :param text: Text of the question
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = "INSERT INTO questions (text, status) VALUES (%s, 'draft')"
        cursor.execute(query, (text,))

        connection.commit()
        print("Question created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


def publish_question(question_id: int):
    """
    Publishes a question by setting its status to 'published' only if the current status is 'draft'.

    :param question_id: The ID of the question to publish
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        select_query = "SELECT status FROM questions WHERE id = %s"
        cursor.execute(select_query, (question_id,))
        result = cursor.fetchone()

        if result is None:
            print("Question not found.")
            return

        current_status = result[0]
        update_query = "UPDATE questions SET status = 'published' WHERE id = %s"
        cursor.execute(update_query, (question_id,))
        connection.commit()
        print("Question published successfully.")
        # if current_status == 'draft':
        #     update_query = "UPDATE questions SET status = 'published' WHERE id = %s"
        #     cursor.execute(update_query, (question_id,))
        #     connection.commit()
        #     print("Question published successfully.")
        # else:
        #     print(f"Cannot publish question. Current status is '{current_status}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


def disable_question(question_id: int):
    """
    Disables a question by setting its status to 'disabled' only if the current status is 'published'.

    :param question_id: The ID of the question to disable
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        select_query = "SELECT status FROM questions WHERE id = %s"
        cursor.execute(select_query, (question_id,))
        result = cursor.fetchone()

        if result is None:
            print("Question not found.")
            return

        current_status = result[0]

        if current_status == 'published':
            update_query = "UPDATE questions SET status = 'disabled' WHERE id = %s"
            cursor.execute(update_query, (question_id,))
            connection.commit()
            print("Question disabled successfully.")
        else:
            print(f"Cannot disable question. Current status is '{current_status}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


def create_answer(text: str, question_id: int):
    """
    Inserts a new answer into the answers table.

    :param text: Text of the answer
    :param question_id: The ID of the question to which the answer belongs
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = "INSERT INTO answers (text, question_id, status) VALUES (%s, %s, 'draft')"
        cursor.execute(query, (text, question_id))

        connection.commit()
        print("Answer created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


def publish_answer(answer_id: int):
    """
    Publishes an answer by setting its status to 'published' only if the current status is 'draft'.

    :param answer_id: The ID of the answer to publish
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        select_query = "SELECT status FROM answers WHERE id = %s"
        cursor.execute(select_query, (answer_id,))
        result = cursor.fetchone()

        if result is None:
            print("Answer not found.")
            return

        current_status = result[0]

        if current_status == 'draft':
            update_query = "UPDATE answers SET status = 'published' WHERE id = %s"
            cursor.execute(update_query, (answer_id,))
            connection.commit()
            print("Answer published successfully.")
        else:
            print(f"Cannot publish answer. Current status is '{current_status}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


def disable_answer(answer_id: int):
    """
    Disables an answer by setting its status to 'disabled' only if the current status is 'published'.

    :param answer_id: The ID of the answer to disable
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        select_query = "SELECT status FROM answers WHERE id = %s"
        cursor.execute(select_query, (answer_id,))
        result = cursor.fetchone()

        if result is None:
            print("Answer not found.")
            return

        current_status = result[0]

        if current_status == 'published':
            update_query = "UPDATE answers SET status = 'disabled' WHERE id = %s"
            cursor.execute(update_query, (answer_id,))
            connection.commit()
            print("Answer disabled successfully.")
        else:
            print(f"Cannot disable answer. Current status is '{current_status}'.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

def create_restriction(answer_id: int, product_id: int):
    """
    Inserts a new 'disallow' restriction into the product_restrictions table.

    :param answer_id: The ID of the answer
    :param product_id: The ID of the product
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        query = "INSERT INTO product_restrictions (product_id, answer_id) VALUES (%s, %s)"
        cursor.execute(query, (product_id, answer_id))

        connection.commit()
        print("Product restriction created successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


def remove_restriction_by_id(product_restriction_id: int):
    """
    Removes a restriction from the product_restrictions table by ID.

    :param product_restriction_id: The ID of the product restriction to remove
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor()

        delete_query = "DELETE FROM product_restrictions WHERE id = %s"
        cursor.execute(delete_query, (product_restriction_id,))

        connection.commit()
        print(f"Product restriction with ID {product_restriction_id} removed successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()


def get_product_restrictions(answer_id: int) -> List[Dict[str, any]]:
    """
    Retrieves all product restrictions for a given answer_id.

    :param answer_id: The ID of the answer
    :return: A list of dictionaries with product restrictions
    """
    restrictions = []
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM product_restrictions WHERE answer_id = %s"
        cursor.execute(query, (answer_id,))
        restrictions = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

    return restrictions

def get_all_product_restrictions() -> List[Dict[str, any]]:
    """
    Retrieves all product restrictions from the product_restrictions table.

    :return: A list of dictionaries with all product restrictions.
    """
    restrictions = []
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        cursor = connection.cursor(dictionary=True)

        # Fetch all product restrictions
        query = "SELECT * FROM product_restrictions"
        cursor.execute(query)
        restrictions = cursor.fetchall()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        connection.close()

    return restrictions
