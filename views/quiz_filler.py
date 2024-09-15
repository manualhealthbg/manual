from flask import Blueprint, request, jsonify
from services.quiz_filler import get_quiz_current_question, answer_current_question, reset_to_previous_question

quiz_filler_blueprint = Blueprint('quiz_filler', __name__)


@quiz_filler_blueprint.route('/filler/<int:quiz_id>/current_question', methods=['GET'])
def get_current_question(quiz_id):
    """
    Retrieves the current question state for the given quiz or create a new quiz if no such exists.
    Response will contain field answers_given if previous answers have been given and will contain recommended_products if recommendations have been made.
    Example Response 1:
        {
            "answers_given": [
              {
                "answer_id": 2,
                "question_id": 1
              }
            ],
            "current_question": {
              "answers": [
                {
                  "id": 5,
                  "status": "published",
                  "text": "no"
                },
                {
                  "id": 4,
                  "status": "disabled",
                  "text": "maybe"
                },
                {
                  "id": 3,
                  "status": "published",
                  "text": "yes"
                }
              ],
              "id": 2,
              "status": "published",
              "text": "am i pretty"
        }

    Example Response 2:
        {
          "answers_given": [
            {
              "answer_id": 2,
              "question_id": 1
            },
            {
              "answer_id": 4,
              "question_id": 2
            }
          ],
          "recommended_products": [
            {
              "description": "desc1",
              "id": 2,
              "name": "name1",
              "status": "draft"
            },
            {
              "description": "desc2",
              "id": 3,
              "name": "name2",
              "status": "draft"
            }
          ]
        }
    """
    try:
        result = get_quiz_current_question(quiz_id)

        # Return recommended products if the quiz is complete
        if 'recommended_products' in result:
            return jsonify(result), 200

        # Return current question and previous answers
        return jsonify({
            "current_question": result['current_question'],
            "answers_given": result['answers_given']
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 500


@quiz_filler_blueprint.route('/filler/<int:quiz_id>/answer', methods=['POST'])
def answer_question(quiz_id):
    """
    Endpoint to answer the current question and get the next question along with previous answers.
    """
    try:
        data = request.get_json()
        answer_id = data.get('answer_id')

        if not answer_id:
            return jsonify({"error": "answer_id is required"}), 400

        result = answer_current_question(quiz_id, answer_id)
        # Check if recommended products exist
        if result.get("recommended_products"):
            response = jsonify({
                "recommended_products": result["recommended_products"],  # Return recommended products at the top level
                "answers_given": result["answers_given"]
            }), 200
            return response

        # If there are still more questions to answer
        if result.get("next_question"):
            response = jsonify({
                "next_question": result["next_question"],
                "answers_given": result["answers_given"]
            }), 200
            return response

        # If there are no more questions and no products recommended
        response = jsonify({
            "message": "No more questions",
            "answers_given": result["answers_given"]
        }), 200
        return response

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@quiz_filler_blueprint.route('/filler/<int:quiz_id>/reset_to_previous_question/<int:question_id>', methods=['POST'])
def reset_to_previous_question_endpoint(quiz_id, question_id):
    """
    Endpoint to reset the quiz to a previous question.
    Removes the given question and all following answers, and returns the current question and previous answers.
    """
    try:
        result = reset_to_previous_question(quiz_id, question_id)

        # Return the current question and previous answers after resetting
        return jsonify({
            "current_question": result['current_question'],
            "answers_given": result['answers_given']
        }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

