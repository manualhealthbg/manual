import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './QuestionsTable.css'; // Assuming you create a separate CSS file

const QuestionsTable = () => {
  const [questions, setQuestions] = useState([]);
  const [newQuestionText, setNewQuestionText] = useState(''); // State for new question
  const [newAnswerText, setNewAnswerText] = useState(''); // State for new answer

  useEffect(() => {
    const fetchQuestions = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/quiz/questions');
        setQuestions(response.data);
      } catch (error) {
        console.error('Error fetching questions and answers:', error);
      }
    };

    fetchQuestions();
  }, []);

  const handleStatusChange = async (type, id, action) => {
    try {
      let endpoint = '';

      // Construct the correct endpoint based on the type (question/answer) and action (publish/disable)
      if (type === 'question') {
        endpoint = action === 'publish'
          ? `http://127.0.0.1:5000/api/quiz/question/${id}/publish`
          : `http://127.0.0.1:5000/api/quiz/question/${id}/disable`;
      } else if (type === 'answer') {
        endpoint = action === 'publish'
          ? `http://127.0.0.1:5000/api/quiz/answer/${id}/publish`
          : `http://127.0.0.1:5000/api/quiz/answer/${id}/disable`;
      }

      await axios.post(endpoint);

      // Update the state locally to reflect the new status
      setQuestions(questions.map(q => {
        if (type === 'question' && q.id === id) {
          return { ...q, status: action === 'publish' ? 'published' : 'disabled' };
        }
        if (type === 'answer') {
          q.answers = q.answers.map(answer =>
            answer.id === id ? { ...answer, status: action === 'publish' ? 'published' : 'disabled' } : answer
          );
        }
        return q;
      }));
    } catch (error) {
      console.error('Error updating status:', error);
    }
  };

  const handleCreateQuestion = async () => {
    if (!newQuestionText) return alert('Question text is required!');

    try {
      await axios.post('http://127.0.0.1:5000/api/quiz/question', { text: newQuestionText });
      setNewQuestionText('');
      const response = await axios.get('http://127.0.0.1:5000/api/quiz/questions');
      setQuestions(response.data);
    } catch (error) {
      console.error('Error creating question:', error);
    }
  };

  const handleCreateAnswer = async (questionId) => {
    if (!newAnswerText) return alert('Answer text is required!');

    try {
      await axios.post('http://127.0.0.1:5000/api/quiz/answer', { text: newAnswerText, question_id: questionId });
      setNewAnswerText('');
      const response = await axios.get('http://127.0.0.1:5000/api/quiz/questions');
      setQuestions(response.data);
    } catch (error) {
      console.error('Error creating answer:', error);
    }
  };

  return (
    <div>
      <h1>Questions and Answers</h1>

      {/* Input for new question */}
      <div>
        <input
          type="text"
          value={newQuestionText}
          onChange={(e) => setNewQuestionText(e.target.value)}
          placeholder="Enter new question text"
        />
        <button onClick={handleCreateQuestion}>Create New Question</button>
      </div>

      <table className="questions-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Text</th>
            <th>Status</th>
            <th>Answers</th>
            <th>Change Status</th>
          </tr>
        </thead>
        <tbody>
          {questions.map(question => (
            <React.Fragment key={question.id}>
              <tr>
                <td>{question.id}</td>
                <td>{question.text}</td>
                <td>{question.status}</td> {/* Show current status of the question */}
                <td>
                  <ul>
                    {question.answers.map(answer => (
                      <li key={answer.id}>
                        <strong>ID: {answer.id}</strong> - {answer.text} ({answer.status}) {/* Show answer status */}
                        <button onClick={() => handleStatusChange('answer', answer.id, 'publish')}>Publish</button>
                        <button onClick={() => handleStatusChange('answer', answer.id, 'disable')}>Disable</button>
                      </li>
                    ))}
                  </ul>
                  <div>
                    <input
                      type="text"
                      value={newAnswerText}
                      onChange={(e) => setNewAnswerText(e.target.value)}
                      placeholder="Enter new answer"
                    />
                    <button onClick={() => handleCreateAnswer(question.id)}>Add Answer</button>
                  </div>
                </td>
                <td>
                  <button onClick={() => handleStatusChange('question', question.id, 'publish')}>Publish</button>
                  <button onClick={() => handleStatusChange('question', question.id, 'disable')}>Disable</button>
                </td>
              </tr>
            </React.Fragment>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default QuestionsTable;
