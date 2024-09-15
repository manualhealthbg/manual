import React, { useState, useEffect } from 'react';
import axios from 'axios';

const ProductRestrictions = () => {
  const [questions, setQuestions] = useState([]);
  const [newRestrictions, setNewRestrictions] = useState({}); // State for tracking restrictions per answer
  const [feedbackMessage, setFeedbackMessage] = useState(''); // Feedback message for users

  useEffect(() => {
    // Fetch questions and answers from the API
    axios.get('http://127.0.0.1:5000/api/quiz/questions')
      .then(response => setQuestions(response.data))
      .catch(error => console.error("There was an error fetching the questions!", error));
  }, []);

  const handleAddRestriction = (answerId) => {
    const restriction = newRestrictions[answerId] || { productId: '' };

    axios.post('http://127.0.0.1:5000/api/restriction', { product_id: restriction.productId, answer_id: answerId })
      .then(response => {
        setFeedbackMessage('Restriction added successfully!'); // Set feedback message
        setTimeout(() => setFeedbackMessage(''), 3000); // Clear message after 3 seconds
        fetchRestrictions(answerId); // Refresh restrictions
      })
      .catch(error => {
        console.error("There was an error adding the restriction!", error);
        setFeedbackMessage('Error adding restriction.');
      });
  };

  const handleRemoveRestriction = (restrictionId, answerId) => {
    axios.delete(`http://127.0.0.1:5000/api/restriction/${restrictionId}`)
      .then(response => {
        setFeedbackMessage('Restriction removed successfully!'); // Set feedback message
        setTimeout(() => setFeedbackMessage(''), 3000); // Clear message after 3 seconds
        fetchRestrictions(answerId); // Refresh restrictions
      })
      .catch(error => {
        console.error("There was an error removing the restriction!", error);
        setFeedbackMessage('Error removing restriction.');
      });
  };

  const fetchRestrictions = (answerId) => {
    axios.get(`http://127.0.0.1:5000/api/product_restrictions/${answerId}`)
      .then(response => {
        setQuestions(prevQuestions =>
          prevQuestions.map(question => ({
            ...question,
            answers: question.answers.map(a =>
              a.id === answerId ? { ...a, restrictions: response.data } : a
            )
          }))
        );
      })
      .catch(error => console.error("There was an error fetching the restrictions!", error));
  };

  const handleInputChange = (answerId, field, value) => {
    setNewRestrictions(prevState => ({
      ...prevState,
      [answerId]: {
        ...prevState[answerId],
        [field]: value
      }
    }));
  };

  return (
    <div>
      <h1>Product Restrictions</h1>

      {/* Display feedback messages */}
      {feedbackMessage && <p style={{ color: feedbackMessage.includes('Error') ? 'red' : 'green' }}>{feedbackMessage}</p>}

      <table>
        <thead>
          <tr>
            <th>Question</th>
            <th>Answer</th>
            <th>Product Restrictions</th>
          </tr>
        </thead>
        <tbody>
          {questions && questions.length > 0 && questions.map(question => (
            <React.Fragment key={question.id}>
              {question.answers && question.answers.length > 0 && question.answers.map(answer => (
                <tr key={answer.id}>
                  <td>{question.text}</td>
                  <td>{answer.text}</td>
                  <td>
                    <ul>
                      {answer.restrictions && answer.restrictions.length > 0 ? (
                        answer.restrictions.map(restriction => (
                          <li key={restriction.id}>
                            Product ID: {restriction.product_id}
                            <button onClick={() => handleRemoveRestriction(restriction.id, answer.id)}>Remove</button>
                          </li>
                        ))
                      ) : (
                        <li>No restrictions</li>
                      )}
                    </ul>
                    <input
                      type="text"
                      placeholder="Product ID"
                      value={newRestrictions[answer.id]?.productId || ''}
                      onChange={(e) => handleInputChange(answer.id, 'productId', e.target.value)}
                    />
                    <button onClick={() => handleAddRestriction(answer.id)}>Add Restriction</button>
                  </td>
                </tr>
              ))}
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ProductRestrictions;
