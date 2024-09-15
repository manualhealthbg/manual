import React, { useState, useEffect } from 'react';
import axios from 'axios';

const QuizFillPage = () => {
  const [quizId, setQuizId] = useState('');
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [recommendedProducts, setRecommendedProducts] = useState([]);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [previousAnswers, setPreviousAnswers] = useState([]); // Store previous answers
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [quizStarted, setQuizStarted] = useState(false); // Add this to track if quiz is started

  // Function to fetch the current question or recommended products for a quiz
  const fetchCurrentQuestion = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.get(`http://127.0.0.1:5000/api/filler/${quizId}/current_question`);

      // Check if there are recommended products
      if (response.data.recommended_products) {
        setRecommendedProducts(response.data.recommended_products);
        setPreviousAnswers(response.data.answers_given);
        setCurrentQuestion(null);
      } else {
        // Handle both current question and previous answers
        setCurrentQuestion(response.data.current_question);
        setPreviousAnswers(response.data.answers_given || []); // Initialize with previous answers if available
        setRecommendedProducts([]);
      }
      setQuizStarted(true); // Mark quiz as started once we get the first question
    } catch (err) {
      setError('Error fetching question');
      setCurrentQuestion(null);
    } finally {
      setLoading(false);
    }
  };


  // Function to handle submitting the answer
  const submitAnswer = async () => {
    if (!selectedAnswer) {
      alert('Please select an answer');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      const response = await axios.post(`http://127.0.0.1:5000/api/filler/${quizId}/answer`, {
        answer_id: selectedAnswer,
      });

      // Check if there are recommended products at the top level
      if (response.data.recommended_products) {
        setRecommendedProducts(response.data.recommended_products);
        setPreviousAnswers(response.data.answers_given); // Make sure to update previous answers here
        setCurrentQuestion(null);
      } else if (response.data.message === 'No more questions') {
        alert('You have completed the quiz!');
        setPreviousAnswers(response.data.answers_given); // Also update previous answers here
        setCurrentQuestion(null);
      } else {
        setCurrentQuestion(response.data.next_question);
        setPreviousAnswers(response.data.answers_given); // Update previous answers
        setSelectedAnswer(null);
      }

    } catch (err) {
      setError('Error submitting answer');
    } finally {
      setLoading(false);
    }
  };

  // Function to reset to a previous question
  const resetToPreviousQuestion = async (questionId) => {
    try {
      setLoading(true);
      setError(null);
      const response = await axios.post(`http://127.0.0.1:5000/api/filler/${quizId}/reset_to_previous_question/${questionId}`);

      // Handle the reset response which returns the current question and previous answers
      if (response.data.current_question) {
        setCurrentQuestion(response.data.current_question);
        setPreviousAnswers(response.data.answers_given || []);
        setRecommendedProducts([]);
        setSelectedAnswer(null);
      }

    } catch (err) {
      setError('Error resetting to previous question');
    } finally {
      setLoading(false);
    }
  };

  // Function to handle quizId submission
  const handleQuizIdSubmit = () => {
    if (quizId) {
      fetchCurrentQuestion();
    } else {
      alert('Please enter a quiz ID');
    }
  };

  return (
    <div>
      <h1>Quiz Fill Page</h1>

      {/* Only show the quiz ID input form if the quiz hasn't started yet */}
      {!quizStarted && (
        <div>
          <label htmlFor="quizId">Enter Quiz ID: </label>
          <input
            type="text"
            id="quizId"
            value={quizId}
            onChange={(e) => setQuizId(e.target.value)}
          />
          <button onClick={handleQuizIdSubmit}>Start Quiz</button>
        </div>
      )}

      {loading && <p>Loading...</p>}

      {/* Display current question */}
      {currentQuestion && currentQuestion.text && (
        <div>
          <h2>{currentQuestion.text}</h2>
          <ul>
            {currentQuestion.answers.map((answer) => (
              <li key={answer.id}>
                <label>
                  <input
                    type="radio"
                    name="answer"
                    value={answer.id}
                    checked={selectedAnswer === answer.id}
                    onChange={() => setSelectedAnswer(answer.id)}
                  />
                  {answer.text}
                </label>
              </li>
            ))}
          </ul>
          <button onClick={submitAnswer}>Submit Answer</button>
        </div>
      )}

      {/* Display recommended products */}
      {recommendedProducts.length > 0 && (
        <div>
          <h2>Product Recommendations</h2>
          <ul>
            {recommendedProducts.map((product) => (
              <li key={product.id}>
                <strong>{product.name}</strong>: {product.description}
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Display previous answers with "Return to this" button */}
      {previousAnswers.length > 0 && (
        <div>
          <h2>Previous Answers</h2>
          <ul>
            {previousAnswers.map((entry, index) => (
              <li key={index}>
                Question ID: {entry.question_id}, Answer ID: {entry.answer_id}
                <button onClick={() => resetToPreviousQuestion(entry.question_id)}>Return to this</button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {error && <p style={{ color: 'red' }}>{error}</p>}
    </div>
  );
};

export default QuizFillPage;
