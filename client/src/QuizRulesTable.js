import React, { useState, useEffect } from 'react';
import axios from 'axios';

const QuizRulesTable = () => {
  const [quizRules, setQuizRules] = useState([]);
  const [editing, setEditing] = useState(null);
  const [newRule, setNewRule] = useState({ answer_id: '', next_question_id: '', product_id: '' });

  // Fetch all quiz rules on component mount
  useEffect(() => {
    const fetchQuizRules = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:5000/api/question_transitions');
        setQuizRules(response.data);
      } catch (error) {
        console.error('Error fetching quiz rules:', error);
      }
    };

    fetchQuizRules();
  }, []);

  // Handle input changes for existing quiz rules (for editing)
  const handleChange = (e, field, ruleId) => {
    const { value } = e.target;
    setQuizRules(quizRules.map(rule =>
      rule.id === ruleId ? { ...rule, [field]: value } : rule
    ));
  };

  // Handle input changes for new quiz rules
  const handleNewRuleChange = (e) => {
    const { name, value } = e.target;
    setNewRule(prevState => ({
      ...prevState,
      [name]: value,
    }));
  };

  // Save updates to a quiz rule
  const handleSave = async (ruleId) => {
    const rule = quizRules.find(r => r.id === ruleId);
    try {
      await axios.put(`http://127.0.0.1:5000/api/question_transitions/${ruleId}`, rule);
      setEditing(null); // Exit editing mode
    } catch (error) {
      console.error('Error updating quiz rule:', error);
    }
  };

  // Create a new quiz rule
  const handleCreateRule = async () => {
    // Ensure either next_question_id or product_id is filled, but not both
    if (!newRule.next_question_id && !newRule.product_id) {
      alert('Either Next Question ID or Product ID must be specified.');
      return;
    }
    if (newRule.next_question_id && newRule.product_id) {
      alert('Cannot have both Next Question ID and Product ID for the same rule.');
      return;
    }

    try {
      await axios.post('http://127.0.0.1:5000/api/question_transitions', newRule);
      setNewRule({ answer_id: '', next_question_id: '', product_id: '' }); // Clear form after submission
      const response = await axios.get('http://127.0.0.1:5000/api/question_transitions');
      setQuizRules(response.data); // Refresh the list of quiz rules
    } catch (error) {
      console.error('Error creating quiz rule:', error);
    }
  };

  // Delete a quiz rule
  const handleDelete = async (ruleId) => {
    try {
      await axios.delete(`http://127.0.0.1:5000/api/question_transitions/${ruleId}`);
      const response = await axios.get('http://127.0.0.1:5000/api/question_transitions');
      setQuizRules(response.data); // Refresh the list of quiz rules after deletion
    } catch (error) {
      console.error('Error deleting quiz rule:', error);
    }
  };

  return (
    <div>
      <h1>Quiz Rules</h1>

      {/* Form for creating a new quiz rule */}
      <h2>Create New Quiz Rule</h2>
      <div>
        <input
          type="text"
          name="answer_id"
          placeholder="Answer ID"
          value={newRule.answer_id}
          onChange={handleNewRuleChange}
        />
        <input
          type="text"
          name="next_question_id"
          placeholder="Next Question ID (optional)"
          value={newRule.next_question_id}
          onChange={handleNewRuleChange}
        />
        <input
          type="text"
          name="product_id"
          placeholder="Product ID (optional)"
          value={newRule.product_id}
          onChange={handleNewRuleChange}
        />
        <button onClick={handleCreateRule}>Create Quiz Rule</button>
      </div>

      {/* Table for displaying and editing quiz rules */}
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Answer ID</th>
            <th>Next Question ID</th>
            <th>Product ID</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {quizRules.map(rule => (
            <tr key={rule.id}>
              <td>{rule.id}</td>
              <td>
                {editing === rule.id ? (
                  <input
                    type="text"
                    value={rule.answer_id}
                    onChange={(e) => handleChange(e, 'answer_id', rule.id)}
                  />
                ) : (
                  rule.answer_id
                )}
              </td>
              <td>
                {editing === rule.id ? (
                  <input
                    type="text"
                    value={rule.next_question_id}
                    onChange={(e) => handleChange(e, 'next_question_id', rule.id)}
                  />
                ) : (
                  rule.next_question_id || 'N/A'
                )}
              </td>
              <td>
                {editing === rule.id ? (
                  <input
                    type="text"
                    value={rule.product_id}
                    onChange={(e) => handleChange(e, 'product_id', rule.id)}
                  />
                ) : (
                  rule.product_id || 'N/A'
                )}
              </td>
              <td>
                {editing === rule.id ? (
                  <button onClick={() => handleSave(rule.id)}>Save</button>
                ) : (
                  <>
                    <button onClick={() => setEditing(rule.id)}>Edit</button>
                    <button onClick={() => handleDelete(rule.id)}>Delete</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default QuizRulesTable;
