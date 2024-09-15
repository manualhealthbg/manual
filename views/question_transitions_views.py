from flask import Blueprint, request, jsonify
from services.question_transitions import (
    get_question_transitions,
    get_question_transition_by_id,
    create_question_transition,
    update_question_transition,
    delete_question_transition
)

question_transitions_blueprint = Blueprint('question_transitions', __name__)

@question_transitions_blueprint.route('/question_transitions', methods=['POST'])
def create_question_transition_endpoint():
    """
    Endpoint to create a new question transition.
    Expects a JSON payload: { "answer_id": <answer_id>, "next_question_id": <next_question_id>, "product_id": <product_id> }
    """
    try:
        data = request.get_json()
        answer_id = data.get('answer_id')
        next_question_id = data.get('next_question_id')
        product_id = data.get('product_id')

        if not answer_id:
            return jsonify({"error": "answer_id is required"}), 400
        if (not next_question_id and not product_id) or (next_question_id and product_id):
            return jsonify({"error": "Provide either next_question_id or product_id, but not both"}), 400

        create_question_transition(answer_id, next_question_id, product_id)
        return jsonify({"message": "question transition created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@question_transitions_blueprint.route('/question_transitions', methods=['GET'])
def get_all_question_transitions():
    """
    Endpoint to get all question transitions.
    """
    try:
        transitions = get_question_transitions()
        return jsonify(transitions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@question_transitions_blueprint.route('/question_transitions/<int:transition_id>', methods=['GET'])
def get_question_transition(transition_id):
    """
    Endpoint to get a question transition by ID.
    """
    try:
        transition = get_question_transition_by_id(transition_id)
        if transition:
            return jsonify(transition), 200
        else:
            return jsonify({"error": "question transition not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@question_transitions_blueprint.route('/question_transitions/<int:transition_id>', methods=['PUT'])
def update_question_transition_endpoint(transition_id):
    """
    Endpoint to update a question transition by ID.
    Expects a JSON payload: { "answer_id": <answer_id>, "next_question_id": <next_question_id>, "product_id": <product_id> }
    """
    try:
        data = request.get_json()
        answer_id = data.get('answer_id')
        next_question_id = data.get('next_question_id')
        product_id = data.get('product_id')

        if not answer_id:
            return jsonify({"error": "answer_id is required"}), 400
        if (not next_question_id and not product_id) or (next_question_id and product_id):
            return jsonify({"error": "Provide either next_question_id or product_id, but not both"}), 400

        updated_rows = update_question_transition(transition_id, answer_id, next_question_id, product_id)
        if updated_rows:
            return jsonify({"message": "question transition updated successfully"}), 200
        else:
            return jsonify({"error": "question transition not found or no changes made"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@question_transitions_blueprint.route('/question_transitions/<int:transition_id>', methods=['DELETE'])
def delete_question_transition_endpoint(transition_id):
    """
    Endpoint to delete a question transition by ID.
    """
    try:
        deleted_rows = delete_question_transition(transition_id)
        if deleted_rows:
            return jsonify({"message": "question transition deleted successfully"}), 200
        else:
            return jsonify({"error": "question transition not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
