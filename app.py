from flask import Flask
from database import init_db
from auth import auth_bp
from routes.game_routes import game_bp

app = Flask(__name__)

# Initialize database
init_db()

# Register all blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')  # Authentication routes
app.register_blueprint(game_bp, url_prefix='/game')  # Game routes

if __name__ == "__main__":
    app.run(debug=True)
