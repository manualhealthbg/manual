from flask import Blueprint, request, jsonify
from services.quiz import (
    create_question,
    publish_question,
    disable_question,
    create_answer,
    publish_answer,
    disable_answer,
    create_restriction,
    remove_restriction_by_id,
    get_all_questions,
    get_product_restrictions
)

questions_blueprint = Blueprint('quiz', __name__)

@questions_blueprint.route('/question', methods=['POST'])
def create_question_endpoint():
    """
    curl -X POST http://127.0.0.1:5000/api/quiz/question \
    -H "Content-Type: application/json" \
    -d '{"text": "What is your favorite color?"}'

    :return:
    """
    data = request.get_json()
    text = data.get('text')
    if not text:
        return jsonify({"error": "Question text is required"}), 400
    create_question(text)
    return jsonify({"message": "Question created successfully"}), 201


@questions_blueprint.route('/question/<int:question_id>/publish', methods=['POST'])
def publish_question_endpoint(question_id):
    """
    curl -X POST http://127.0.0.1:5000/api/quiz/question/1/publish

    :param question_id:
    :return:
    """
    try:
        publish_question(question_id)
        return jsonify({"message": "Question published successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@questions_blueprint.route('/question/<int:question_id>/disable', methods=['POST'])
def disable_question_endpoint(question_id):
    """
    curl -X POST http://127.0.0.1:5000/api/quiz/question/1/disable

    :param question_id:
    :return:
    """
    try:
        disable_question(question_id)
        return jsonify({"message": "Question disabled successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@questions_blueprint.route('/answer', methods=['POST'])
def create_answer_endpoint():
    """
    curl -X POST http://127.0.0.1:5000/api/quiz/answer \
    -H "Content-Type: application/json" \
    -d '{"text": "Blue", "question_id": 1}'

    :return:
    """
    data = request.get_json()
    text = data.get('text')
    question_id = data.get('question_id')
    if not text or not question_id:
        return jsonify({"error": "Both answer text and question_id are required"}), 400
    create_answer(text, question_id)
    return jsonify({"message": "Answer created successfully"}), 201


@questions_blueprint.route('/answer/<int:answer_id>/publish', methods=['POST'])
def publish_answer_endpoint(answer_id):
    """
    curl -X POST http://127.0.0.1:5000/api/quiz/answer/1/publish

    :param answer_id:
    :return:
    """
    try:
        publish_answer(answer_id)
        return jsonify({"message": "Answer published successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@questions_blueprint.route('/answer/<int:answer_id>/disable', methods=['POST'])
def disable_answer_endpoint(answer_id):
    """
    curl -X POST http://127.0.0.1:5000/api/quiz/answer/1/disable

    :param answer_id:
    :return:
    """
    try:
        disable_answer(answer_id)
        return jsonify({"message": "Answer disabled successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@questions_blueprint.route('/restriction', methods=['POST'])
def create_restriction_endpoint():
    """
    curl -X POST http://127.0.0.1:5000/api/quiz/restriction \
    -H "Content-Type: application/json" \
    -d '{"answer_id": 1, "product_id": 1, "action": "allow"}'

    :return:
    """
    data = request.get_json()
    answer_id = data.get('answer_id')
    product_id = data.get('product_id')
    action = data.get('action')
    if not answer_id or not product_id or action not in ['allow', 'disallow']:
        return jsonify({"error": "Valid answer_id, product_id, and action are required"}), 400
    create_restriction(answer_id, product_id, action)
    return jsonify({"message": "Product restriction created successfully"}), 201


@questions_blueprint.route('/restriction/<int:product_restriction_id>', methods=['DELETE'])
def remove_restriction_by_id_endpoint(product_restriction_id):
    """
    curl -X DELETE http://127.0.0.1:5000/api/quiz/restriction/1

    :param product_restriction_id:
    :return:
    """
    try:
        remove_restriction_by_id(product_restriction_id)
        return jsonify({"message": "Product restriction removed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@questions_blueprint.route('/questions', methods=['GET'])
def get_all_questions_endpoint():
    """
    curl -X GET http://127.0.0.1:5000/api/quiz/answers

    Endpoint to get all answers with their associated questions.
    """
    try:
        result = get_all_questions()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

