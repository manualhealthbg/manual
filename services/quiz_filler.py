from domain.quiz_filler import QuizFiller
from services.product import get_all_products
from services.quiz import get_all_questions, get_all_product_restrictions
from services.question_transitions import get_question_transitions
from services.db_config import quiz_collection


def init_quiz(quiz_id):
    """
    Initializes a new quiz by fetching data from MySQL and
    inserting the initialized quiz data along with the initial progress into MongoDB.
    """
    try:
        questions = get_all_questions()
        products = get_all_products()
        product_restrictions = get_all_product_restrictions()
        question_transitions = get_question_transitions()

        quiz_data = {
            "quiz_id": quiz_id,
            "quiz_snapshot": {
                "questions": questions,
                "products": products,
                "product_restrictions": product_restrictions,
                "question_transitions": question_transitions
            },
            "progress": {
                "answers_given": [],
                "current_question_id": next((q["id"] for q in questions if q["status"] == "published"), None),
                "recommended_products": []
            }
        }

        quiz_collection.update_one(
            {"quiz_id": quiz_id},
            {"$set": quiz_data},
            upsert=True
        )

        print(f"Quiz initialized {quiz_id} and stored in MongoDB.")
    except Exception as e:
        print(f"Error initializing quiz for quiz {quiz_id}: {e}")
        raise e

def get_quiz(quiz_id, force_create=False):
    """
    Retrieves the quiz from MongoDB.
    If force_create is True, it initializes a new quiz if none exists.

    :param quiz_id: The ID of the quiz to retrieve the quiz for
    :param force_create: If True, create a new quiz if no quiz exists for the id
    :return: A QuizFiller object if a quiz is found or created
    """
    quiz_data = quiz_collection.find_one({"quiz_id": quiz_id})

    if quiz_data:
        return QuizFiller(
            quiz_id,
            quiz_data['quiz_snapshot'],
            quiz_data.get('progress', {})
        )
    elif force_create:
        init_quiz(quiz_id)
        return get_quiz(quiz_id)
    else:
        raise ValueError(f"No quiz found for id {quiz_id}")


def get_quiz_current_question(quiz_id):
    quiz_filler = get_quiz(quiz_id, force_create=True)

    # Check if there are recommended products stored in progress
    if 'recommended_products' in quiz_filler.progress and quiz_filler.progress['recommended_products']:
        return {
            "recommended_products": quiz_filler.progress['recommended_products'],
            "answers_given": quiz_filler.progress['answers_given']  # Include previous answers
        }

    # Otherwise, get the current question and also return previous answers
    current_question = quiz_filler.get_current_question()
    quiz_filler.save_progress()  # Save the progress back to MongoDB

    return {
        "current_question": current_question,
        "answers_given": quiz_filler.progress['answers_given']  # Include previous answers
    }


def answer_current_question(quiz_id, answer_id):
    quiz_filler = get_quiz(quiz_id)

    current_question = quiz_filler.get_current_question()

    if current_question is None:
        raise ValueError("No current question found.")

    if any(answer['question_id'] == current_question['id'] for answer in quiz_filler.progress['answers_given']):
        raise ValueError("This question has already been answered.")

    result = quiz_filler.answer(answer_id, current_question)

    quiz_filler.save_progress()

    # If result contains recommended products, return them at the top level
    if "recommended_products" in result:
        return {
            "recommended_products": result["recommended_products"],
            "answers_given": quiz_filler.progress['answers_given']
        }

    # Otherwise, return the next question
    return {
        "next_question": result,
        "answers_given": quiz_filler.progress['answers_given']
    }

def reset_to_previous_question(quiz_id, question_id):
    quiz_filler = get_quiz(quiz_id)  # Load the quiz for the given ID

    # Step 1: Check if the question exists in the answers_given list
    answers_given = quiz_filler.progress['answers_given']
    question_index = None

    for index, answer in enumerate(answers_given):
        if answer['question_id'] == question_id:
            question_index = index
            break

    if question_index is None:
        raise ValueError(f"Question with ID {question_id} has not been answered yet.")

    # Step 2: Remove the specified question and all following answers
    quiz_filler.progress['answers_given'] = answers_given[:question_index]

    # Step 3: Set the specified question as the current question
    quiz_filler.progress['current_question_id'] = question_id

    # Step 4: Save the updated progress
    quiz_filler.save_progress()

    # Step 5: Return the response similar to get_quiz_current_question
    current_question = quiz_filler.get_current_question()

    return {
        "current_question": current_question,
        "answers_given": quiz_filler.progress['answers_given']  # Return updated answers_given list
    }

