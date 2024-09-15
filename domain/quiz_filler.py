from services.db_config import quiz_collection


class QuizFiller:
    def __init__(self, quiz_id, quiz_snapshot, progress=None):
        self.quiz_id = quiz_id
        self.questions = {q['id']: q for q in quiz_snapshot['questions']}
        self.products = {product['id']: product for product in quiz_snapshot['products']}
        self.product_restrictions = quiz_snapshot['product_restrictions']
        self.question_transitions = quiz_snapshot['question_transitions']

        self.progress = progress or {
            "answers_given": [],
            "current_question_id": self._get_first_question_id(),
            "recommended_products": []
        }

    def _get_first_question_id(self):
        """Get the first published question's ID."""
        for question in self.questions.values():
            if question.get('status') == 'published':
                return question['id']
        return None

    def get_current_question(self):
        """Get the current question based on the progress."""
        current_question_id = self.progress['current_question_id']
        if current_question_id is None:
            return None
        return self.questions.get(current_question_id)

    def answer(self, answer_id, current_question):
        """
        Process the answer and determine the next question or recommended products,
        ensuring restricted products are not recommended.
        """
        # Validate the answer ID
        valid_answer = next((answer for answer in current_question['answers'] if answer['id'] == answer_id), None)
        if valid_answer is None:
            raise ValueError(f"Invalid answer ID {answer_id} for question {current_question['id']}")

        # Append the current answer to the progress
        self.progress['answers_given'].append({'question_id': current_question['id'], 'answer_id': answer_id})

        # Get the result of the answer to decide the next question or recommended products
        transition_result = self._get_transition_result(answer_id)

        if transition_result.get('next_question_id'):
            # Move to the next question if available
            self.progress['current_question_id'] = transition_result['next_question_id']
            return self.get_current_question()

        elif transition_result.get('product_ids'):
            # Get all answer_ids from answers_given
            answer_ids = [entry['answer_id'] for entry in self.progress['answers_given']]

            # Fetch restricted products for those answers
            restricted_product_ids = self._get_restricted_products_for_answers(answer_ids)

            # Recommend products that are not restricted
            recommended_products = [
                self.products[product_id]
                for product_id in transition_result['product_ids']
                if product_id not in restricted_product_ids
            ]

            self.progress['recommended_products'] = recommended_products

            return {"recommended_products": recommended_products}

        # End of quiz (no more questions or recommendations)
        self.progress['current_question_id'] = None
        return None

    def _get_restricted_products_for_answers(self, answer_ids):
        """
        Get restricted product IDs for a given set of answer_ids from product_restrictions.

        :param answer_ids: List of answer IDs for which to fetch restrictions.
        :return: Set of restricted product IDs.
        """
        restricted_products = set()

        # Loop through all restrictions in product_restrictions
        for restriction in self.product_restrictions:
            if restriction['answer_id'] in answer_ids:
                restricted_products.add(restriction['product_id'])

        return restricted_products

    def _get_transition_result(self, answer_id):
        """
        Determines the next action based on the given answer ID using the question_transitions.
        Either returns a next question ID or a list of product IDs.
        """
        next_question_id = None
        product_ids = []

        for transition in self.question_transitions:
            if transition['answer_id'] == answer_id:
                if transition.get('next_question_id'):
                    next_question_id = transition['next_question_id']
                    break
                elif transition.get('product_id'):
                    product_ids.append(transition['product_id'])

        return {"next_question_id": next_question_id, "product_ids": product_ids}

    def save_progress(self):
        """Updates the MongoDB document with the quiz's progress."""
        quiz_collection.update_one(
            {"quiz_id": self.quiz_id},
            {"$set": {"progress": self.progress}},
            upsert=True
        )
