from flask import Flask
from flask_cors import CORS
from views.questions_views import questions_blueprint
from views.product_views import product_blueprint
from views.quiz_filler import quiz_filler_blueprint
from views.question_transitions_views import question_transitions_blueprint

app = Flask(__name__)
# Enable CORS for all routes and allow the necessary methods
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

# Register blueprints
app.register_blueprint(questions_blueprint, url_prefix='/api/quiz')
app.register_blueprint(product_blueprint, url_prefix='/api')
app.register_blueprint(quiz_filler_blueprint, url_prefix='/api')
app.register_blueprint(question_transitions_blueprint, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
