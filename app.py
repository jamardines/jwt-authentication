import os
import logging
from flask import Flask
from config import Config
from extensions import db

# initialize app

app = Flask(__name__)
app.config.from_object(Config)

# initialize db
db.init_app(app)

# configure logging
os.makedirs(app.config['LOG_FOLDER'], exist_ok=True)
logging.basicConfig(
    filename=f"{app.config['LOG_FOLDER']}/app.log",
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

# register blueprints
from controllers.file_controller import file_bp
from controllers.authentication_controller import auth_bp
app.register_blueprint(file_bp)
app.register_blueprint(auth_bp)

# Create tables if not exist
with app.app_context():
    print("Creating database tables...")
    db.create_all()
    print("Database tables created.")

@app.route('/')
def index():
    return "✅ Flask app is running successfully!"

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)