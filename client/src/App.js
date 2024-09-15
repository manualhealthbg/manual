import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import ProductTable from './ProductTable';
import ProductRestrictions from './ProductRestrictions';
import QuestionsTable from './QuestionsTable';
import QuizFillPage from './QuizFillPage';
import QuizRulesTable from './QuizRulesTable';
import './App.css'; // Importing CSS for styles

// Home page with two big icons
const HomePage = () => {
  return (
    <div className="homepage-container">
      <Link to="/quiz/fill" className="home-button fill-quiz">
        Fill Quiz
      </Link>
      <Link to="/admin" className="home-button admin">
        Admin
      </Link>
    </div>
  );
};

// Admin page with all admin links
const AdminPage = () => {
  return (
    <div className="admin-page">
      <h1>Admin Dashboard</h1>
      <ul>
        <li><Link to="/admin/product_restrictions">Product Restrictions</Link></li>
        <li><Link to="/admin/product">Product Table</Link></li>
        <li><Link to="/admin/questions">Questions Table</Link></li>
        <li><Link to="/admin/quiz_rules">Quiz Rules Table</Link></li>
      </ul>
    </div>
  );
};

// Main App Component
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/quiz/fill" element={<QuizFillPage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/admin/product_restrictions" element={<ProductRestrictions />} />
        <Route path="/admin/product" element={<ProductTable />} />
        <Route path="/admin/questions" element={<QuestionsTable />} />
        <Route path="/admin/quiz_rules" element={<QuizRulesTable />} />
      </Routes>
    </Router>
  );
}

export default App;
